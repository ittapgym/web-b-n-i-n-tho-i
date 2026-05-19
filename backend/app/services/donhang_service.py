from sqlalchemy.orm import Session, joinedload
from typing import List
from app.models.donhang import DonHang, ChiTietDonHang
from app.models.giohang import GioHang
from app.models.voucher import Voucher
from app.schemas.donhang import DonHangCreate
from app.services.voucher_service import VoucherService
from app.services.shipping_service import ShippingService
from fastapi import HTTPException


class DonHangService:
    @staticmethod
    async def create_order(db: Session, order_data: DonHangCreate, user_id: int = None):
        """Tạo đơn hàng mới và chi tiết đơn hàng, sau đó xóa giỏ hàng tương ứng.
        Server-side calculation: tong_tien, giam_gia_voucher, phi_ship được tính ở server."""
        try:
            # Check daily purchase limit of 10 items for Personal accounts (i.e. not doanh_nghiep and not admin)
            if user_id:
                from app.models.nguoidung import NguoiDung
                from datetime import datetime, time
                user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
                if user and user.vai_tro not in ["doanh_nghiep", "admin"]:
                    # Lấy thời gian bắt đầu của ngày hôm nay (00:00:00)
                    today_start = datetime.combine(datetime.now().date(), time.min)
                    # Lấy danh sách các đơn hàng đã đặt hôm nay của người dùng này
                    orders_today = db.query(DonHang).filter(
                        DonHang.user_id == user_id,
                        DonHang.ngay_tao >= today_start
                    ).all()
                    
                    # Tính tổng số lượng sản phẩm đã mua hôm nay
                    total_qty_today = 0
                    for o in orders_today:
                        for item in o.items:
                            total_qty_today += item.so_luong
                    
                    # Cộng thêm số lượng của đơn hàng mới đang đặt
                    new_order_qty = sum(item.so_luong for item in order_data.items)
                    
                    if total_qty_today + new_order_qty > 10:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Tài khoản Cá nhân bị giới hạn mua tối đa 10 sản phẩm mỗi ngày. Hôm nay bạn đã mua {total_qty_today} sản phẩm và đang định đặt thêm {new_order_qty} sản phẩm. Vui lòng đăng ký tài khoản Doanh nghiệp trong trang Hồ sơ cá nhân để không bị giới hạn số lượng mua!"
                        )

            # 1. Tính tổng tiền hàng từ items (server-side, không tin client)
            tong_tien_hang = sum(item.gia * item.so_luong for item in order_data.items)

            # 2. Xử lý Voucher nếu có
            giam_gia_voucher = 0.0
            voucher_id = None
            if order_data.ma_voucher:
                voucher_check = await VoucherService.kiem_tra_voucher(
                    db, order_data.ma_voucher, tong_tien_hang
                )
                if not voucher_check.hop_le:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Voucher không hợp lệ: {voucher_check.loi}",
                    )
                giam_gia_voucher = voucher_check.so_tien_giam
                # Lấy voucher_id từ DB
                voucher = (
                    db.query(Voucher)
                    .filter(Voucher.ma_voucher == order_data.ma_voucher)
                    .first()
                )
                if voucher:
                    voucher_id = voucher.id

            # 3. Xử lý phí ship nếu có
            phi_ship = 0.0
            if order_data.phuong_thuc_van_chuyen:
                phi_ship = await ShippingService.tinh_phi_ship(
                    order_data.phuong_thuc_van_chuyen, tong_tien_hang, db
                )

            # 4. Tính tổng tiền cuối cùng
            tong_tien_cuoi = tong_tien_hang - giam_gia_voucher + phi_ship
            if tong_tien_cuoi < 0:
                tong_tien_cuoi = 0

            # Generate random IMEI: 10 random digits + 2 random letters
            import random
            import string
            imei_digits = "".join(random.choices(string.digits, k=10))
            imei_letters = "".join(random.choices(string.ascii_uppercase, k=2))
            order_imei = f"{imei_digits}{imei_letters}"
            
            # Determine warranty months based on loyalty tier
            warranty_months = 6  # Default/Standard
            if user_id:
                from app.models.nguoidung import NguoiDung
                user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
                if user:
                    points = getattr(user, 'diem_tich_luy', 0) or 0
                    if points >= 10000:
                        warranty_months = 24  # Kim cương (Diamond)
                    elif points >= 5000:
                        warranty_months = 16  # Vàng (Gold)
                    elif points >= 1000:
                        warranty_months = 12  # Bạc (Silver)
                    else:
                        warranty_months = 6   # Standard

            # 5. Tạo Đơn hàng mới
            new_order = DonHang(
                user_id=user_id,
                ten_khach_hang=order_data.ten_khach_hang,
                so_dien_thoai=order_data.so_dien_thoai,
                dia_chi=order_data.dia_chi,
                ghi_chu=order_data.ghi_chu,
                tong_tien=tong_tien_cuoi,
                trang_thai="cho_duyet",
                phuong_thuc_thanh_toan=order_data.phuong_thuc_thanh_toan,
                phuong_thuc_van_chuyen=order_data.phuong_thuc_van_chuyen,
                phi_ship=phi_ship,
                giam_gia_voucher=giam_gia_voucher,
                voucher_id=voucher_id,
                imei=order_imei,
                warranty_months=warranty_months,
            )
            db.add(new_order)
            db.flush()  # Lấy ID của đơn hàng vừa tạo

            # 6. Tạo Chi tiết đơn hàng và trừ tồn kho
            from app.models.sanpham import SanPham
            for item in order_data.items:
                # Tìm sản phẩm để kiểm tra và trừ tồn kho
                product = db.query(SanPham).filter(SanPham.id == item.san_pham_id).first()
                if not product:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Không tìm thấy sản phẩm có ID {item.san_pham_id}"
                    )
                
                # Kiểm tra tồn kho
                product_stock = getattr(product, 'so_luong_kho', 100)
                if product_stock is None:
                    product_stock = 100
                if product_stock < item.so_luong:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Sản phẩm '{product.ten}' đã hết hàng hoặc không đủ số lượng tồn kho (Còn lại: {product_stock})"
                    )
                
                # Trừ tồn kho
                product.so_luong_kho = product_stock - item.so_luong

                detail = ChiTietDonHang(
                    don_hang_id=new_order.id,
                    san_pham_id=item.san_pham_id,
                    so_luong=item.so_luong,
                    gia=item.gia,
                    dung_luong=item.dung_luong,
                    ram=item.ram,
                    mau_sac=item.mau_sac,
                )
                db.add(detail)

            # 7. Xóa giỏ hàng của người dùng sau khi đặt thành công (nếu có user_id)
            if user_id:
                db.query(GioHang).filter(GioHang.nguoi_dung_id == user_id).delete()

            # 8. Giảm lượt dùng voucher (nếu có)
            if voucher_id:
                await VoucherService.cap_nhat_luot_dung(db, voucher_id)

            db.commit()
            db.refresh(new_order)
            return new_order
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Lỗi khi tạo đơn hàng: {str(e)}"
            )

    @staticmethod
    async def get_all_orders(db: Session):
        """Lấy toàn bộ danh sách đơn hàng (Dành cho Admin)."""
        return (
            db.query(DonHang)
            .options(joinedload(DonHang.items).joinedload(ChiTietDonHang.san_pham))
            .order_by(DonHang.ngay_tao.desc())
            .all()
        )

    @staticmethod
    async def update_status(db: Session, order_id: int, status: str):
        """Cập nhật trạng thái đơn hàng (Dành cho Admin)."""
        order = db.query(DonHang).filter(DonHang.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

        order.trang_thai = status
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    async def get_user_orders(db: Session, user_id: int):
        """Lấy danh sách đơn hàng của một người dùng cụ thể."""
        return (
            db.query(DonHang)
            .options(joinedload(DonHang.items).joinedload(ChiTietDonHang.san_pham))
            .filter(DonHang.user_id == user_id, DonHang.is_visible_user)
            .order_by(DonHang.ngay_tao.desc())
            .all()
        )

    @staticmethod
    async def update_order_status(db: Session, order_id: int, trang_thai: str):
        """Cập nhật trạng thái của một đơn hàng cụ thể."""
        order = db.query(DonHang).filter(DonHang.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

        try:
            order.trang_thai = trang_thai
            if trang_thai == "hoan_thanh":
                from datetime import datetime
                order.ngay_hoan_thanh = datetime.utcnow()
            else:
                order.ngay_hoan_thanh = None
            db.commit()
            
            # Ghi nhật ký Admin
            from app.services.admin_activity_service import AdminActivityService
            status_map = {
                "cho_duyet": "Chờ duyệt",
                "da_duyet": "Đã duyệt",
                "dang_giao": "Đang giao",
                "hoan_thanh": "Hoàn thành",
                "da_huy": "Đã hủy"
            }
            status_vn = status_map.get(trang_thai, trang_thai)
            AdminActivityService.ghi_log(db, f"Cập nhật trạng thái đơn hàng #{order_id} sang: {status_vn}", "Admin")
            
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Lỗi khi cập nhật trạng thái: {str(e)}"
            )

    @staticmethod
    async def admin_update_order(db: Session, order_id: int, update_data: dict):
        """Admin cập nhật thông tin đơn hàng (Tên, SĐT, Địa chỉ, Ghi chú, Trạng thái)."""
        order = db.query(DonHang).filter(DonHang.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

        try:
            for key, value in update_data.items():
                if hasattr(order, key):
                    setattr(order, key, value)
                    if key in ("trang_thai", "status"):
                        if value == "hoan_thanh":
                            from datetime import datetime
                            order.ngay_hoan_thanh = datetime.utcnow()
                        else:
                            order.ngay_hoan_thanh = None
            db.commit()
            
            # Ghi nhật ký Admin
            from app.services.admin_activity_service import AdminActivityService
            AdminActivityService.ghi_log(db, f"Cập nhật thông tin chung đơn hàng #{order_id}", "Admin")
            
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Lỗi khi cập nhật đơn hàng: {str(e)}"
            )

    @staticmethod
    async def delete_order(db: Session, order_id: int, user: any):
        """Người dùng ẩn đơn hàng khỏi lịch sử của họ (Không xóa thật trong DB)."""
        order = db.query(DonHang).filter(DonHang.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

        # Chỉ chủ đơn hàng mới có quyền "ẩn" (xóa phía user)
        if order.user_id != user.id:
            raise HTTPException(
                status_code=403, detail="Bạn không có quyền ẩn đơn hàng này"
            )

        try:
            # Người dùng xóa -> Chỉ ẩn đi (is_visible_user = False)
            # Admin KHÔNG có quyền xóa trong hàm này (theo yêu cầu: Admin không xóa)
            order.is_visible_user = False
            db.commit()
            return {"message": "Đã ẩn đơn hàng thành công"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý: {str(e)}")

    @staticmethod
    async def admin_delete_order(db: Session, order_id: int):
        """Admin xóa vĩnh viễn một đơn hàng và các chi tiết liên quan."""
        order = db.query(DonHang).filter(DonHang.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

        try:
            # Xóa các chi tiết đơn hàng trước để tránh lỗi ràng buộc khóa ngoại
            db.query(ChiTietDonHang).filter(
                ChiTietDonHang.don_hang_id == order_id
            ).delete()
            # Xóa đơn hàng chính
            db.delete(order)
            db.commit()
            
            # Ghi nhật ký Admin
            from app.services.admin_activity_service import AdminActivityService
            AdminActivityService.ghi_log(db, f"Xóa vĩnh viễn đơn hàng #{order_id}", "Admin")
            
            return {"message": "Đã xóa đơn hàng vĩnh viễn"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Lỗi khi xóa đơn hàng: {str(e)}"
            )

    @staticmethod
    async def admin_bulk_delete_orders(db: Session, order_ids: List[int]):
        """Admin xóa hàng loạt các đơn hàng vĩnh viễn."""
        try:
            # Xóa chi tiết của tất cả đơn hàng trong danh sách để tránh lỗi khóa ngoại
            db.query(ChiTietDonHang).filter(
                ChiTietDonHang.don_hang_id.in_(order_ids)
            ).delete(synchronize_session=False)
            # Xóa các đơn hàng chính
            db.query(DonHang).filter(DonHang.id.in_(order_ids)).delete(
                synchronize_session=False
            )
            db.commit()
            
            # Ghi nhật ký Admin
            from app.services.admin_activity_service import AdminActivityService
            AdminActivityService.ghi_log(db, f"Xóa hàng loạt {len(order_ids)} đơn hàng (IDs: {order_ids})", "Admin")
            
            return {"message": f"Đã xóa thành công {len(order_ids)} đơn hàng"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Lỗi khi xóa hàng loạt đơn hàng: {str(e)}"
            )
