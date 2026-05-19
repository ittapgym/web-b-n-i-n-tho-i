from sqlalchemy import Column, Integer, String, Float, Text
from app.core.database import Base

class CauHinhLoyalty(Base):
    __tablename__ = "cau_hinh_loyalty"

    id = Column(Integer, primary_key=True, index=True)
    ten_hang = Column(String(50), unique=True, nullable=False) # 'Silver', 'Gold', 'Diamond'
    diem_toi_thieu = Column(Integer, nullable=False, default=0)
    phan_tram_giam = Column(Float, nullable=False, default=0.0) # e.g. 5.0 for 5%
    uu_dai_rieng = Column(Text, nullable=True) # Semicolon separated privileges
    color = Column(String(7), nullable=False, default="#8e8e93")
