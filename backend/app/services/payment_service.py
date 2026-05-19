from sqlalchemy.orm import Session
from typing import List
from app.models.doi_tac_thanh_toan import DoiTacThanhToan
from app.schemas.payment import DoiTacThanhToanCreate, DoiTacThanhToanUpdate
from fastapi import HTTPException


class PaymentService:
    @staticmethod
    async def lay_danh_sach_doi_tac(db: Session) -> List[DoiTacThanhToan]:
        """
        Lấy danh sách các đối tác/phương thức thanh toán đang kích hoạt hoạt động.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

        Returns:
            List[DoiTacThanhToan]: Danh sách đối tác thanh toán đang kích hoạt.
        """
        return db.query(DoiTacThanhToan).filter(DoiTacThanhToan.kich_hoat.is_(True)).all()

    @staticmethod
    async def lay_tat_ca_doi_tac(db: Session) -> List[DoiTacThanhToan]:
        """
        Lấy toàn bộ các đối tác/phương thức thanh toán trong hệ thống dành cho Admin quản trị.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

        Returns:
            List[DoiTacThanhToan]: Danh sách đầy đủ đối tác thanh toán.
        """
        return db.query(DoiTacThanhToan).all()

    @staticmethod
    async def tao_doi_tac(db: Session, data: DoiTacThanhToanCreate) -> DoiTacThanhToan:
        """
        Tạo mới một đối tác thanh toán. Kiểm tra xem mã phương thức thanh toán đã tồn tại chưa.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            data (DoiTacThanhToanCreate): Dữ liệu đối tác mới cần thêm.

        Returns:
            DoiTacThanhToan: Bản ghi đối tác vừa tạo.

        Raises:
            HTTPException: Lỗi 400 nếu mã phương thức thanh toán đã tồn tại.
        """
        existing = (
            db.query(DoiTacThanhToan)
            .filter(DoiTacThanhToan.ma_phuong_thuc == data.ma_phuong_thuc)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Ma phuong thuc da ton tai")

        doi_tac = DoiTacThanhToan(**data.model_dump())
        db.add(doi_tac)
        db.commit()
        db.refresh(doi_tac)
        return doi_tac

    @staticmethod
    async def cap_nhat_doi_tac(
        db: Session, id: int, data: DoiTacThanhToanUpdate
    ) -> DoiTacThanhToan:
        """
        Cập nhật thông tin chi tiết của đối tác thanh toán theo ID chỉ định.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            id (int): ID của đối tác cần cập nhật.
            data (DoiTacThanhToanUpdate): Dữ liệu cập nhật mới.

        Returns:
            DoiTacThanhToan: Bản ghi đối tác sau khi cập nhật thành công.

        Raises:
            HTTPException: Lỗi 404 nếu không tìm thấy đối tác thanh toán.
        """
        doi_tac = db.query(DoiTacThanhToan).filter(DoiTacThanhToan.id == id).first()
        if not doi_tac:
            raise HTTPException(
                status_code=404, detail="Khong tim thay doi tac thanh toan"
            )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(doi_tac, key, value)

        db.commit()
        db.refresh(doi_tac)
        return doi_tac

    @staticmethod
    async def xoa_doi_tac(db: Session, id: int):
        """
        Xóa đối tác thanh toán khỏi hệ thống theo ID chỉ định.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            id (int): ID của đối tác cần xóa.

        Returns:
            dict: Thông báo xóa đối tác thành công.

        Raises:
            HTTPException: Lỗi 404 nếu không tìm thấy đối tác thanh toán.
        """
        doi_tac = db.query(DoiTacThanhToan).filter(DoiTacThanhToan.id == id).first()
        if not doi_tac:
            raise HTTPException(
                status_code=404, detail="Khong tim thay doi tac thanh toan"
            )

        db.delete(doi_tac)
        db.commit()
        return {"message": "Da xoa doi tac thanh toan thanh cong"}

    @staticmethod
    async def kiem_tra_so_du_doi_tac():
        """
        Kiểm tra số dư từ các cổng đối tác thanh toán như MoMo, VNPay (Hàm giả lập/Placeholder).

        Returns:
            dict: Thông tin số dư giả lập của từng cổng thanh toán.
        """
        # Trong thuc te, se goi API cua MoMo/VNPay de lay so du
        return {
            "COD": {"so_du": 0, "don_vi": "VNĐ"},
            "QR_Bank": {"so_du": 0, "don_vi": "VNĐ"},
            "MOMO": {"so_du": 0, "don_vi": "VNĐ"},
            "VNPAY": {"so_du": 0, "don_vi": "VNĐ"},
        }
