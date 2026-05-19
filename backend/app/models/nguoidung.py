from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.core.database import Base

class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    mat_khau = Column(String(255), nullable=False)
    ho_ten = Column(String(100), nullable=False)
    so_dien_thoai = Column(String(20), nullable=True)
    dia_chi = Column(String(255), nullable=True)
    vai_tro = Column(String(50), default="nguoi_dung")
    trang_thai = Column(String(50), default="dang_hoat_dong")
    diem_tich_luy = Column(Integer, default=0)
    hinh_anh = Column(String(500), nullable=True)
    
    # Doanh nghiệp Info
    ten_doanh_nghiep = Column(String(255), nullable=True)
    ma_so_thue = Column(String(100), nullable=True)
    dia_chi_kd = Column(String(255), nullable=True)
    linh_vuc_kd = Column(String(100), nullable=True)
    
    ma_pin = Column(String(255), nullable=True)
    yeu_cau_pin = Column(Boolean, default=False)
    
    ngay_tao = Column(DateTime, default=datetime.utcnow)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def co_pin(self) -> bool:
        return self.ma_pin is not None and self.ma_pin != ""
