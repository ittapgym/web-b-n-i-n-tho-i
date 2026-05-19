from pydantic import BaseModel
from typing import Optional, List

class SanPhamBase(BaseModel):
    ten: str
    mau_sac: str
    dung_luong: Optional[str] = ""
    ram: Optional[str] = ""
    mo_ta: str
    gia: float
    hinh_anh: Optional[str] = None
    thu_vien_anh: Optional[List[str]] = []
    danh_muc: str
    is_new: Optional[int] = 1
    so_luong_kho: Optional[int] = 100

class SanPhamCreate(SanPhamBase):
    pass

class SanPhamUpdate(BaseModel):
    ten: Optional[str] = None
    mau_sac: Optional[str] = None
    dung_luong: Optional[str] = None
    ram: Optional[str] = None
    mo_ta: Optional[str] = None
    gia: Optional[float] = None
    hinh_anh: Optional[str] = None
    thu_vien_anh: Optional[List[str]] = None
    danh_muc: Optional[str] = None
    is_new: Optional[int] = None
    so_luong_kho: Optional[int] = None

class SanPhamRead(SanPhamBase):
    id: int

    class Config:
        from_attributes = True
