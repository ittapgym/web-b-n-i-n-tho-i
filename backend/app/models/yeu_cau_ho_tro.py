from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class YeuCauHoTro(Base):
    __tablename__ = "yeu_cau_ho_tro"

    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id", ondelete="CASCADE"), nullable=False)
    chu_de = Column(String(255), nullable=False)
    imei_serial = Column(String(100), nullable=True)
    noi_dung = Column(Text, nullable=False)
    trang_thai = Column(String(50), default="cho_xu_ly")  # 'cho_xu_ly', 'dang_xu_ly', 'da_xu_ly'
    hinh_anh = Column(Text, nullable=True) # Semicolon-delimited file paths
    thoi_gian = Column(DateTime, default=datetime.utcnow)

    # Relationship to user
    nguoi_dung = relationship("NguoiDung", backref="yeu_cau_ho_tro")
