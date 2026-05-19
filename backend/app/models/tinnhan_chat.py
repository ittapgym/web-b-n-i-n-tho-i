from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class TinNhanChat(Base):
    __tablename__ = "tin_nhan_chat"

    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id", ondelete="CASCADE"), nullable=False)
    nguoi_gui = Column(String(50), nullable=False) # 'user' or 'admin'
    noi_dung = Column(Text, nullable=False)
    thoi_gian = Column(DateTime, default=datetime.utcnow)

    # Relationship to user
    nguoi_dung = relationship("NguoiDung", backref="tin_nhan_chat")
