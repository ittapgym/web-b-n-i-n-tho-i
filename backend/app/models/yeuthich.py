from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class YeuThich(Base):
    __tablename__ = "yeu_thich"

    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(
        Integer, ForeignKey("nguoi_dung.id", ondelete="CASCADE"), nullable=False
    )
    san_pham_id = Column(
        Integer, ForeignKey("san_pham.id", ondelete="CASCADE"), nullable=False
    )
    ngay_tao = Column(DateTime, default=datetime.utcnow)

    # Relationships
    nguoi_dung = relationship("NguoiDung")
    san_pham = relationship("SanPham")
