from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.payment_service import PaymentService
from app.schemas.payment import (
    DoiTacThanhToanCreate,
    DoiTacThanhToanUpdate,
    DoiTacThanhToanSchema,
)

router = APIRouter(prefix="/payment", tags=["Thanh toan"])


@router.get("/doi-tac", response_model=List[DoiTacThanhToanSchema])
async def lay_danh_sach_doi_tac(db: Session = Depends(get_db)):
    """
    Lấy danh sách các đối tác thanh toán đang ở trạng thái kích hoạt hoạt động.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        List[DoiTacThanhToanSchema]: Danh sách đối tác thanh toán hoạt động.
    """
    return await PaymentService.lay_danh_sach_doi_tac(db)


# ---- Admin APIs ----


@router.get("/admin/all", response_model=List[DoiTacThanhToanSchema])
async def lay_tat_ca_doi_tac_admin(db: Session = Depends(get_db)):
    """
    Lấy toàn bộ danh sách đối tác thanh toán trong hệ thống dành cho Admin (bao gồm cả đối tác bị vô hiệu hóa).

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        List[DoiTacThanhToanSchema]: Toàn bộ đối tác thanh toán trong hệ thống.
    """
    return await PaymentService.lay_tat_ca_doi_tac(db)


@router.post("/doi-tac", response_model=DoiTacThanhToanSchema)
async def tao_doi_tac(data: DoiTacThanhToanCreate, db: Session = Depends(get_db)):
    """
    Tạo mới một đối tác hoặc phương thức thanh toán mới (Hành động từ Admin).

    Args:
        data (DoiTacThanhToanCreate): Thông tin chi tiết đối tác thanh toán mới.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        DoiTacThanhToanSchema: Đối tượng đối tác thanh toán vừa tạo thành công.
    """
    return await PaymentService.tao_doi_tac(db, data)


@router.put("/doi-tac/{id}", response_model=DoiTacThanhToanSchema)
async def cap_nhat_doi_tac(
    id: int, data: DoiTacThanhToanUpdate, db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin chi tiết hoặc trạng thái kích hoạt của đối tác thanh toán.

    Args:
        id (int): ID định danh đối tác thanh toán cần sửa đổi.
        data (DoiTacThanhToanUpdate): Dữ liệu cập nhật mới.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        DoiTacThanhToanSchema: Đối tượng đối tác thanh toán sau khi lưu cập nhật.
    """
    return await PaymentService.cap_nhat_doi_tac(db, id, data)


@router.delete("/doi-tac/{id}")
async def xoa_doi_tac(id: int, db: Session = Depends(get_db)):
    """
    Xóa vĩnh viễn một đối tác thanh toán khỏi hệ thống (Hành động từ Admin).

    Args:
        id (int): ID định danh đối tác thanh toán cần xóa.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Kết quả trạng thái xóa thành công.
    """
    return await PaymentService.xoa_doi_tac(db, id)


@router.get("/so-du")
async def kiem_tra_so_du_doi_tac():
    """
    Kiểm tra số dư tiền mặt hoặc tài khoản trực tiếp từ các cổng đối tác thanh toán liên kết.

    Returns:
        dict: Danh sách số dư chi tiết của các cổng thanh toán.
    """
    return await PaymentService.kiem_tra_so_du_doi_tac()
