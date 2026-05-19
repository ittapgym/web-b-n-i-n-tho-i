from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from app.core.database import Base


class DonViVanChuyen(Base):
    __tablename__ = "don_vi_van_chuyen"

    id = Column(Integer, primary_key=True, index=True)
    ten_don_vi = Column(String(100), nullable=False)
    ma_don_vi = Column(String(50), unique=True, nullable=False)  # GIAO_NHANH, TIET_KIEM
    phi_co_dinh = Column(Float, default=0)
    nguong_mien_phi = Column(Float, default=0)
    thoi_gian_du_kien = Column(String(50), default="2-3 ngay")
    mo_ta = Column(String(255), nullable=True)
    kich_hoat = Column(Boolean, default=True)

    ngay_tao = Column(DateTime, default=datetime.utcnow)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
