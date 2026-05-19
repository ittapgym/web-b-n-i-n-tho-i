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
    """
    Lấy danh sách các sản phẩm đang có trong giỏ hàng của người dùng hiện tại.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
        nguoi_dung (NguoiDung): Người dùng hiện tại đang đăng nhập.

    Returns:
        List[GioHang]: Danh sách các bản ghi giỏ hàng.
    """
    return db.query(GioHang).filter(GioHang.nguoi_dung_id == nguoi_dung.id).all()

@router.post("/them", response_model=GioHangSchema)
def them_vao_gio(
    du_lieu: GioHangTaoMoi,
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """
    Thêm mới một mặt hàng hoặc tăng số lượng của mặt hàng sẵn có trong giỏ hàng.
    Kiểm tra tính trùng khớp về màu sắc, dung lượng và RAM để gộp dòng nếu cần.

    Args:
        du_lieu (GioHangTaoMoi): Thông tin mặt hàng cần thêm (ID sản phẩm, số lượng, RAM, dung lượng, màu sắc).
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
        nguoi_dung (NguoiDung): Người dùng hiện tại đang đăng nhập.

    Returns:
        GioHang: Bản ghi giỏ hàng vừa được thêm hoặc cập nhật.

    Raises:
        HTTPException: Lỗi 404 nếu sản phẩm không tồn tại trong kho hàng.
    """
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
    """
    Cập nhật số lượng của một mặt hàng cụ thể trong giỏ hàng.
    Nếu số lượng mới nhỏ hơn hoặc bằng 0, mặt hàng sẽ bị xóa hoàn toàn khỏi giỏ.

    Args:
        item_id (int): ID của bản ghi giỏ hàng cần sửa.
        du_lieu (GioHangCapNhat): Số lượng sản phẩm mới cần đặt.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
        nguoi_dung (NguoiDung): Người dùng hiện tại đang đăng nhập.

    Returns:
        GioHang: Bản ghi giỏ hàng sau cập nhật, hoặc None nếu bản ghi bị xóa.

    Raises:
        HTTPException: Lỗi 404 nếu không tìm thấy bản ghi giỏ hàng thuộc sở hữu của người dùng.
    """
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
    """
    Xóa một bản ghi mặt hàng cụ thể ra khỏi giỏ hàng của người dùng.

    Args:
        item_id (int): ID của bản ghi giỏ hàng cần xóa.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
        nguoi_dung (NguoiDung): Người dùng hiện tại đang đăng nhập.

    Returns:
        dict: Trạng thái chi tiết của yêu cầu xóa.

    Raises:
        HTTPException: Lỗi 404 nếu không tìm thấy bản ghi giỏ hàng tương ứng.
    """
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
    """
    Xóa sạch toàn bộ các mặt hàng trong giỏ hàng của người dùng hiện tại.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
        nguoi_dung (NguoiDung): Người dùng hiện tại đang đăng nhập.

    Returns:
        dict: Thông điệp xác nhận đã dọn sạch giỏ hàng.
    """
    db.query(GioHang).filter(GioHang.nguoi_dung_id == nguoi_dung.id).delete()
    db.commit()
    return {"detail": "Da lam trong gio hang"}
