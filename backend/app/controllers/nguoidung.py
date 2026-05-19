from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.nguoidung import NguoiDung
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(tags=["Admin Quản lý Khách hàng"])

class CustomerUpdate(BaseModel):
    ho_ten: Optional[str] = None
    email: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None
    vai_tro: Optional[str] = None
    trang_thai: Optional[str] = None

def _build_image_url(hinh_anh_raw) -> str:
    """Helper to build image URL without f-string backslash issues."""
    if not hinh_anh_raw:
        return None
    ha = str(hinh_anh_raw)
    if not ha.strip():
        return None
    if "/static/uploads/" in ha:
        ha = "/static/uploads/" + ha.split("/static/uploads/", 1)[1]
    else:
        for host in ["http://127.0.0.1:8000", "http://localhost:8000", "https://peach-store-backend.onrender.com"]:
            if ha.startswith(host):
                ha = ha[len(host):]
    if ha.startswith('http'):
        return ha
    # Normalize backslashes to forward slashes
    ha_normalized = ha.replace('\\', '/')
    filename = ha_normalized.split('/')[-1]
    if "user_" in ha:
        return f"/static/uploads/avatars/{filename}"
    return f"/static/uploads/{filename}"

@router.get("/api/admin/customers", response_model=List[dict])
@router.get("/api/admin/customers/", response_model=List[dict])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(NguoiDung).all()
    return [
        {
            "id": c.id,
            "ho_ten": c.ho_ten,
            "email": c.email,
            "so_dien_thoai": c.so_dien_thoai,
            "dia_chi": c.dia_chi,
            "vai_tro": c.vai_tro,
            "trang_thai": getattr(c, 'trang_thai', 'dang_hoat_dong'),
            "diem_tich_luy": getattr(c, 'diem_tich_luy', 0),
            "hinh_anh": _build_image_url(getattr(c, 'hinh_anh', None))
        } for c in customers
    ]

@router.post("/api/admin/customers")
@router.post("/api/admin/customers/")
def create_customer(data: dict, db: Session = Depends(get_db)):
    # Đảm bảo có mật khẩu mặc định nếu admin không nhập
    if "mat_khau" not in data or not data["mat_khau"]:
        data["mat_khau"] = "123456" # Mật khẩu mặc định
    
    new_user = NguoiDung(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Thêm thành công", "id": new_user.id}

@router.put("/api/admin/customers/{customer_id}")
def update_customer(customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(NguoiDung).filter(NguoiDung.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, key, value)
    
    db.commit()
    return {"message": "Cập nhật thành công"}

@router.delete("/api/admin/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    from app.models.donhang import DonHang
    from app.models.giohang import GioHang
    from app.models.lichsu_dangnhap import LichSuDangNhap
    from app.models.yeuthich import YeuThich
    from app.models.tinnhan_chat import TinNhanChat
    from app.models.yeu_cau_ho_tro import YeuCauHoTro
    from app.models.yeu_cau_doanh_nghiep import YeuCauDoanhNghiep
    
    customer = db.query(NguoiDung).filter(NguoiDung.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng")
    
    try:
        # 1. Unlink orders (preserve history but remove user link)
        db.query(DonHang).filter(DonHang.user_id == customer_id).update({DonHang.user_id: None})
        
        # 2. Delete cart items
        db.query(GioHang).filter(GioHang.nguoi_dung_id == customer_id).delete()
        
        # 3. Delete login history
        db.query(LichSuDangNhap).filter(LichSuDangNhap.nguoi_dung_id == customer_id).delete()
        
        # 4. Delete favorites
        db.query(YeuThich).filter(YeuThich.nguoi_dung_id == customer_id).delete()
        
        # 5. Delete chat messages
        db.query(TinNhanChat).filter(TinNhanChat.nguoi_dung_id == customer_id).delete()
        
        # 6. Delete support tickets/requests
        db.query(YeuCauHoTro).filter(YeuCauHoTro.nguoi_dung_id == customer_id).delete()
        
        # 7. Delete business upgrade requests
        db.query(YeuCauDoanhNghiep).filter(YeuCauDoanhNghiep.nguoi_dung_id == customer_id).delete()
        
        # 8. Delete the user
        db.delete(customer)
        db.commit()
        return {"message": "Xóa thành công"}
    except Exception as e:
        db.rollback()
        print(f"Error deleting customer {customer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa người dùng: {str(e)}")

import json
import os
import random
from datetime import datetime
from app.services.bao_mat import DichVuBaoMat

RESET_REQUESTS_FILE = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "static",
        "reset_requests.json"
    )
)

def read_reset_requests():
    if not os.path.exists(RESET_REQUESTS_FILE):
        return []
    try:
        with open(RESET_REQUESTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def write_reset_requests(data):
    os.makedirs(os.path.dirname(RESET_REQUESTS_FILE), exist_ok=True)
    try:
        with open(RESET_REQUESTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing reset requests: {e}")

@router.post("/api/support/reset-requests")
def create_reset_request(data: dict):
    requests = read_reset_requests()
    new_id = len(requests) + 1
    new_req = {
        "id": new_id,
        "type": data.get("type"), # 'password' or 'pin'
        "fullName": data.get("fullName"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "address": data.get("address"),
        "message": data.get("message"),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    requests.append(new_req)
    write_reset_requests(requests)
    return {"message": "Gửi yêu cầu thành công!", "id": new_id}

@router.get("/api/support/reset-requests")
def get_reset_requests():
    return read_reset_requests()

class VerifyPayload(BaseModel):
    fullName: str
    email: str
    phone: str
    address: str

@router.post("/api/support/verify-customer")
def verify_customer(payload: VerifyPayload, db: Session = Depends(get_db)):
    customers = db.query(NguoiDung).all()
    matched_user = None
    
    for c in customers:
        db_name = (c.ho_ten or "").strip().lower()
        payload_name = payload.fullName.strip().lower()
        
        db_email = (c.email or "").strip().lower()
        payload_email = payload.email.strip().lower()
        
        # Chuẩn hóa số điện thoại: xóa khoảng trắng, dấu gạch ngang
        db_phone = (c.so_dien_thoai or "").strip().replace(" ", "").replace("-", "")
        payload_phone = payload.phone.strip().replace(" ", "").replace("-", "")
        
        # Chuẩn hóa địa chỉ
        db_address = (c.dia_chi or "").strip().lower()
        payload_address = payload.address.strip().lower()
        
        # So khớp chính xác sau khi chuẩn hóa (Tên, Email, SĐT) - Bỏ hoàn toàn địa chỉ để tránh sai lệch
        if (db_name == payload_name and
            db_email == payload_email and
            db_phone == payload_phone):
            matched_user = c
            break
            
    if not matched_user:
        return {"matched": False, "message": "Thông tin chi tiết cung cấp không khớp với bất kỳ tài khoản nào."}
        
    return {
        "matched": True,
        "user": {
            "id": matched_user.id,
            "ho_ten": matched_user.ho_ten,
            "email": matched_user.email,
            "so_dien_thoai": matched_user.so_dien_thoai,
            "dia_chi": matched_user.dia_chi,
            "vai_tro": matched_user.vai_tro,
            "trang_thai": getattr(matched_user, 'trang_thai', 'dang_hoat_dong')
        }
    }

@router.post("/api/support/reset-password")
def reset_customer_password(data: dict, db: Session = Depends(get_db)):
    user_id = data.get("user_id")
    request_id = data.get("request_id")
    user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
        
    new_password = "PEACH" + "".join([str(random.randint(0, 9)) for _ in range(6)])
    user.mat_khau = DichVuBaoMat.ma_hoa_mat_khau(new_password)
    
    if request_id:
        reqs = read_reset_requests()
        for r in reqs:
            if r["id"] == int(request_id):
                r["status"] = "resolved_password"
                r["new_password"] = new_password
        write_reset_requests(reqs)
        
    db.commit()
    return {"success": True, "new_password": new_password}

@router.post("/api/support/reset-pin")
def reset_customer_pin(data: dict, db: Session = Depends(get_db)):
    user_id = data.get("user_id")
    request_id = data.get("request_id")
    user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
        
    new_pin = "".join([str(random.randint(0, 9)) for _ in range(6)])
    user.ma_pin = DichVuBaoMat.ma_hoa_mat_khau(new_pin)
    
    if request_id:
        reqs = read_reset_requests()
        for r in reqs:
            if r["id"] == int(request_id):
                r["status"] = "resolved_pin"
                r["new_pin"] = new_pin
        write_reset_requests(reqs)
        
    db.commit()
    return {"success": True, "new_pin": new_pin}


@router.get("/api/support/admin/unread-states")
def lay_trang_thai_chua_rep(db: Session = Depends(get_db)):
    """API lấy danh sách các customer_id có tin nhắn cuối cùng là từ user (admin chưa rep)"""
    from app.models.tinnhan_chat import TinNhanChat
    from sqlalchemy import func
    
    # Query to find the max message ID for each customer
    subq = db.query(
        TinNhanChat.nguoi_dung_id,
        func.max(TinNhanChat.id).label("max_id")
    ).group_by(TinNhanChat.nguoi_dung_id).subquery()
    
    # Join back to get the actual sender of the last message
    latest_messages = db.query(TinNhanChat).join(
        subq,
        (TinNhanChat.id == subq.c.max_id)
    ).all()
    
    # Map of user_id -> whether last sender is 'user' (i.e. admin hasn't replied yet)
    unread_map = {}
    for m in latest_messages:
        unread_map[m.nguoi_dung_id] = (m.nguoi_gui == 'user')
        
    return unread_map


class AdminGuiTinNhanPayload(BaseModel):
    text: str


@router.get("/api/support/admin/tin-nhan-chat/{nguoi_dung_id}")
def lay_tin_nhan_chat_admin(
    nguoi_dung_id: int,
    db: Session = Depends(get_db)
):
    """API Admin lấy toàn bộ tin nhắn chat của 1 khách hàng cụ thể"""
    from app.models.tinnhan_chat import TinNhanChat
    messages = db.query(TinNhanChat).filter(
        TinNhanChat.nguoi_dung_id == nguoi_dung_id
    ).order_by(TinNhanChat.id.asc()).all()
    
    return [
        {
            "id": m.id,
            "sender": m.nguoi_gui,
            "text": m.noi_dung,
            "time": m.thoi_gian.strftime("%H:%M")
        }
        for m in messages
    ]


@router.post("/api/support/admin/tin-nhan-chat/{nguoi_dung_id}")
def gui_tin_nhan_chat_admin(
    nguoi_dung_id: int,
    payload: AdminGuiTinNhanPayload,
    db: Session = Depends(get_db)
):
    """API Admin gửi tin nhắn chat phản hồi cho 1 khách hàng cụ thể"""
    from app.models.tinnhan_chat import TinNhanChat
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Nội dung tin nhắn không được để trống!")
        
    m = TinNhanChat(
        nguoi_dung_id=nguoi_dung_id,
        nguoi_gui="admin",
        noi_dung=payload.text.strip()
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    
    # Ghi nhật ký Admin
    try:
        from app.models.nguoidung import NguoiDung
        from app.services.admin_activity_service import AdminActivityService
        user = db.query(NguoiDung).filter(NguoiDung.id == nguoi_dung_id).first()
        user_name = user.ho_ten if user else f"Khách hàng #{nguoi_dung_id}"
        AdminActivityService.ghi_log(db, f"Trả lời tin nhắn của khách hàng: {user_name}", "Admin")
    except Exception as chat_log_err:
        print(f">>> Lỗi ghi log chat Admin: {chat_log_err}")
    
    return {
        "id": m.id,
        "sender": m.nguoi_gui,
        "text": m.noi_dung,
        "time": m.thoi_gian.strftime("%H:%M")
    }


class CapNhatTrangThaiTicketPayload(BaseModel):
    trang_thai: str


@router.get("/api/support/admin/tickets")
def lay_tat_ca_tickets_admin(db: Session = Depends(get_db)):
    """API Admin lấy toàn bộ danh sách yêu cầu hỗ trợ (tickets)"""
    from app.models.yeu_cau_ho_tro import YeuCauHoTro
    
    # Tự động dọn dẹp dữ liệu mẫu nếu có trong DB
    db.query(YeuCauHoTro).filter(YeuCauHoTro.chu_de.like("%Lỗi camera%")).delete(synchronize_session=False)
    db.commit()
    
    tickets = db.query(YeuCauHoTro).order_by(YeuCauHoTro.id.desc()).all()
    
    return [
        {
            "id": t.id,
            "user": {
                "id": t.nguoi_dung.id,
                "ho_ten": t.nguoi_dung.ho_ten,
                "email": t.nguoi_dung.email,
                "so_dien_thoai": t.nguoi_dung.so_dien_thoai
            },
            "chu_de": t.chu_de,
            "imei_serial": t.imei_serial,
            "noi_dung": t.noi_dung,
            "trang_thai": t.trang_thai,
            "hinh_anh": t.hinh_anh.split(";") if t.hinh_anh else [],
            "thoi_gian": t.thoi_gian.strftime("%Y-%m-%d %H:%M:%S")
        }
        for t in tickets
    ]


@router.post("/api/support/admin/tickets/{ticket_id}/status")
def cap_nhat_trang_thai_ticket(
    ticket_id: int,
    payload: CapNhatTrangThaiTicketPayload,
    db: Session = Depends(get_db)
):
    """API Admin cập nhật trạng thái của yêu cầu hỗ trợ"""
    from app.models.yeu_cau_ho_tro import YeuCauHoTro
    
    ticket = db.query(YeuCauHoTro).filter(YeuCauHoTro.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Yêu cầu hỗ trợ không tồn tại!")
        
    valid_statuses = ["cho_xu_ly", "dang_xu_ly", "da_xu_ly"]
    if payload.trang_thai not in valid_statuses:
        raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ!")
        
    ticket.trang_thai = payload.trang_thai
    
    # Ghi nhật ký Admin
    from app.services.admin_activity_service import AdminActivityService
    status_map = {
        "cho_xu_ly": "Chờ xử lý",
        "dang_xu_ly": "Đang xử lý",
        "da_xu_ly": "Đã xử lý"
    }
    status_vn = status_map.get(payload.trang_thai, payload.trang_thai)
    AdminActivityService.ghi_log(db, f"Cập nhật trạng thái yêu cầu hỗ trợ #{ticket_id} thành: {status_vn}", "Admin")
    
    db.commit()
    
    return {"success": True, "message": "Cập nhật trạng thái thành công!", "trang_thai": ticket.trang_thai}


# --- ADMIN LOẠI HÌNH DOANH NGHIỆP ---

@router.get("/api/admin/business-requests")
def lay_yeu_cau_doanh_nghiep(db: Session = Depends(get_db)):
    """API Admin lấy danh sách yêu cầu đăng ký nâng cấp doanh nghiệp"""
    from app.models.yeu_cau_doanh_nghiep import YeuCauDoanhNghiep
    requests = db.query(YeuCauDoanhNghiep).order_by(YeuCauDoanhNghiep.ngay_tao.desc()).all()
    return [
        {
            "id": r.id,
            "nguoi_dung_id": r.nguoi_dung_id,
            "ho_ten": r.nguoi_dung.ho_ten if r.nguoi_dung else "Không xác định",
            "email": r.nguoi_dung.email if r.nguoi_dung else "Không xác định",
            "ten_doanh_nghiep": r.ten_doanh_nghiep,
            "ma_so_thue": r.ma_so_thue,
            "dia_chi_kd": r.dia_chi_kd,
            "linh_vuc_kd": r.linh_vuc_kd,
            "trang_thai": r.trang_thai,
            "ngay_tao": r.ngay_tao.strftime("%Y-%m-%d %H:%M:%S") if r.ngay_tao else None,
            "ngay_duyet": r.ngay_duyet.strftime("%Y-%m-%d %H:%M:%S") if r.ngay_duyet else None
        }
        for r in requests
    ]


@router.post("/api/admin/business-requests/{request_id}/approve")
def phe_duyet_yeu_cau_doanh_nghiep(request_id: int, db: Session = Depends(get_db)):
    """API Admin phê duyệt yêu cầu đăng ký Doanh nghiệp và nâng cấp role người dùng"""
    from app.models.yeu_cau_doanh_nghiep import YeuCauDoanhNghiep
    from app.models.nguoidung import NguoiDung
    from datetime import datetime
    
    yeu_cau = db.query(YeuCauDoanhNghiep).filter(YeuCauDoanhNghiep.id == request_id).first()
    if not yeu_cau:
        raise HTTPException(status_code=404, detail="Yêu cầu không tồn tại!")
        
    if yeu_cau.trang_thai != "cho_duyet":
        raise HTTPException(status_code=400, detail="Yêu cầu này đã được xử lý từ trước!")
        
    user = db.query(NguoiDung).filter(NguoiDung.id == yeu_cau.nguoi_dung_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Khách hàng gửi yêu cầu này không còn tồn tại trên hệ thống!")
        
    # Nâng cấp tài khoản người dùng sang doanh_nghiep
    user.vai_tro = "doanh_nghiep"
    user.ten_doanh_nghiep = yeu_cau.ten_doanh_nghiep
    user.ma_so_thue = yeu_cau.ma_so_thue
    user.dia_chi_kd = yeu_cau.dia_chi_kd
    user.linh_vuc_kd = yeu_cau.linh_vuc_kd
    
    # Cập nhật trạng thái yêu cầu
    yeu_cau.trang_thai = "da_duyet"
    yeu_cau.ngay_duyet = datetime.utcnow()
    
    # Ghi nhật ký Admin
    from app.services.admin_activity_service import AdminActivityService
    AdminActivityService.ghi_log(db, f"Phê duyệt nâng cấp Doanh nghiệp cho: {user.ho_ten} ({yeu_cau.ten_doanh_nghiep})", "Admin")
    
    db.commit()
    return {"success": True, "message": f"Đã phê duyệt và nâng cấp tài khoản {user.ho_ten} thành tài khoản Doanh nghiệp thành công!"}


@router.post("/api/admin/business-requests/{request_id}/reject")
def tu_choi_yeu_cau_doanh_nghiep(request_id: int, db: Session = Depends(get_db)):
    """API Admin từ chối yêu cầu đăng ký Doanh nghiệp"""
    from app.models.yeu_cau_doanh_nghiep import YeuCauDoanhNghiep
    from datetime import datetime
    
    yeu_cau = db.query(YeuCauDoanhNghiep).filter(YeuCauDoanhNghiep.id == request_id).first()
    if not yeu_cau:
        raise HTTPException(status_code=404, detail="Yêu cầu không tồn tại!")
        
    if yeu_cau.trang_thai != "cho_duyet":
        raise HTTPException(status_code=400, detail="Yêu cầu này đã được xử lý từ trước!")
        
    yeu_cau.trang_thai = "tu_choi"
    yeu_cau.ngay_duyet = datetime.utcnow()
    
    # Ghi nhật ký Admin
    from app.services.admin_activity_service import AdminActivityService
    AdminActivityService.ghi_log(db, f"Từ chối yêu cầu nâng cấp Doanh nghiệp (Yêu cầu #{request_id})", "Admin")
    
    db.commit()
    return {"success": True, "message": "Đã từ chối yêu cầu đăng ký Doanh nghiệp của khách hàng."}


@router.post("/api/support/reset-requests/resolve-all")
def resolve_all_reset_requests():
    """API Admin giải quyết toàn bộ yêu cầu khôi phục mật khẩu/PIN"""
    reqs = read_reset_requests()
    count = 0
    for r in reqs:
        if r.get("status") == "pending":
            r["status"] = "resolved_by_admin"
            count += 1
    if count > 0:
        write_reset_requests(reqs)
    return {"success": True, "message": f"Đã đánh dấu xử lý thành công {count} yêu cầu khôi phục!", "resolved_count": count}


@router.post("/api/admin/business-requests/approve-all")
def phe_duyet_tat_ca_yeu_cau_doanh_nghiep(db: Session = Depends(get_db)):
    """API Admin phê duyệt tất cả yêu cầu đăng ký Doanh nghiệp đang chờ"""
    from app.models.yeu_cau_doanh_nghiep import YeuCauDoanhNghiep
    from app.models.nguoidung import NguoiDung
    from datetime import datetime
    
    yeu_cau_list = db.query(YeuCauDoanhNghiep).filter(YeuCauDoanhNghiep.trang_thai == "cho_duyet").all()
    count = 0
    for yeu_cau in yeu_cau_list:
        user = db.query(NguoiDung).filter(NguoiDung.id == yeu_cau.nguoi_dung_id).first()
        if user:
            user.vai_tro = "doanh_nghiep"
            user.ten_doanh_nghiep = yeu_cau.ten_doanh_nghiep
            user.ma_so_thue = yeu_cau.ma_so_thue
            user.dia_chi_kd = yeu_cau.dia_chi_kd
            user.linh_vuc_kd = yeu_cau.linh_vuc_kd
            
            yeu_cau.trang_thai = "da_duyet"
            yeu_cau.ngay_duyet = datetime.utcnow()
            count += 1
            
    if count > 0:
        db.commit()
    return {"success": True, "message": f"Đã phê duyệt và nâng cấp thành công {count} tài khoản doanh nghiệp!", "approved_count": count}


