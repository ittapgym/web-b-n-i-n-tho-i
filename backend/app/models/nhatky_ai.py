from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base

class NhatKyChatAI(Base):
    __tablename__ = "nhat_ky_chat_ai"

    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(Integer, nullable=True)
    email_nguoi_dung = Column(String(255), nullable=True)
    cau_hoi = Column(Text, nullable=False)
    tra_loi = Column(Text, nullable=False)
    thoi_gian = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(50), nullable=True)
