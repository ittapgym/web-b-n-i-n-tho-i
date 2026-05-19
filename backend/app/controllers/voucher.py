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
    """Lay danh sach voucher dang hoat dong (cho khach hang)"""
    return await VoucherService.lay_danh_sach_voucher(db)


@router.get("/user/all", response_model=List[VoucherSchema])
async def lay_danh_sach_voucher_cho_user(db: Session = Depends(get_db)):
    """Lay danh sach voucher cho user (bao gom dang_hoat_dong va tam_dung)"""
    return await VoucherService.lay_danh_sach_voucher_cho_user(db)


@router.post("/check-voucher", response_model=KiemTraVoucherResponse)
async def kiem_tra_voucher(req: KiemTraVoucherRequest, db: Session = Depends(get_db)):
    """Kiem tra ma voucher co hop le khong"""
    return await VoucherService.kiem_tra_voucher(db, req.ma_voucher, req.tong_bill)


# ---- Admin APIs ----


@router.get("/admin/all", response_model=List[VoucherSchema])
async def lay_tat_ca_voucher_admin(db: Session = Depends(get_db)):
    """Admin lay tat ca voucher"""
    return await VoucherService.lay_tat_ca_voucher(db)


@router.post("/", response_model=VoucherSchema)
async def tao_voucher(data: VoucherCreate, db: Session = Depends(get_db)):
    """Admin tao voucher moi"""
    return await VoucherService.tao_voucher(db, data)


@router.put("/{id}", response_model=VoucherSchema)
async def cap_nhat_voucher(id: int, data: VoucherUpdate, db: Session = Depends(get_db)):
    """Admin cap nhat voucher"""
    return await VoucherService.cap_nhat_voucher(db, id, data)


@router.put("/{id}/status", response_model=VoucherSchema)
async def cap_nhat_trang_thai_voucher(
    id: int, req: CapNhatTrangThaiRequest, db: Session = Depends(get_db)
):
    """Admin cap nhat nhanh trang thai voucher (dang_hoat_dong / tam_dung)"""
    return await VoucherService.cap_nhat_trang_thai(db, id, req.trang_thai)


@router.delete("/{id}")
async def xoa_voucher(id: int, db: Session = Depends(get_db)):
    """Admin xoa voucher"""
    return await VoucherService.xoa_voucher(db, id)
