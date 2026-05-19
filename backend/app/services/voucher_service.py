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
        """
        Kiểm tra độ hợp lệ của một mã giảm giá (voucher) cụ thể.
        Xét các điều kiện: mã tồn tại, không bị hủy, chưa hết hạn, còn lượt sử dụng, và tổng tiền đạt giá trị tối thiểu.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            ma_voucher (str): Mã code giảm giá cần kiểm tra.
            tong_bill (float): Tổng giá trị của đơn hàng hiện tại.

        Returns:
            KiemTraVoucherResponse: Kết quả kiểm tra chi tiết (hợp lệ hay không, lỗi cụ thể và số tiền giảm).
        """
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
        """
        Tính toán số tiền giảm giá thực tế của voucher dựa trên cấu hình (phần trăm kèm mức tối đa hoặc số tiền cố định).

        Args:
            tong_bill (float): Tổng giá trị hóa đơn.
            voucher (Voucher): Đối tượng mã giảm giá đang xét.

        Returns:
            float: Số tiền được chiết khấu giảm giá.
        """
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
        """
        Trừ đi 1 lượt sử dụng của voucher sau khi đơn hàng áp dụng thành công.
        Tự động chuyển trạng thái sang 'het_han' nếu lượt sử dụng còn lại về 0.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            id_voucher (int): ID định danh của voucher.
        """
        voucher = db.query(Voucher).filter(Voucher.id == id_voucher).first()
        if voucher and voucher.so_luong_con_lai > 0:
            voucher.so_luong_con_lai -= 1
            if voucher.so_luong_con_lai <= 0:
                voucher.trang_thai = "het_han"
            db.commit()
            db.refresh(voucher)

    @staticmethod
    async def lay_danh_sach_voucher(db: Session) -> List[Voucher]:
        """
        Lấy danh sách mã giảm giá đang hoạt động, chưa quá hạn, và còn số lượt sử dụng.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

        Returns:
            List[Voucher]: Danh sách các voucher khả dụng cho khách hàng.
        """
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
        """
        Lấy danh sách voucher dành cho hiển thị ở phía Client (bao gồm cả mã tạm dừng hoặc hết hạn, loại trừ mã đã hủy).

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

        Returns:
            List[Voucher]: Danh sách voucher hiển thị.
        """
        return (
            db.query(Voucher)
            .filter(Voucher.trang_thai != "da_huy")
            .order_by(Voucher.ngay_tao.desc())
            .all()
        )

    @staticmethod
    async def lay_tat_ca_voucher(db: Session) -> List[Voucher]:
        """
        Lấy toàn bộ danh sách voucher trong hệ thống phục vụ giao diện quản trị của Admin.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

        Returns:
            List[Voucher]: Danh sách đầy đủ voucher sắp xếp theo thời gian tạo mới nhất.
        """
        return db.query(Voucher).order_by(Voucher.ngay_tao.desc()).all()

    @staticmethod
    async def cap_nhat_trang_thai(db: Session, id: int, trang_thai: str) -> Voucher:
        """
        Cập nhật nhanh trạng thái bật/tắt của một mã giảm giá.
        Đồng thời ghi nhật ký hoạt động của quản trị viên.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            id (int): ID của voucher cần cập nhật.
            trang_thai (str): Trạng thái mới thiết lập (dang_hoat_dong / tam_dung).

        Returns:
            Voucher: Đối tượng voucher sau cập nhật.

        Raises:
            HTTPException: Lỗi 404 nếu không tìm thấy voucher.
        """
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
        """
        Tạo mới một mã giảm giá trong hệ thống.
        Kiểm tra mã trùng lặp và ghi nhật ký hoạt động quản trị viên.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            data (VoucherCreate): Dữ liệu cấu hình voucher mới.

        Returns:
            Voucher: Đối tượng voucher vừa tạo.

        Raises:
            HTTPException: Lỗi 400 nếu mã voucher đã tồn tại trước đó.
        """
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
        """
        Cập nhật thông tin chi tiết của một mã giảm giá trong DB.
        Đồng thời ghi nhật ký hoạt động của quản trị viên.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            id (int): ID định danh của voucher cần cập nhật.
            data (VoucherUpdate): Dữ liệu cập nhật mới.

        Returns:
            Voucher: Đối tượng sau cập nhật thành công.

        Raises:
            HTTPException: Lỗi 404 nếu không tìm thấy voucher.
        """
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
        """
        Xóa vĩnh viễn một mã giảm giá khỏi hệ thống.
        Đồng thời ghi nhật ký hoạt động của quản trị viên.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            id (int): ID định danh của voucher cần xóa.

        Returns:
            dict: Thông báo kết quả xóa voucher thành công.

        Raises:
            HTTPException: Lỗi 404 nếu không tìm thấy voucher.
        """
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
