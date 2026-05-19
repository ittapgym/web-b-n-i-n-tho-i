from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChiTietDonHangBase(BaseModel):
    san_pham_id: int
    so_luong: int
    gia: float
    dung_luong: Optional[str] = None
    ram: Optional[str] = None
    mau_sac: Optional[str] = None


class ChiTietDonHangCreate(ChiTietDonHangBase):
    pass


class SanPhamInfo(BaseModel):
    ten: str
    hinh_anh: Optional[str] = None


class ChiTietDonHangSchema(ChiTietDonHangBase):
    id: int
    don_hang_id: int
    san_pham: Optional[SanPhamInfo] = None

    class Config:
        from_attributes = True


class DonHangBase(BaseModel):
    ten_khach_hang: str
    so_dien_thoai: str
    dia_chi: str
    ghi_chu: Optional[str] = None
    tong_tien: float


class DonHangCreate(DonHangBase):
    items: List[ChiTietDonHangCreate]
    phuong_thuc_thanh_toan: Optional[str] = None
    phuong_thuc_van_chuyen: Optional[str] = None
    ma_voucher: Optional[str] = None
    ma_pin: Optional[str] = None


class DonHangUpdateStatus(BaseModel):
    trang_thai: str


class DonHangSchema(DonHangBase):
    id: int
    user_id: Optional[int]
    trang_thai: str
    phuong_thuc_thanh_toan: Optional[str] = None
    phuong_thuc_van_chuyen: Optional[str] = None
    phi_ship: float = 0
    giam_gia_voucher: float = 0
    voucher_id: Optional[int] = None
    imei: Optional[str] = None
    warranty_months: Optional[int] = None
    ngay_tao: datetime
    items: List[ChiTietDonHangSchema]

    class Config:
        from_attributes = True
