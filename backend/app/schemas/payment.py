from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DoiTacThanhToanBase(BaseModel):
    ten_doi_tac: str
    ma_phuong_thuc: str
    loai_hinh: str  # COD, Chuyen_khoan, Vi_dien_tu
    mo_ta: Optional[str] = None
    kich_hoat: bool = True


class DoiTacThanhToanCreate(DoiTacThanhToanBase):
    pass


class DoiTacThanhToanUpdate(BaseModel):
    ten_doi_tac: Optional[str] = None
    ma_phuong_thuc: Optional[str] = None
    loai_hinh: Optional[str] = None
    mo_ta: Optional[str] = None
    kich_hoat: Optional[bool] = None


class DoiTacThanhToanSchema(DoiTacThanhToanBase):
    id: int
    ngay_tao: datetime
    ngay_cap_nhat: datetime

    class Config:
        from_attributes = True
