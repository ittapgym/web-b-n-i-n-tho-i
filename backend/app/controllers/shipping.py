from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.shipping_service import ShippingService
from app.schemas.shipping import (
    DonViVanChuyenCreate,
    DonViVanChuyenUpdate,
    DonViVanChuyenSchema,
    TinhPhiShipRequest,
)

router = APIRouter(prefix="/shipping", tags=["Van chuyen"])


@router.get("/don-vi", response_model=List[DonViVanChuyenSchema])
async def lay_danh_sach_don_vi(db: Session = Depends(get_db)):
    """
    Lấy danh sách các đơn vị vận chuyển đang ở trạng thái kích hoạt hoạt động.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        List[DonViVanChuyenSchema]: Danh sách đơn vị vận chuyển khả dụng.
    """
    return await ShippingService.lay_danh_sach_don_vi(db)


@router.post("/tinh-phi")
async def tinh_phi_ship(req: TinhPhiShipRequest, db: Session = Depends(get_db)):
    """
    Tính toán chi phí vận chuyển dựa trên đơn vị được chọn và tổng giá trị hóa đơn.

    Args:
        req (TinhPhiShipRequest): Chứa mã đơn vị vận chuyển và tổng tiền hóa đơn.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Chứa thông tin số tiền phí vận chuyển được tính toán.
    """
    phi_ship = await ShippingService.tinh_phi_ship(req.ma_don_vi, req.tong_bill, db)
    return {"phi_ship": phi_ship}


# ---- Admin APIs ----


@router.get("/admin/all", response_model=List[DonViVanChuyenSchema])
async def lay_tat_ca_don_vi_admin(db: Session = Depends(get_db)):
    """
    Lấy toàn bộ các đơn vị vận chuyển trong hệ thống dành cho Admin (bao gồm cả các đơn vị không kích hoạt).

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        List[DonViVanChuyenSchema]: Danh sách đầy đủ các đơn vị vận chuyển.
    """
    return await ShippingService.lay_tat_ca_don_vi(db)


@router.post("/don-vi", response_model=DonViVanChuyenSchema)
async def tao_don_vi(data: DonViVanChuyenCreate, db: Session = Depends(get_db)):
    """
    Tạo mới một đơn vị vận chuyển mới (Hành động từ Admin).

    Args:
        data (DonViVanChuyenCreate): Thông tin chi tiết đơn vị vận chuyển mới.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        DonViVanChuyenSchema: Bản ghi đơn vị vận chuyển vừa được tạo.
    """
    return await ShippingService.tao_don_vi(db, data)


@router.put("/don-vi/{id}", response_model=DonViVanChuyenSchema)
async def cap_nhat_don_vi(
    id: int, data: DonViVanChuyenUpdate, db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin chi tiết hoặc trạng thái kích hoạt của một đơn vị vận chuyển.

    Args:
        id (int): ID định danh đơn vị vận chuyển cần sửa đổi.
        data (DonViVanChuyenUpdate): Dữ liệu cập nhật mới.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        DonViVanChuyenSchema: Đối tượng sau khi cập nhật thành công.
    """
    return await ShippingService.cap_nhat_don_vi(db, id, data)


@router.delete("/don-vi/{id}")
async def xoa_don_vi(id: int, db: Session = Depends(get_db)):
    """
    Xóa vĩnh viễn một đơn vị vận chuyển khỏi hệ thống (Hành động từ Admin).

    Args:
        id (int): ID định danh đơn vị vận chuyển cần xóa.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Trạng thái xác nhận xóa thành công.
    """
    return await ShippingService.xoa_don_vi(db, id)
