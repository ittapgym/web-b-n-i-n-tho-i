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
    """Lay danh sach don vi van chuyen dang kich hoat"""
    return await ShippingService.lay_danh_sach_don_vi(db)


@router.post("/tinh-phi")
async def tinh_phi_ship(req: TinhPhiShipRequest, db: Session = Depends(get_db)):
    """Tinh phi van chuyen"""
    phi_ship = await ShippingService.tinh_phi_ship(req.ma_don_vi, req.tong_bill, db)
    return {"phi_ship": phi_ship}


# ---- Admin APIs ----


@router.get("/admin/all", response_model=List[DonViVanChuyenSchema])
async def lay_tat_ca_don_vi_admin(db: Session = Depends(get_db)):
    """Admin lay tat ca don vi van chuyen"""
    return await ShippingService.lay_tat_ca_don_vi(db)


@router.post("/don-vi", response_model=DonViVanChuyenSchema)
async def tao_don_vi(data: DonViVanChuyenCreate, db: Session = Depends(get_db)):
    """Admin them don vi van chuyen"""
    return await ShippingService.tao_don_vi(db, data)


@router.put("/don-vi/{id}", response_model=DonViVanChuyenSchema)
async def cap_nhat_don_vi(
    id: int, data: DonViVanChuyenUpdate, db: Session = Depends(get_db)
):
    """Admin cap nhat don vi van chuyen"""
    return await ShippingService.cap_nhat_don_vi(db, id, data)


@router.delete("/don-vi/{id}")
async def xoa_don_vi(id: int, db: Session = Depends(get_db)):
    """Admin xoa don vi van chuyen"""
    return await ShippingService.xoa_don_vi(db, id)
