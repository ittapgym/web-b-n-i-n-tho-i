from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.core.database import Base


class SanPham(Base):
    __tablename__ = "san_pham"

    id = Column(Integer, primary_key=True, index=True)
    ten = Column(String(255), index=True)
    mau_sac = Column(String(255))  # HEX codes separated by commas: #ffffff,#000000
    dung_luong = Column(String(255), default="")  # Storage capacities separated by commas: 128GB,256GB,512GB
    ram = Column(String(255), default="")  # RAM options separated by commas: 8GB, 16GB
    mo_ta = Column(Text)
    gia = Column(Float)
    hinh_anh = Column(String(500))
    thu_vien_anh = Column(JSON, default=[]) # Luu danh sach URL anh chi tiet
    danh_muc = Column(String(100))
    is_new = Column(Integer, default=1)
    so_luong_kho = Column(Integer, default=100)
