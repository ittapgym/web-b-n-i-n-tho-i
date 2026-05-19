from sqlalchemy.orm import Session
from typing import List
from app.models.doi_tac_thanh_toan import DoiTacThanhToan
from app.schemas.payment import DoiTacThanhToanCreate, DoiTacThanhToanUpdate
from fastapi import HTTPException


class PaymentService:
    @staticmethod
    async def lay_danh_sach_doi_tac(db: Session) -> List[DoiTacThanhToan]:
        """Tra ve cac phuong thuc thanh toan dang kich hoat"""
        return db.query(DoiTacThanhToan).filter(DoiTacThanhToan.kich_hoat.is_(True)).all()

    @staticmethod
    async def lay_tat_ca_doi_tac(db: Session) -> List[DoiTacThanhToan]:
        """Lay tat ca doi tac thanh toan (cho Admin)"""
        return db.query(DoiTacThanhToan).all()

    @staticmethod
    async def tao_doi_tac(db: Session, data: DoiTacThanhToanCreate) -> DoiTacThanhToan:
        """Admin them doi tac thanh toan moi"""
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
        """Admin cap nhat doi tac thanh toan"""
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
        """Admin xoa doi tac thanh toan"""
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
        """Danh cho Admin theo doi dong tien ve tu doi tac (placeholder)"""
        # Trong thuc te, se goi API cua MoMo/VNPay de lay so du
        return {
            "COD": {"so_du": 0, "don_vi": "VNĐ"},
            "QR_Bank": {"so_du": 0, "don_vi": "VNĐ"},
            "MOMO": {"so_du": 0, "don_vi": "VNĐ"},
            "VNPAY": {"so_du": 0, "don_vi": "VNĐ"},
        }
