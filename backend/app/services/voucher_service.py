from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
from app.models.voucher import Voucher
from app.schemas.voucher import VoucherCreate, VoucherUpdate, KiemTraVoucherResponse
from fastapi import HTTPException


class VoucherService:
    @staticmethod
    async def kiem_tra_voucher(
        db: Session, ma_voucher: str, tong_bill: float
    ) -> KiemTraVoucherResponse:
        """Kiem tra ma voucher co ton tai, con han, du dieu kien don hang hay khong"""
        voucher = db.query(Voucher).filter(Voucher.ma_voucher == ma_voucher).first()

        # ---- Status: da_huy -> hidden completely (treat as not found) ----
        if not voucher or voucher.trang_thai == "da_huy":
            return KiemTraVoucherResponse(
                hop_le=False, loi="Ma giam gia khong ton tai", ma_voucher=ma_voucher
            )

        # ---- Status: tam_dung -> show but reject ----
        if voucher.trang_thai == "tam_dung":
            return KiemTraVoucherResponse(
                hop_le=False,
                loi="Ma giam gia dang bao tri, vui long quay lai sau",
                ma_voucher=ma_voucher,
            )

        # ---- Status: het_han -> reject with specific message ----
        # (status may be set manually by admin OR auto-set when runs out)
        if voucher.trang_thai == "het_han":
            return KiemTraVoucherResponse(
                hop_le=False,
                loi="Ma giam gia da het han su dung",
                ma_voucher=ma_voucher,
            )

        # ---- Status: dang_hoat_dong -> continue checks below ----

        # Kiem tra ngay het han (date-based expiry check)
        if voucher.ngay_het_han and voucher.ngay_het_han < datetime.utcnow():
            return KiemTraVoucherResponse(
                hop_le=False,
                loi="Ma giam gia da qua han su dung",
                ma_voucher=ma_voucher,
            )

        # Kiem tra so luong con lai
        if voucher.so_luong_con_lai <= 0:
            return KiemTraVoucherResponse(
                hop_le=False,
                loi="Ma giam gia da het luot su dung",
                ma_voucher=ma_voucher,
            )

        # Kiem tra don hang toi thieu
        if tong_bill < voucher.don_hang_toi_thieu:
            return KiemTraVoucherResponse(
                hop_le=False,
                loi=f"Don hang chua dat gia tri toi thieu {voucher.don_hang_toi_thieu:,.0f}₫",
                ma_voucher=ma_voucher,
            )

        # Tinh so tien giam thuc te
        so_tien_giam = await VoucherService.tinh_so_tien_giam(tong_bill, voucher)

        return KiemTraVoucherResponse(
            hop_le=True,
            loi=None,
            ma_voucher=voucher.ma_voucher,
            loai_giam_gia=voucher.loai_giam_gia,
            gia_tri_giam=voucher.gia_tri_giam,
            giam_toi_da=voucher.giam_toi_da,
            so_tien_giam=so_tien_giam,
        )

    @staticmethod
    async def tinh_so_tien_giam(tong_bill: float, voucher: Voucher) -> float:
        """Tra ve so tien khach duoc giam thuc te"""
        if voucher.loai_giam_gia == "phan_tram":
            so_tien = tong_bill * voucher.gia_tri_giam / 100
            # Neu co giam_toi_da, khong vuot qua muc nay
            if voucher.giam_toi_da and so_tien > voucher.giam_toi_da:
                so_tien = voucher.giam_toi_da
            return round(so_tien, 0)
        else:
            # Loai so_tien: giam truc tiep
            return min(voucher.gia_tri_giam, tong_bill)

    @staticmethod
    async def cap_nhat_luot_dung(db: Session, id_voucher: int):
        """Tru di 1 luot su dung sau khi don hang thanh cong"""
        voucher = db.query(Voucher).filter(Voucher.id == id_voucher).first()
        if voucher and voucher.so_luong_con_lai > 0:
            voucher.so_luong_con_lai -= 1
            if voucher.so_luong_con_lai <= 0:
                voucher.trang_thai = "het_han"
            db.commit()
            db.refresh(voucher)

    @staticmethod
    async def lay_danh_sach_voucher(db: Session) -> List[Voucher]:
        """Lay danh sach voucher dang hoat dong (cho khach hang)"""
        now = datetime.utcnow()
        return (
            db.query(Voucher)
            .filter(
                Voucher.trang_thai == "dang_hoat_dong",
                Voucher.ngay_het_han >= now,
                Voucher.so_luong_con_lai > 0,
            )
            .all()
        )

    @staticmethod
    async def lay_danh_sach_voucher_cho_user(db: Session) -> List[Voucher]:
        """Lay danh sach voucher cho user (loai tru da_huy - bao gom dang_hoat_dong, tam_dung, het_han)"""
        return (
            db.query(Voucher)
            .filter(Voucher.trang_thai != "da_huy")
            .order_by(Voucher.ngay_tao.desc())
            .all()
        )

    @staticmethod
    async def lay_tat_ca_voucher(db: Session) -> List[Voucher]:
        """Lay tat ca voucher (cho Admin)"""
        return db.query(Voucher).order_by(Voucher.ngay_tao.desc()).all()

    @staticmethod
    async def cap_nhat_trang_thai(db: Session, id: int, trang_thai: str) -> Voucher:
        """Admin cap nhat nhanh trang thai voucher (dang_hoat_dong / tam_dung)"""
        voucher = db.query(Voucher).filter(Voucher.id == id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Khong tim thay voucher")

        voucher.trang_thai = trang_thai
        db.commit()
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        status_vn = "Đang hoạt động" if trang_thai == "dang_hoat_dong" else "Tạm dừng"
        AdminActivityService.ghi_log(db, f"Cập nhật trạng thái mã giảm giá {voucher.ma_voucher} thành: {status_vn}", "Admin")
        
        db.refresh(voucher)
        return voucher

    @staticmethod
    async def tao_voucher(db: Session, data: VoucherCreate) -> Voucher:
        """Admin tao voucher moi"""
        # Kiem tra ma da ton tai
        existing = (
            db.query(Voucher).filter(Voucher.ma_voucher == data.ma_voucher).first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Ma voucher da ton tai")

        voucher = Voucher(**data.model_dump())
        db.add(voucher)
        db.commit()
        db.refresh(voucher)
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        AdminActivityService.ghi_log(db, f"Đã tạo mã giảm giá mới: {voucher.ma_voucher}", "Admin")
        
        return voucher

    @staticmethod
    async def cap_nhat_voucher(db: Session, id: int, data: VoucherUpdate) -> Voucher:
        """Admin cap nhat voucher"""
        voucher = db.query(Voucher).filter(Voucher.id == id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Khong tim thay voucher")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(voucher, key, value)

        db.commit()
        db.refresh(voucher)
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        AdminActivityService.ghi_log(db, f"Đã cập nhật thông tin mã giảm giá: {voucher.ma_voucher}", "Admin")
        
        return voucher

    @staticmethod
    async def xoa_voucher(db: Session, id: int):
        """Admin xoa voucher"""
        voucher = db.query(Voucher).filter(Voucher.id == id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Khong tim thay voucher")

        code = voucher.ma_voucher
        db.delete(voucher)
        db.commit()
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        AdminActivityService.ghi_log(db, f"Xóa vĩnh viễn mã giảm giá: {code}", "Admin")
        
        return {"message": "Da xoa voucher thanh cong"}
