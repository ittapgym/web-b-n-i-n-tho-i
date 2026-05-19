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
    """Lay danh sach doi tac thanh toan dang kich hoat"""
    return await PaymentService.lay_danh_sach_doi_tac(db)


# ---- Admin APIs ----


@router.get("/admin/all", response_model=List[DoiTacThanhToanSchema])
async def lay_tat_ca_doi_tac_admin(db: Session = Depends(get_db)):
    """Admin lay tat ca doi tac thanh toan"""
    return await PaymentService.lay_tat_ca_doi_tac(db)


@router.post("/doi-tac", response_model=DoiTacThanhToanSchema)
async def tao_doi_tac(data: DoiTacThanhToanCreate, db: Session = Depends(get_db)):
    """Admin them doi tac thanh toan"""
    return await PaymentService.tao_doi_tac(db, data)


@router.put("/doi-tac/{id}", response_model=DoiTacThanhToanSchema)
async def cap_nhat_doi_tac(
    id: int, data: DoiTacThanhToanUpdate, db: Session = Depends(get_db)
):
    """Admin cap nhat doi tac thanh toan"""
    return await PaymentService.cap_nhat_doi_tac(db, id, data)


@router.delete("/doi-tac/{id}")
async def xoa_doi_tac(id: int, db: Session = Depends(get_db)):
    """Admin xoa doi tac thanh toan"""
    return await PaymentService.xoa_doi_tac(db, id)


@router.get("/so-du")
async def kiem_tra_so_du_doi_tac():
    """Admin kiem tra so du tu cac doi tac"""
    return await PaymentService.kiem_tra_so_du_doi_tac()
