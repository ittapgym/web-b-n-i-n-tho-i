from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Schema co ban cho Nguoi Dung
class NguoiDungBase(BaseModel):
    email: EmailStr
    ho_ten: str
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None
    hinh_anh: Optional[str] = None

# Schema khi Dang Ky (can mat khau)
class DangKyNguoiDung(NguoiDungBase):
    mat_khau: str

# Schema khi Dang Nhap
class DangNhapNguoiDung(BaseModel):
    email: EmailStr
    mat_khau: str

# Schema tra ve thong tin (khong tra ve mat khau)
class ThongTinNguoiDung(NguoiDungBase):
    id: int
    vai_tro: str
    trang_thai: str
    diem_tich_luy: int
    ngay_tao: datetime
    yeu_cau_pin: bool = False
    co_pin: bool = False
    
    # Doanh nghiệp Info
    ten_doanh_nghiep: Optional[str] = None
    ma_so_thue: Optional[str] = None
    dia_chi_kd: Optional[str] = None
    linh_vuc_kd: Optional[str] = None

    class Config:
        from_attributes = True

# Schema tra ve Token khi dang nhap thanh cong
class Token(BaseModel):
    access_token: str
    token_type: str
