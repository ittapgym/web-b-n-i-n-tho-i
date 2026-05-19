from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VoucherBase(BaseModel):
    ma_voucher: str
    loai_giam_gia: str  # 'phan_tram' or 'so_tien'
    gia_tri_giam: float
    don_hang_toi_thieu: float = 0
    giam_toi_da: Optional[float] = None
    ngay_het_han: datetime
    so_luong_con_lai: int = 0
    trang_thai: str = "dang_hoat_dong"


class VoucherCreate(VoucherBase):
    pass


class VoucherUpdate(BaseModel):
    ma_voucher: Optional[str] = None
    loai_giam_gia: Optional[str] = None
    gia_tri_giam: Optional[float] = None
    don_hang_toi_thieu: Optional[float] = None
    giam_toi_da: Optional[float] = None
    ngay_het_han: Optional[datetime] = None
    so_luong_con_lai: Optional[int] = None
    trang_thai: Optional[str] = None


class VoucherSchema(VoucherBase):
    id: int
    ngay_tao: datetime
    ngay_cap_nhat: datetime

    class Config:
        from_attributes = True


class KiemTraVoucherRequest(BaseModel):
    ma_voucher: str
    tong_bill: float


class KiemTraVoucherResponse(BaseModel):
    hop_le: bool
    loi: Optional[str] = None
    ma_voucher: Optional[str] = None
    loai_giam_gia: Optional[str] = None
    gia_tri_giam: Optional[float] = None
    giam_toi_da: Optional[float] = None
    so_tien_giam: Optional[float] = None
