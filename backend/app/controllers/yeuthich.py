from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.phu_thuoc import lay_nguoi_dung_hien_tai
from app.models.yeuthich import YeuThich
from app.models.sanpham import SanPham
from app.models.nguoidung import NguoiDung
from app.schemas.sanpham import SanPhamRead

router = APIRouter(prefix="/yeu-thich", tags=["Yeu Thich"])

@router.get("/", response_model=List[SanPhamRead])
def lay_danh_sach_yeu_thich(
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """
    Lấy danh sách tất cả các sản phẩm mà người dùng hiện tại đã nhấn yêu thích (Like).

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
        nguoi_dung (NguoiDung): Đối tượng người dùng đang đăng nhập.

    Returns:
        List[SanPhamRead]: Danh sách thông tin các sản phẩm được yêu thích.
    """
    favorites = db.query(YeuThich).filter(YeuThich.nguoi_dung_id == nguoi_dung.id).all()
    # Trả về đối tượng sản phẩm lồng ghép bên trong mỗi bản ghi yêu thích
    return [fav.san_pham for fav in favorites if fav.san_pham]

@router.post("/toggle/{san_pham_id}")
def toggle_yeu_thich(
    san_pham_id: int,
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """
    Chuyển đổi trạng thái yêu thích của sản phẩm (nếu chưa thích thì thêm vào, nếu đã thích thì xóa đi).

    Args:
        san_pham_id (int): ID của sản phẩm cần chuyển đổi trạng thái yêu thích.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
        nguoi_dung (NguoiDung): Đối tượng người dùng đang đăng nhập.

    Returns:
        dict: Kết quả trạng thái thao tác ('da_them' hoặc 'da_xoa') kèm theo chi tiết.

    Raises:
        HTTPException: Lỗi 404 nếu sản phẩm không tồn tại trong hệ thống.
    """
    # Kiểm tra sản phẩm có tồn tại hay không
    san_pham = db.query(SanPham).filter(SanPham.id == san_pham_id).first()
    if not san_pham:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sản phẩm không tồn tại"
        )
    
    # Kiểm tra sản phẩm đã được yêu thích chưa
    fav = db.query(YeuThich).filter(
        YeuThich.nguoi_dung_id == nguoi_dung.id,
        YeuThich.san_pham_id == san_pham_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()
        return {"status": "da_xoa", "detail": "Đã xóa sản phẩm khỏi danh sách yêu thích"}
    else:
        new_fav = YeuThich(nguoi_dung_id=nguoi_dung.id, san_pham_id=san_pham_id)
        db.add(new_fav)
        db.commit()
        return {"status": "da_them", "detail": "Đã thêm sản phẩm vào danh sách yêu thích"}

@router.get("/check/{san_pham_id}")
def kiem_tra_yeu_thich(
    san_pham_id: int,
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """
    Kiểm tra nhanh xem sản phẩm cụ thể đã được người dùng này nhấn yêu thích hay chưa.

    Args:
        san_pham_id (int): ID của sản phẩm cần kiểm tra.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
        nguoi_dung (NguoiDung): Đối tượng người dùng đang đăng nhập.

    Returns:
        dict: Chứa trường boolean `is_favorite` thể hiện kết quả kiểm tra.
    """
    fav = db.query(YeuThich).filter(
        YeuThich.nguoi_dung_id == nguoi_dung.id,
        YeuThich.san_pham_id == san_pham_id
    ).first()
    return {"is_favorite": fav is not None}
