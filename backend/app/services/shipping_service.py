from sqlalchemy.orm import Session
from typing import List
from app.models.don_vi_van_chuyen import DonViVanChuyen
from app.schemas.shipping import DonViVanChuyenCreate, DonViVanChuyenUpdate
from fastapi import HTTPException


class ShippingService:
    @staticmethod
    async def lay_danh_sach_don_vi(db: Session) -> List[DonViVanChuyen]:
        """
        Lấy danh sách các đơn vị vận chuyển đang kích hoạt hoạt động trong hệ thống.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

        Returns:
            List[DonViVanChuyen]: Danh sách các đơn vị vận chuyển khả dụng.
        """
        return db.query(DonViVanChuyen).filter(DonViVanChuyen.kich_hoat.is_(True)).all()

    @staticmethod
    async def lay_tat_ca_don_vi(db: Session) -> List[DonViVanChuyen]:
        """
        Lấy toàn bộ danh sách đơn vị vận chuyển phục vụ cho giao diện quản trị của Admin.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

        Returns:
            List[DonViVanChuyen]: Danh sách tất cả đơn vị vận chuyển.
        """
        return db.query(DonViVanChuyen).all()

    @staticmethod
    async def tinh_phi_ship(ma_don_vi: str, tong_bill: float, db: Session) -> float:
        """
        Tính toán chi phí giao hàng dựa theo mã đơn vị vận chuyển và giá trị hóa đơn.
        Áp dụng chính sách miễn phí giao hàng nếu tổng tiền vượt ngưỡng miễn phí của đơn vị đó.

        Args:
            ma_don_vi (str): Mã định danh của đơn vị giao hàng.
            tong_bill (float): Tổng giá trị của đơn hàng để xét miễn phí giao hàng.
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

        Returns:
            float: Chi phí giao hàng sau khi tính toán.

        Raises:
            HTTPException: Lỗi 404 nếu không tìm thấy đơn vị vận chuyển tương ứng.
        """
        don_vi = (
            db.query(DonViVanChuyen)
            .filter(DonViVanChuyen.ma_don_vi == ma_don_vi)
            .first()
        )

        if not don_vi:
            raise HTTPException(
                status_code=404, detail="Khong tim thay don vi van chuyen"
            )

        # Neu tong bill >= nguong mien phi, free ship
        if don_vi.nguong_mien_phi > 0 and tong_bill >= don_vi.nguong_mien_phi:
            return 0

        return don_vi.phi_co_dinh

    @staticmethod
    async def tao_don_vi(db: Session, data: DonViVanChuyenCreate) -> DonViVanChuyen:
        """
        Tạo mới một đơn vị vận chuyển trong hệ thống (Hành động từ Admin).

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            data (DonViVanChuyenCreate): Dữ liệu cấu hình đơn vị vận chuyển mới.

        Returns:
            DonViVanChuyen: Bản ghi đơn vị vận chuyển vừa được lưu.

        Raises:
            HTTPException: Lỗi 400 nếu mã đơn vị vận chuyển đã tồn tại trước đó.
        """
        existing = (
            db.query(DonViVanChuyen)
            .filter(DonViVanChuyen.ma_don_vi == data.ma_don_vi)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Ma don vi da ton tai")

        don_vi = DonViVanChuyen(**data.model_dump())
        db.add(don_vi)
        db.commit()
        db.refresh(don_vi)
        return don_vi

    @staticmethod
    async def cap_nhat_don_vi(
        db: Session, id: int, data: DonViVanChuyenUpdate
    ) -> DonViVanChuyen:
        """
        Cập nhật thông tin chi tiết hoặc trạng thái kích hoạt của đơn vị vận chuyển.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            id (int): ID định danh của đơn vị vận chuyển cần sửa đổi.
            data (DonViVanChuyenUpdate): Dữ liệu cập nhật mới.

        Returns:
            DonViVanChuyen: Đối tượng đơn vị vận chuyển sau cập nhật.

        Raises:
            HTTPException: Lỗi 404 nếu không tìm thấy đơn vị vận chuyển.
        """
        don_vi = db.query(DonViVanChuyen).filter(DonViVanChuyen.id == id).first()
        if not don_vi:
            raise HTTPException(
                status_code=404, detail="Khong tim thay don vi van chuyen"
            )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(don_vi, key, value)

        db.commit()
        db.refresh(don_vi)
        return don_vi

    @staticmethod
    async def xoa_don_vi(db: Session, id: int):
        """
        Xóa một đơn vị vận chuyển khỏi hệ thống dựa vào ID chỉ định.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            id (int): ID định danh đơn vị vận chuyển cần xóa.

        Returns:
            dict: Thông báo kết quả xóa đơn vị vận chuyển thành công.

        Raises:
            HTTPException: Lỗi 404 nếu không tìm thấy đơn vị vận chuyển.
        """
        don_vi = db.query(DonViVanChuyen).filter(DonViVanChuyen.id == id).first()
        if not don_vi:
            raise HTTPException(
                status_code=404, detail="Khong tim thay don vi van chuyen"
            )

        db.delete(don_vi)
        db.commit()
        return {"message": "Da xoa don vi van chuyen thanh cong"}
