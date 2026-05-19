from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class YeuCauDoanhNghiep(Base):
    __tablename__ = "yeu_cau_doanh_nghiep"

    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id", ondelete="CASCADE"), nullable=False)
    ten_doanh_nghiep = Column(String(255), nullable=False)
    ma_so_thue = Column(String(100), nullable=False)
    dia_chi_kd = Column(String(255), nullable=False)
    linh_vuc_kd = Column(String(100), nullable=False)
    trang_thai = Column(String(50), default="cho_duyet")  # 'cho_duyet', 'da_duyet', 'tu_choi'
    ngay_tao = Column(DateTime, default=datetime.utcnow)
    ngay_duyet = Column(DateTime, nullable=True)

    # Relationship to user
    nguoi_dung = relationship("NguoiDung", backref="yeu_cau_doanh_nghiep")
