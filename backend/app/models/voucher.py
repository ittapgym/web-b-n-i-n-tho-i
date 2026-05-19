from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from app.core.database import Base


class Voucher(Base):
    __tablename__ = "voucher"

    id = Column(Integer, primary_key=True, index=True)
    ma_voucher = Column(String(50), unique=True, index=True, nullable=False)
    loai_giam_gia = Column(String(20), nullable=False)  # 'phan_tram' hoac 'so_tien'
    gia_tri_giam = Column(Float, nullable=False)
    don_hang_toi_thieu = Column(Float, default=0)
    giam_toi_da = Column(Float, nullable=True)
    ngay_het_han = Column(DateTime, nullable=False)
    so_luong_con_lai = Column(Integer, default=0)
    trang_thai = Column(
        String(20), default="dang_hoat_dong"
    )  # dang_hoat_dong, tam_dung, het_han, da_huy

    ngay_tao = Column(DateTime, default=datetime.utcnow)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
