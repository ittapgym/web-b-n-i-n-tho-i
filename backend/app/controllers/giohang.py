from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.phu_thuoc import lay_nguoi_dung_hien_tai
from app.models.giohang import GioHang
from app.models.sanpham import SanPham
from app.models.nguoidung import NguoiDung
from app.schemas.giohang import GioHang as GioHangSchema, GioHangTaoMoi, GioHangCapNhat

router = APIRouter(prefix="/gio-hang", tags=["Gio Hang"])

@router.get("/", response_model=List[GioHangSchema])
def lay_gio_hang(
    db: Session = Depends(get_db), 
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """Lay danh sach san pham trong gio hang cua nguoi dung"""
    return db.query(GioHang).filter(GioHang.nguoi_dung_id == nguoi_dung.id).all()

@router.post("/them", response_model=GioHangSchema)
def them_vao_gio(
    du_lieu: GioHangTaoMoi,
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """Them san pham vao gio hang"""
    # Kiem tra san pham co ton tai khong
    san_pham = db.query(SanPham).filter(SanPham.id == du_lieu.san_pham_id).first()
    if not san_pham:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="San pham khong ton tai")
    
    # Kiem tra san pham da co trong gio hang chua (cung dung luong va mau sac)
    item_cu = db.query(GioHang).filter(
        GioHang.nguoi_dung_id == nguoi_dung.id,
        GioHang.san_pham_id == du_lieu.san_pham_id,
        GioHang.dung_luong == (du_lieu.dung_luong or ""),
        GioHang.ram == (du_lieu.ram or ""),
        GioHang.mau_sac == (du_lieu.mau_sac or "")
    ).first()
    
    if item_cu:
        # Neu da co thi tang so luong
        item_cu.so_luong += du_lieu.so_luong
        db.commit()
        db.refresh(item_cu)
        return item_cu
    
    # Neu chua co thi tao moi
    item_moi = GioHang(
        nguoi_dung_id=nguoi_dung.id,
        san_pham_id=du_lieu.san_pham_id,
        so_luong=du_lieu.so_luong,
        dung_luong=du_lieu.dung_luong or "",
        ram=du_lieu.ram or "",
        mau_sac=du_lieu.mau_sac or ""
    )
    db.add(item_moi)
    db.commit()
    db.refresh(item_moi)
    return item_moi

@router.put("/cap-nhat/{item_id}", response_model=GioHangSchema)
def cap_nhat_so_luong(
    item_id: int,
    du_lieu: GioHangCapNhat,
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """Cap nhat so luong cua mot san pham trong gio"""
    item = db.query(GioHang).filter(
        GioHang.id == item_id,
        GioHang.nguoi_dung_id == nguoi_dung.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay san pham trong gio hang")
    
    if du_lieu.so_luong <= 0:
        db.delete(item)
    else:
        item.so_luong = du_lieu.so_luong
        
    db.commit()
    if du_lieu.so_luong > 0:
        db.refresh(item)
        return item
    return None # Hoac tra ve thong bao da xoa

@router.delete("/xoa/{item_id}")
def xoa_khoi_gio(
    item_id: int,
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """Xoa san pham khoi gio hang"""
    item = db.query(GioHang).filter(
        GioHang.id == item_id,
        GioHang.nguoi_dung_id == nguoi_dung.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay san pham trong gio hang")
    
    db.delete(item)
    db.commit()
    return {"detail": "Da xoa san pham khoi gio hang"}

@router.delete("/lam-trong")
def lam_trong_gio(
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """Xoa toan bo gio hang"""
    db.query(GioHang).filter(GioHang.nguoi_dung_id == nguoi_dung.id).delete()
    db.commit()
    return {"detail": "Da lam trong gio hang"}
