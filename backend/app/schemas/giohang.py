from pydantic import BaseModel
from typing import Optional
from .sanpham import SanPhamRead

class GioHangBase(BaseModel):
    san_pham_id: int
    so_luong: int = 1
    dung_luong: Optional[str] = ""
    ram: Optional[str] = ""
    mau_sac: Optional[str] = ""

class GioHangTaoMoi(GioHangBase):
    pass

class GioHangCapNhat(BaseModel):
    so_luong: int
    dung_luong: Optional[str] = None
    ram: Optional[str] = None
    mau_sac: Optional[str] = None

class GioHang(GioHangBase):
    id: int
    nguoi_dung_id: int
    san_pham: Optional[SanPhamRead] = None

    class Config:
        from_attributes = True
