from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class DonHang(Base):
    __tablename__ = "don_hang"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=True)
    ten_khach_hang = Column(String(100), nullable=False)
    so_dien_thoai = Column(String(20), nullable=False)
    dia_chi = Column(String(255), nullable=False)
    ghi_chu = Column(String(500), nullable=True)
    tong_tien = Column(Float, nullable=False)
    trang_thai = Column(
        String(50), default="cho_duyet"
    )  # cho_duyet, da_duyet, dang_giao, hoan_thanh, da_huy
    is_visible_user = Column(Boolean, default=True)
    imei = Column(String(50), nullable=True)
    warranty_months = Column(Integer, nullable=True)
    ngay_hoan_thanh = Column(DateTime, nullable=True)

    # Cac truong bo sung cho he thong dat hang
    phuong_thuc_thanh_toan = Column(
        String(50), nullable=True
    )  # COD, QR_BANK, MOMO, VNPAY
    phuong_thuc_van_chuyen = Column(String(50), nullable=True)  # GIAO_NHANH, TIET_KIEM
    phi_ship = Column(Float, default=0)
    giam_gia_voucher = Column(Float, default=0)
    voucher_id = Column(Integer, ForeignKey("voucher.id"), nullable=True)

    ngay_tao = Column(DateTime, default=datetime.utcnow)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("ChiTietDonHang", back_populates="don_hang")
    voucher = relationship("Voucher", lazy="joined")


class ChiTietDonHang(Base):
    __tablename__ = "chi_tiet_don_hang"

    id = Column(Integer, primary_key=True, index=True)
    don_hang_id = Column(Integer, ForeignKey("don_hang.id"))
    san_pham_id = Column(Integer, ForeignKey("san_pham.id"))
    so_luong = Column(Integer, nullable=False)
    gia = Column(Float, nullable=False)
    dung_luong = Column(String(50), nullable=True)
    ram = Column(String(50), nullable=True)
    mau_sac = Column(String(50), nullable=True)

    don_hang = relationship("DonHang", back_populates="items")
    san_pham = relationship("SanPham")
