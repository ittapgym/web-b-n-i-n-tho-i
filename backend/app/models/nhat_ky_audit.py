from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class NhatKyAudit(Base):
    __tablename__ = "nhat_ky_audit"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    user_email = Column(String(255), nullable=True)
    hanh_dong = Column(String(500), nullable=False)
    ip_address = Column(String(50), nullable=True)
    thoi_gian = Column(DateTime, default=datetime.utcnow)
