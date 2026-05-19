from sqlalchemy.orm import Session
from typing import List
from app.models.don_vi_van_chuyen import DonViVanChuyen
from app.schemas.shipping import DonViVanChuyenCreate, DonViVanChuyenUpdate
from fastapi import HTTPException


class ShippingService:
    @staticmethod
    async def lay_danh_sach_don_vi(db: Session) -> List[DonViVanChuyen]:
        """Tra ve cac phuong thuc van chuyen co san"""
        return db.query(DonViVanChuyen).filter(DonViVanChuyen.kich_hoat.is_(True)).all()

    @staticmethod
    async def lay_tat_ca_don_vi(db: Session) -> List[DonViVanChuyen]:
        """Lay tat ca don vi van chuyen (cho Admin)"""
        return db.query(DonViVanChuyen).all()

    @staticmethod
    async def tinh_phi_ship(ma_don_vi: str, tong_bill: float, db: Session) -> float:
        """Tinh phi ship dua tren don vi van chuyen va tong bill"""
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
        """Admin them don vi van chuyen moi"""
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
        """Admin cap nhat don vi van chuyen"""
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
        """Admin xoa don vi van chuyen"""
        don_vi = db.query(DonViVanChuyen).filter(DonViVanChuyen.id == id).first()
        if not don_vi:
            raise HTTPException(
                status_code=404, detail="Khong tim thay don vi van chuyen"
            )

        db.delete(don_vi)
        db.commit()
        return {"message": "Da xoa don vi van chuyen thanh cong"}
