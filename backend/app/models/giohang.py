from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class GioHang(Base):
    __tablename__ = "gio_hang"

    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id"))
    san_pham_id = Column(Integer, ForeignKey("san_pham.id"))
    so_luong = Column(Integer, default=1)
    dung_luong = Column(String(50), default="")  # Selected storage capacity: 128GB, 256GB, etc.
    ram = Column(String(50), default="")         # Selected RAM: 8GB, 16GB, etc.
    mau_sac = Column(String(50), default="")     # Selected color: #ffffff, #000000, etc.

    # Quan he voi cac bang khac
    nguoi_dung = relationship("NguoiDung")
    san_pham = relationship("SanPham")
