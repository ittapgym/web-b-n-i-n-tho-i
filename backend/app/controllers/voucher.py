from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.voucher_service import VoucherService
from app.schemas.voucher import (
    VoucherCreate,
    VoucherUpdate,
    VoucherSchema,
    KiemTraVoucherRequest,
    KiemTraVoucherResponse,
)
from pydantic import BaseModel

router = APIRouter(prefix="/vouchers", tags=["Voucher"])


class CapNhatTrangThaiRequest(BaseModel):
    trang_thai: str


@router.get("/", response_model=List[VoucherSchema])
async def lay_danh_sach_voucher(db: Session = Depends(get_db)):
    """
    Lấy danh sách các mã giảm giá (voucher) đang ở trạng thái kích hoạt hoạt động cho người dùng xem.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        List[VoucherSchema]: Danh sách voucher khả dụng.
    """
    return await VoucherService.lay_danh_sach_voucher(db)


@router.get("/user/all", response_model=List[VoucherSchema])
async def lay_danh_sach_voucher_cho_user(db: Session = Depends(get_db)):
    """
    Lấy danh sách các voucher dành cho phía client (bao gồm cả mã hoạt động hoặc tạm dừng).

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        List[VoucherSchema]: Danh sách voucher hiển thị ở giao diện khách hàng.
    """
    return await VoucherService.lay_danh_sach_voucher_cho_user(db)


@router.post("/check-voucher", response_model=KiemTraVoucherResponse)
async def kiem_tra_voucher(req: KiemTraVoucherRequest, db: Session = Depends(get_db)):
    """
    Kiểm tra tính hợp lệ và tính số tiền giảm giá được áp dụng dựa trên mã voucher và tổng bill.

    Args:
        req (KiemTraVoucherRequest): Chứa mã code voucher và tổng giá trị đơn hàng.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        KiemTraVoucherResponse: Kết quả hợp lệ hay không, kèm theo giá trị giảm cụ thể.
    """
    return await VoucherService.kiem_tra_voucher(db, req.ma_voucher, req.tong_bill)


# ---- Admin APIs ----


@router.get("/admin/all", response_model=List[VoucherSchema])
async def lay_tat_ca_voucher_admin(db: Session = Depends(get_db)):
    """
    Lấy toàn bộ tất cả voucher trong hệ thống dành cho Admin.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        List[VoucherSchema]: Danh sách toàn bộ voucher.
    """
    return await VoucherService.lay_tat_ca_voucher(db)


@router.post("/", response_model=VoucherSchema)
async def tao_voucher(data: VoucherCreate, db: Session = Depends(get_db)):
    """
    Tạo mới một mã giảm giá (voucher) mới trong hệ thống (Hành động từ Admin).

    Args:
        data (VoucherCreate): Thông tin cấu hình voucher mới (mã, loại giảm giá, giá trị, hạn mức...).
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        VoucherSchema: Thông tin chi tiết voucher vừa tạo.
    """
    return await VoucherService.tao_voucher(db, data)


@router.put("/{id}", response_model=VoucherSchema)
async def cap_nhat_voucher(id: int, data: VoucherUpdate, db: Session = Depends(get_db)):
    """
    Cập nhật toàn bộ thông tin cấu hình của voucher cụ thể.

    Args:
        id (int): ID định danh voucher cần sửa đổi.
        data (VoucherUpdate): Dữ liệu cập nhật mới.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        VoucherSchema: Đối tượng voucher sau khi cập nhật thành công.
    """
    return await VoucherService.cap_nhat_voucher(db, id, data)


@router.put("/{id}/status", response_model=VoucherSchema)
async def cap_nhat_trang_thai_voucher(
    id: int, req: CapNhatTrangThaiRequest, db: Session = Depends(get_db)
):
    """
    Cập nhật nhanh trạng thái bật/tắt (hoạt động / tạm dừng) của một voucher.

    Args:
        id (int): ID định danh voucher cần đổi trạng thái.
        req (CapNhatTrangThaiRequest): Trạng thái mới (dang_hoat_dong hoặc tam_dung).
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        VoucherSchema: Đối tượng sau cập nhật trạng thái.
    """
    return await VoucherService.cap_nhat_trang_thai(db, id, req.trang_thai)


@router.delete("/{id}")
async def xoa_voucher(id: int, db: Session = Depends(get_db)):
    """
    Xóa vĩnh viễn một voucher khỏi cơ sở dữ liệu hệ thống (Hành động từ Admin).

    Args:
        id (int): ID định danh voucher cần xóa bỏ hoàn toàn.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Trạng thái kết quả xóa voucher thành công.
    """
    return await VoucherService.xoa_voucher(db, id)
