from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.core.database import Base


class DoiTacThanhToan(Base):
    __tablename__ = "doi_tac_thanh_toan"

    id = Column(Integer, primary_key=True, index=True)
    ten_doi_tac = Column(String(100), nullable=False)
    ma_phuong_thuc = Column(
        String(50), unique=True, nullable=False
    )  # COD, QR_BANK, MOMO, VNPAY
    loai_hinh = Column(String(50), nullable=False)  # COD, Chuyen_khoan, Vi_dien_tu
    mo_ta = Column(String(255), nullable=True)
    kich_hoat = Column(Boolean, default=True)

    ngay_tao = Column(DateTime, default=datetime.utcnow)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
