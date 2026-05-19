from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DonViVanChuyenBase(BaseModel):
    ten_don_vi: str
    ma_don_vi: str
    phi_co_dinh: float = 0
    nguong_mien_phi: float = 0
    thoi_gian_du_kien: str = "2-3 ngay"
    mo_ta: Optional[str] = None
    kich_hoat: bool = True


class DonViVanChuyenCreate(DonViVanChuyenBase):
    pass


class DonViVanChuyenUpdate(BaseModel):
    ten_don_vi: Optional[str] = None
    ma_don_vi: Optional[str] = None
    phi_co_dinh: Optional[float] = None
    nguong_mien_phi: Optional[float] = None
    thoi_gian_du_kien: Optional[str] = None
    mo_ta: Optional[str] = None
    kich_hoat: Optional[bool] = None


class DonViVanChuyenSchema(DonViVanChuyenBase):
    id: int
    ngay_tao: datetime
    ngay_cap_nhat: datetime

    class Config:
        from_attributes = True


class TinhPhiShipRequest(BaseModel):
    ma_don_vi: str
    tong_bill: float
