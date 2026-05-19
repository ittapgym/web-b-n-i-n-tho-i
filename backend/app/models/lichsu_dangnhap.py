from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class LichSuDangNhap(Base):
    __tablename__ = "lich_su_dang_nhap"

    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id", ondelete="CASCADE"), nullable=False)
    thiet_bi = Column(String(255), nullable=False)
    ip_address = Column(String(50), nullable=False)
    vi_tri = Column(String(100), nullable=True)
    ngay_dang_nhap = Column(DateTime, default=datetime.utcnow)

    # Relationship to user
    nguoi_dung = relationship("NguoiDung", backref="lich_su_dang_nhap")
