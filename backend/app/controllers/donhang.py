from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.donhang_service import DonHangService
from app.schemas.donhang import DonHangCreate, DonHangSchema, DonHangUpdateStatus
from app.core.phu_thuoc import lay_nguoi_dung_hien_tai
from app.models.nguoidung import NguoiDung

router = APIRouter(prefix="/don-hang", tags=["Đơn hàng"])

@router.post("/tao", response_model=DonHangSchema)
async def tao_don_hang(
    order_data: DonHangCreate, 
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """Người dùng đặt hàng"""
    if nguoi_dung.yeu_cau_pin:
        if not order_data.ma_pin:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Mã PIN giao dịch là bắt buộc!")
        from app.services.bao_mat import DichVuBaoMat
        if not DichVuBaoMat.xac_minh_mat_khau(order_data.ma_pin, nguoi_dung.ma_pin):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Mã PIN giao dịch không chính xác!")

    return await DonHangService.create_order(db, order_data, nguoi_dung.id)

@router.get("/admin/all", response_model=List[DonHangSchema])
async def lay_tat_ca_don_hang_admin(db: Session = Depends(get_db)):
    """Admin xem toàn bộ đơn hàng (Không cần đăng nhập)"""
    return await DonHangService.get_all_orders(db)

@router.put("/cap-nhat-trang-thai/{order_id}")
async def admin_cap_nhat_trang_thai(order_id: int, status_data: DonHangUpdateStatus, db: Session = Depends(get_db)):
    """Admin cập nhật trạng thái (Không cần đăng nhập)"""
    return await DonHangService.update_order_status(db, order_id, status_data.trang_thai)

@router.put("/admin/update/{order_id}")
async def admin_update_order(order_id: int, update_data: dict, db: Session = Depends(get_db)):
    """Admin cập nhật thông tin chung đơn hàng"""
    return await DonHangService.admin_update_order(db, order_id, update_data)

@router.get("/user/my-orders", response_model=List[DonHangSchema])
async def lay_don_hang_cua_toi(
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """Người dùng xem lịch sử đơn hàng của mình"""
    return await DonHangService.get_user_orders(db, nguoi_dung.id)

@router.delete("/xoa/{order_id}")
async def xoa_don_hang(
    order_id: int,
    db: Session = Depends(get_db),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)
):
    """Ẩn đơn hàng (xóa mềm) từ phía người dùng"""
    return await DonHangService.delete_order(db, order_id, nguoi_dung)
@router.delete("/admin/xoa/{order_id}")
async def admin_xoa_don_hang(order_id: int, db: Session = Depends(get_db)):
    """Admin xóa hẳn đơn hàng vĩnh viễn"""
    return await DonHangService.admin_delete_order(db, order_id)

@router.post("/admin/xoa-nhieu")
async def admin_xoa_nhieu_don_hang(order_ids: List[int], db: Session = Depends(get_db)):
    """Admin xóa nhiều đơn hàng vĩnh viễn"""
    return await DonHangService.admin_bulk_delete_orders(db, order_ids)

@router.get("/tra-cuu-bao-hanh/{imei}")
async def tra_cuu_bao_hanh(imei: str, db: Session = Depends(get_db)):
    """Tra cứu bảo hành theo mã IMEI"""
    from app.models.donhang import DonHang
    from datetime import datetime, timedelta
    from fastapi import HTTPException
    
    # Tìm kiếm không phân biệt chữ hoa chữ thường
    order = db.query(DonHang).filter(DonHang.imei.ilike(imei)).first()
    if not order:
        raise HTTPException(
            status_code=404, 
            detail="Không tìm thấy mã IMEI bảo hành này trong hệ thống. Vui lòng kiểm tra lại!"
        )
        
    # Tính thời hạn bảo hành
    months = order.warranty_months or 6
    
    # Lấy hạng thẻ thành viên của người dùng lúc mua hàng
    hang_the = "Tiêu chuẩn"
    if order.user_id:
        from app.models.nguoidung import NguoiDung
        user = db.query(NguoiDung).filter(NguoiDung.id == order.user_id).first()
        if user:
            points = user.diem_tich_luy or 0
            if points >= 10000:
                hang_the = "Kim cương"
            elif points >= 5000:
                hang_the = "Vàng"
            elif points >= 1000:
                hang_the = "Bạc"
            else:
                hang_the = "Tiêu chuẩn"
                
    # Lấy tên các sản phẩm
    product_names = []
    for item in order.items:
        if item.san_pham:
            detail_str = item.san_pham.ten
            if item.dung_luong:
                detail_str += f" ({item.dung_luong})"
            product_names.append(detail_str)
            
    # Nếu đơn hàng chưa hoàn thành, bảo hành chưa kích hoạt
    if order.trang_thai != "hoan_thanh" or not order.ngay_hoan_thanh:
        return {
            "ten_khach_hang": order.ten_khach_hang,
            "so_dien_thoai": order.so_dien_thoai[:4] + "****" + order.so_dien_thoai[-3:] if len(order.so_dien_thoai) > 6 else order.so_dien_thoai,
            "ten_san_pham": ", ".join(product_names) if product_names else "Sản phẩm Peach Store",
            "imei": order.imei,
            "ngay_mua": "Chưa kích hoạt (Đơn hàng chưa hoàn thành)",
            "thoi_han_bao_hanh": f"{months} tháng",
            "ngay_het_han": "Chưa kích hoạt",
            "trang_thai_bao_hanh": "ChuaKichHoat",
            "so_ngay_con_lai": 0,
            "hang_the": hang_the
        }
        
    # Tính ngày hết hạn từ thời điểm hoàn thành đơn hàng (giây, phút, giờ, ngày, tháng, năm)
    expiration_date = order.ngay_hoan_thanh + timedelta(days=months * 30)
    
    # Tính số ngày còn lại
    now = datetime.utcnow()
    time_left = expiration_date - now
    days_left = max(0, time_left.days)
    
    trang_thai = "ConHieuLuc" if days_left > 0 else "HetHieuLuc"
            
    return {
        "ten_khach_hang": order.ten_khach_hang,
        "so_dien_thoai": order.so_dien_thoai[:4] + "****" + order.so_dien_thoai[-3:] if len(order.so_dien_thoai) > 6 else order.so_dien_thoai,
        "ten_san_pham": ", ".join(product_names) if product_names else "Sản phẩm Peach Store",
        "imei": order.imei,
        "ngay_mua": order.ngay_hoan_thanh.strftime("%H:%M:%S %d/%m/%Y"),
        "thoi_han_bao_hanh": f"{months} tháng",
        "ngay_het_han": expiration_date.strftime("%H:%M:%S %d/%m/%Y"),
        "trang_thai_bao_hanh": trang_thai,
        "so_ngay_con_lai": days_left,
        "hang_the": hang_the
    }
