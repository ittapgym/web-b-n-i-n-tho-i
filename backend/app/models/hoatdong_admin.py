from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class HoatDongAdmin(Base):
    __tablename__ = "hoat_dong_admin"

    id = Column(Integer, primary_key=True, index=True)
    nhan_vien = Column(String(255), default="Admin")
    thao_tac = Column(String(500), nullable=False)
    thoi_gian = Column(DateTime, default=datetime.utcnow)
