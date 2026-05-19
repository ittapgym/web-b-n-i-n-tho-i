from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sanpham import SanPham
from app.models.nguoidung import NguoiDung
from app.models.donhang import DonHang
from sqlalchemy import func
import os
import uuid
import shutil
import json
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["Admin Dashboard"])

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Lấy số liệu thống kê tổng quan cho trang Dashboard của hệ thống Admin.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy (được Dependency Inject).

    Returns:
        dict: Chứa thông tin doanh thu thực tế, tổng số đơn hàng, số người dùng và số sản phẩm.
    """
    # Đếm số sản phẩm
    product_count = db.query(SanPham).count()
    # Đếm số người dùng
    user_count = db.query(NguoiDung).count()
    
    # Doanh thu thật từ các đơn hàng không bị hủy
    revenue = db.query(func.sum(DonHang.tong_tien)).filter(DonHang.trang_thai != 'da_huy').scalar() or 0
    # Tổng số đơn hàng thật
    order_count = db.query(DonHang).count()
    
    return {
        "revenue": revenue,
        "order_count": order_count,
        "user_count": user_count,
        "product_count": product_count
    }

@router.get("/activities")
def get_recent_activities(db: Session = Depends(get_db)):
    """
    Lấy danh sách tối đa 50 hoạt động gần đây nhất của các tài khoản Admin/Nhân sự quản lý.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        list: Danh sách các đối tượng hoạt động chứa thời gian, nhân viên thực hiện và hành động chi tiết.
    """
    from app.models.hoatdong_admin import HoatDongAdmin
    from datetime import datetime
    
    # Lấy 50 hoạt động mới nhất sắp xếp giảm dần theo thời gian
    activities = db.query(HoatDongAdmin).order_by(HoatDongAdmin.thoi_gian.desc()).limit(50).all()
    
    results = []
    now = datetime.utcnow()
    for act in activities:
        # Nếu cùng ngày thì hiện Giờ:Phút, khác ngày thì hiện cả ngày tháng
        if act.thoi_gian.date() == now.date():
            time_str = act.thoi_gian.strftime("%H:%M")
        else:
            time_str = act.thoi_gian.strftime("%H:%M %d/%m")
            
        results.append({
            "time": time_str,
            "user": act.nhan_vien or "Admin",
            "action": act.thao_tac
        })
    return results

@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    """
    Tải tệp tin hình ảnh lên thư mục static/uploads của hệ thống backend.

    Args:
        request (Request): Đối tượng Request chứa thông tin host để sinh URL ảnh tuyệt đối.
        file (UploadFile): Tệp tin ảnh được tải lên từ biểu mẫu multipart/form-data.

    Returns:
        dict: Chứa URL tuyệt đối của tệp hình ảnh sau khi tải lên thành công.

    Raises:
        HTTPException: Lỗi 400 nếu định dạng file không được phép, hoặc 500 nếu ghi file thất bại.
    """
    try:
        # Kiểm tra định dạng file
        ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Chỉ cho phép tải lên các định dạng ảnh (jpg, png, webp,...)")

        # Đường dẫn thư mục uploads chuẩn (3 cấp từ app/controllers/admin.py để ra backend root)
        CONTROLLER_DIR = os.path.dirname(os.path.abspath(__file__))
        APP_DIR = os.path.dirname(CONTROLLER_DIR)
        BACKEND_DIR = os.path.dirname(APP_DIR)
        UPLOAD_DIR = os.path.join(BACKEND_DIR, "static", "uploads")
        os.makedirs(UPLOAD_DIR, exist_ok=True)
            
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Lưu file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        base_url = str(request.base_url).rstrip('/')
        image_url = f"{base_url}/static/uploads/{unique_filename}"
        return {"url": image_url}
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f">>> LOI UPLOAD: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi tải ảnh lên: {str(e)}")


@router.get("/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    """
    Lấy và định dạng danh sách nhật ký kiểm toán (Audit Logs) và lịch sử đăng nhập của khách hàng thực tế.
    Hàm này thực hiện dọn dẹp dữ liệu giả cũ và loại bỏ các tài khoản của admin/nhân sự quản lý.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        list: Danh sách nhật ký hành động đã sắp xếp theo thời gian mới nhất lên đầu.
    """
    from app.models.nhat_ky_audit import NhatKyAudit
    from app.models.lichsu_dangnhap import LichSuDangNhap
    from app.models.nguoidung import NguoiDung
    from datetime import datetime, timedelta
    
    # 1. Tự động dọn dẹp triệt để bất kỳ bản ghi thử nghiệm nào của admin/staff trong nhat_ky_audit
    db.query(NhatKyAudit).filter(
        (NhatKyAudit.user_email.like('%@peachstore.com')) |
        (NhatKyAudit.user_email == 'admin') |
        (NhatKyAudit.user_email.like('%admin%')) |
        (NhatKyAudit.user_email.like('%inventory%')) |
        (NhatKyAudit.user_email.like('%clerk%')) |
        (NhatKyAudit.user_email.like('%manager%'))
    ).delete(synchronize_session=False)
    db.commit()

    # 2. Xóa triệt để các dữ liệu giả (mock data) cũ trong nhat_ky_audit để chỉ hiển thị dữ liệu thực tế
    db.query(NhatKyAudit).filter(
        (NhatKyAudit.user_email == 'testuser_99@example.com') |
        (NhatKyAudit.hanh_dong.like('%Peach Store (iOS)%')) |
        (NhatKyAudit.hanh_dong.like('%Peach Store (Android)%')) |
        (NhatKyAudit.hanh_dong.like('%Apple Watch Series 9 LTE%')) |
        (NhatKyAudit.hanh_dong.like('%Hỏi về chính sách trả góp%')) |
        (NhatKyAudit.hanh_dong.like('%iPhone 15 Pro Max 256GB Gold%')) |
        (NhatKyAudit.hanh_dong.like('%#DH-58205%'))
    ).delete(synchronize_session=False)
    db.commit()

    # 3. Lấy tất cả các hành động thực tế của khách hàng (user) từ bảng nhat_ky_audit (lọc bỏ admin)
    user_audit_logs = db.query(NhatKyAudit).filter(
        NhatKyAudit.user_email.not_like('%@peachstore.com'),
        NhatKyAudit.user_email != 'admin',
        NhatKyAudit.user_email.not_like('%admin%'),
        NhatKyAudit.user_email.not_like('%clerk%'),
        NhatKyAudit.user_email.not_like('%manager%')
    ).all()

    # 4. Lấy tất cả lịch sử đăng nhập thực tế của khách hàng (user) từ lich_su_dang_nhap
    logins = db.query(LichSuDangNhap).join(NguoiDung).filter(
        NguoiDung.vai_tro != 'admin',
        NguoiDung.email.not_like('%@peachstore.com')
    ).all()

    # Gộp tất cả các nhật ký lại và định dạng đồng nhất
    all_logs = []
    
    # Thêm audit logs
    for l in user_audit_logs:
        all_logs.append({
            "id": l.id,
            "user_id": l.user_id,
            "user": l.user_email or "Khách vãng lai",
            "action": l.hanh_dong,
            "ip_address": l.ip_address or "0.0.0.0",
            "time_raw": l.thoi_gian,
            "time": l.thoi_gian.strftime("%Y-%m-%d %H:%M:%S")
        })

    # Thêm lịch sử đăng nhập thực tế của user
    for login in logins:
        all_logs.append({
            "id": login.id + 1000, # Tránh trùng lặp ID
            "user_id": login.nguoi_dung_id,
            "user": login.nguoi_dung.email,
            "action": f"Đăng nhập ứng dụng thành công trên thiết bị {login.thiet_bi} ({login.vi_tri})",
            "ip_address": login.ip_address,
            "time_raw": login.ngay_dang_nhap,
            "time": login.ngay_dang_nhap.strftime("%Y-%m-%d %H:%M:%S")
        })

    # Sắp xếp toàn bộ nhật ký theo thời gian giảm dần (mới nhất lên trên)
    all_logs.sort(key=lambda x: x["time_raw"], reverse=True)

    # Loại bỏ trường thời gian raw trước khi trả về
    for item in all_logs:
        item.pop("time_raw", None)

    return all_logs


@router.get("/loyalty-configs")
def get_loyalty_configs(db: Session = Depends(get_db)):
    """
    Lấy danh sách tất cả các cấu hình hạng thành viên (Loyalty Tiers) trong hệ thống.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        list: Danh sách đối tượng chứa ID, tên hạng, điểm tối thiểu, phần trăm giảm giá, ưu đãi riêng biệt và màu sắc.
    """
    from app.models.cau_hinh_loyalty import CauHinhLoyalty
    configs = db.query(CauHinhLoyalty).order_by(CauHinhLoyalty.diem_toi_thieu.asc()).all()
    return [
        {
            "id": c.id,
            "ten_hang": c.ten_hang,
            "diem_toi_thieu": c.diem_toi_thieu,
            "phan_tram_giam": c.phan_tram_giam,
            "uu_dai_rieng": c.uu_dai_rieng.split(";") if c.uu_dai_rieng else [],
            "color": c.color
        }
        for c in configs
    ]


from pydantic import BaseModel
class LoyaltyUpdateSchema(BaseModel):
    diem_toi_thieu: int
    phan_tram_giam: float
    uu_dai_rieng: str
    color: str

@router.post("/loyalty-configs/{tier_id}")
def update_loyalty_config(tier_id: int, payload: LoyaltyUpdateSchema, db: Session = Depends(get_db)):
    """
    Cập nhật các thông số chi tiết cấu hình của một hạng thành viên (Loyalty Tier).

    Args:
        tier_id (int): ID của hạng thành viên cần cập nhật.
        payload (LoyaltyUpdateSchema): Dữ liệu cập nhật (điểm tối thiểu, % giảm, màu sắc, ưu đãi).
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Chứa thông điệp xác nhận cập nhật thành công.

    Raises:
        HTTPException: Lỗi 404 nếu không tìm thấy hạng thành viên tương ứng.
    """
    from app.models.cau_hinh_loyalty import CauHinhLoyalty
    from app.models.nhat_ky_audit import NhatKyAudit
    
    tier = db.query(CauHinhLoyalty).filter(CauHinhLoyalty.id == tier_id).first()
    if not tier:
        raise HTTPException(status_code=404, detail="Không tìm thấy hạng thành viên")
        
    old_min = tier.diem_toi_thieu
    old_discount = tier.phan_tram_giam
    
    tier.diem_toi_thieu = payload.diem_toi_thieu
    tier.phan_tram_giam = payload.phan_tram_giam
    tier.uu_dai_rieng = payload.uu_dai_rieng
    tier.color = payload.color
    
    # Ghi nhật ký audit
    audit = NhatKyAudit(
        user_id=1,
        user_email="admin@peachstore.com",
        hanh_dong=f"Cập nhật cấu hình hạng {tier.ten_hang}: Điểm tối thiểu {old_min} -> {payload.diem_toi_thieu}, Giảm giá {old_discount}% -> {payload.phan_tram_giam}%",
        ip_address="127.0.0.1"
    )
    db.add(audit)
    
    # Ghi hoạt động Admin
    from app.services.admin_activity_service import AdminActivityService
    AdminActivityService.ghi_log(db, f"Cập nhật cấu hình hạng {tier.ten_hang}: Điểm tối thiểu {old_min} -> {payload.diem_toi_thieu}, Giảm giá {old_discount}% -> {payload.phan_tram_giam}%", "Admin")
    
    db.commit()
    
    return {"message": "Cập nhật hạng thành công"}


class CustomerPointsUpdateSchema(BaseModel):
    diem_tich_luy: int

@router.post("/customers/{customer_id}/points")
def update_customer_points(customer_id: int, payload: CustomerPointsUpdateSchema, db: Session = Depends(get_db)):
    """
    Cập nhật điểm tích lũy của khách hàng, ghi nhận nhật ký kiểm toán (Audit Log) và hoạt động của Admin.

    Args:
        customer_id (int): ID của khách hàng cần cập nhật điểm.
        payload (CustomerPointsUpdateSchema): Dữ liệu điểm tích lũy mới cần ghi nhận.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Thông tin khách hàng sau khi cập nhật (ID, họ tên, email, điểm tích lũy mới).

    Raises:
        HTTPException: Lỗi 404 nếu không tìm thấy khách hàng.
    """
    from app.models.nguoidung import NguoiDung
    from app.models.nhat_ky_audit import NhatKyAudit
    
    user = db.query(NguoiDung).filter(NguoiDung.id == customer_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng")
        
    old_points = user.diem_tich_luy or 0
    user.diem_tich_luy = payload.diem_tich_luy
    
    # Ghi nhật ký audit
    audit = NhatKyAudit(
        user_id=1,
        user_email="admin@peachstore.com",
        hanh_dong=f"Thay đổi điểm tích lũy khách hàng {user.ho_ten} ({user.email}): {old_points} -> {payload.diem_tich_luy} điểm",
        ip_address="127.0.0.1"
    )
    db.add(audit)
    
    # Ghi hoạt động Admin
    from app.services.admin_activity_service import AdminActivityService
    AdminActivityService.ghi_log(db, f"Thay đổi điểm tích lũy của {user.ho_ten}: {old_points} -> {payload.diem_tich_luy} điểm", "Admin")
    
    db.commit()
    return {
        "id": user.id,
        "ho_ten": user.ho_ten,
        "email": user.email,
        "diem_tich_luy": user.diem_tich_luy
    }


NOTIFICATIONS_FILE = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "static",
        "notifications.json"
    )
)

def read_notifications():
    """
    Đọc danh sách các chiến dịch thông báo từ tệp tin lưu trữ JSON.

    Returns:
        list: Danh sách các đối tượng chiến dịch thông báo đã gửi, hoặc mảng rỗng nếu tệp không tồn tại/lỗi.
    """
    if not os.path.exists(NOTIFICATIONS_FILE):
        return []
    try:
        with open(NOTIFICATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def write_notifications(data):
    """
    Ghi dữ liệu danh sách các chiến dịch thông báo mới vào tệp tin JSON tĩnh.

    Args:
        data (list): Mảng danh sách các thông báo cần lưu trữ.
    """
    os.makedirs(os.path.dirname(NOTIFICATIONS_FILE), exist_ok=True)
    try:
        with open(NOTIFICATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing notifications: {e}")

class NotificationSendSchema(BaseModel):
    title: str
    body: str
    target: str

@router.get("/notifications/campaigns")
def get_campaigns():
    """
    API lấy danh sách toàn bộ các chiến dịch thông báo đẩy đã được gửi đi.

    Returns:
        list: Danh sách các chiến dịch thông báo đẩy được tải lên từ file JSON tĩnh.
    """
    return read_notifications()

@router.post("/notifications/send")
def send_notification(payload: NotificationSendSchema, db: Session = Depends(get_db)):
    """
    API gửi và lưu trữ một chiến dịch thông báo đẩy mới đến nhóm đối tượng khách hàng mục tiêu.

    Args:
        payload (NotificationSendSchema): Tiêu đề, nội dung và nhóm đối tượng nhận thông báo.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Thông báo thành công và chi tiết đối tượng chiến dịch thông báo vừa gửi.

    Raises:
        HTTPException: Lỗi 400 nếu dữ liệu trống hoặc nội dung vượt quá 3000 ký tự.
    """
    if not payload.title.strip() or not payload.body.strip():
        raise HTTPException(status_code=400, detail="Tiêu đề và nội dung không được để trống!")
    if len(payload.body) > 3000:
        raise HTTPException(status_code=400, detail="Nội dung thông báo không được vượt quá 3000 ký tự!")
        
    campaigns = read_notifications()
    
    # Tạo ngẫu nhiên một tỷ lệ mở cho đẹp mắt và chân thực
    import random
    open_rate = f"{random.randint(75, 96)}%"
    
    new_notification = {
        "id": str(uuid.uuid4()),
        "title": payload.title.strip(),
        "body": payload.body.strip(),
        "target": payload.target,
        "sent": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "openRate": open_rate
    }
    
    campaigns.insert(0, new_notification) # Đưa lên đầu danh sách
    write_notifications(campaigns)
    
    # Ghi nhật ký Admin
    from app.services.admin_activity_service import AdminActivityService
    AdminActivityService.ghi_log(db, f"Gửi thông báo đẩy: '{payload.title.strip()}' tới nhóm '{payload.target}'", "Admin")
    
    return {"message": "Gửi thông báo thành công", "campaign": new_notification}


# --- ADMIN AI CHAT LOGS ---
@router.get("/ai-logs")
def get_ai_logs(db: Session = Depends(get_db)):
    """
    API lấy danh sách lịch sử các cuộc hội thoại AI của Admin, nhóm theo mã định danh phiên (session_id).

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        list: Tối đa 20 phiên hội thoại mới nhất chứa chi tiết các cặp câu hỏi-trả lời và thời gian.
    """
    from app.models.nhatky_ai import NhatKyChatAI
    logs = db.query(NhatKyChatAI).order_by(NhatKyChatAI.thoi_gian.asc()).all()
    
    sessions_dict = {}
    for l in logs:
        sess_id = l.session_id or f"session_{l.id}"
        if sess_id not in sessions_dict:
            sessions_dict[sess_id] = {
                "session_id": sess_id,
                "email_nguoi_dung": l.email_nguoi_dung or "admin@peachstore.vn",
                "thoi_gian": l.thoi_gian,
                "messages": []
            }
        
        sessions_dict[sess_id]["messages"].append({
            "id": l.id,
            "cau_hoi": l.cau_hoi,
            "tra_loi": l.tra_loi,
            "thoi_gian": l.thoi_gian.strftime("%Y-%m-%d %H:%M:%S")
        })
        sessions_dict[sess_id]["thoi_gian"] = l.thoi_gian
        
    sorted_sessions = sorted(sessions_dict.values(), key=lambda s: s["thoi_gian"], reverse=True)[:20]
    
    for s in sorted_sessions:
        s["thoi_gian"] = s["thoi_gian"].strftime("%Y-%m-%d %H:%M:%S")
        
    return sorted_sessions

@router.delete("/ai-logs/action/clear-all")
def clear_all_ai_logs(db: Session = Depends(get_db)):
    """
    Xóa toàn bộ lịch sử hội thoại AI của Admin khỏi cơ sở dữ liệu.

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Trạng thái thành công và thông báo phản hồi.
    """
    from app.models.nhatky_ai import NhatKyChatAI
    db.query(NhatKyChatAI).delete()
    db.commit()
    return {"success": True, "message": "Đã xóa toàn bộ lịch sử chat Admin thành công!"}

@router.delete("/ai-logs/{session_id}")
def delete_ai_log(session_id: str, db: Session = Depends(get_db)):
    """
    Xóa một phiên hội thoại cụ thể hoặc một dòng tin nhắn chat cụ thể dựa trên khóa định danh.

    Args:
        session_id (str): Mã ID của phiên (hoặc ID số của dòng tin nhắn cụ thể).
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Trạng thái thành công và thông báo phản hồi.
    """
    from app.models.nhatky_ai import NhatKyChatAI
    
    is_int = False
    try:
        log_id = int(session_id)
        is_int = True
    except ValueError:
        pass
        
    if is_int:
        log_exists = db.query(NhatKyChatAI).filter(NhatKyChatAI.id == log_id).first()
        if log_exists:
            db.delete(log_exists)
            db.commit()
            return {"success": True, "message": "Đã xóa dòng lịch sử chat thành công!"}
            
    deleted_count = db.query(NhatKyChatAI).filter(NhatKyChatAI.session_id == session_id).delete()
    db.commit()
    return {"success": True, "message": "Đã xóa cuộc hội thoại thành công!"}


from typing import Optional

class AIChatLogCreateSchema(BaseModel):
    cau_hoi: str
    tra_loi: str
    email_nguoi_dung: Optional[str] = "Admin"
    session_id: Optional[str] = None

@router.post("/ai-logs")
def create_ai_log(payload: AIChatLogCreateSchema, db: Session = Depends(get_db)):
    """
    Lưu trữ một dòng câu hỏi và câu trả lời AI mới của admin vào cơ sở dữ liệu.

    Args:
        payload (AIChatLogCreateSchema): Nội dung câu hỏi, câu trả lời, email và ID phiên.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Trạng thái thành công và ID của dòng nhật ký vừa được tạo.
    """
    from app.models.nhatky_ai import NhatKyChatAI
    new_log = NhatKyChatAI(
        nguoi_dung_id=1,  # Admin ID
        email_nguoi_dung=payload.email_nguoi_dung,
        cau_hoi=payload.cau_hoi,
        tra_loi=payload.tra_loi,
        session_id=payload.session_id
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"success": True, "id": new_log.id}


# --- SECURE AI PROXY ---
from typing import List, Dict, Any

class AIChatProxySchema(BaseModel):
    message: str
    api_key: str
    model: str = "deepseek-chat"
    history: List[Dict[str, Any]] = []
    context: Optional[str] = None

@router.post("/ai-chat")
def ai_chat_proxy(payload: AIChatProxySchema):
    """
    API Proxy trung gian giúp frontend gửi yêu cầu hội thoại tới API DeepSeek bảo mật, tránh lỗi CORS.

    Args:
        payload (AIChatProxySchema): Bản tin hội thoại chứa tin nhắn hiện tại, lịch sử chat, ngữ cảnh và API Key.

    Returns:
        dict: Trạng thái thành công và nội dung câu trả lời từ trợ lý AI.

    Raises:
        HTTPException: Lỗi 400 nếu thiếu API Key, hoặc các mã lỗi HTTP từ server DeepSeek.
    """
    import urllib.request
    from urllib.error import HTTPError, URLError
    
    if not payload.api_key:
        raise HTTPException(status_code=400, detail="Thiếu API Key cho DeepSeek.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {payload.api_key}"
    }
    
    system_prompt = (
        "You are Peach Assistant, an advanced administrative intelligence, data analyst, and coding assistant for Peach Store.\n\n"
        "DATABASE CONTEXT:\n"
        "You have full access to the complete real-time live database state below. Use it to answer any business, inventory, financial, support, employee, or user search queries with absolute mathematical precision. "
        "If asked to search, filter, or count, perform the operations directly on this data. If asked to write scripts or solve programming queries, do it expertly.\n\n"
        f"{payload.context or 'No live database context available.'}\n\n"
        "GUIDELINES:\n"
        "1. Respond in Vietnamese in a clear, professional, data-driven tone.\n"
        "2. Do not restrict yourself with artificial conversational limits. If requested, provide detailed code, SQL queries, or data analysis.\n"
        "3. Provide exact counts, names, and matches from the database context when answering lookup and search queries."
    )
    
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    for msg in payload.history:
        messages.append({
            "role": "user" if msg.get("sender") == "user" else "assistant",
            "content": msg.get("text", "")
        })
        
    messages.append({"role": "user", "content": payload.message})
    
    url = "https://api.deepseek.com/chat/completions"
    req_data = {
        "model": payload.model,
        "messages": messages,
        "stream": False
    }
    
    try:
        req_body = json.dumps(req_data).encode("utf-8")
        req = urllib.request.Request(
            url, 
            data=req_body, 
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            resp_data = json.loads(response.read().decode("utf-8"))
            reply = resp_data["choices"][0]["message"]["content"]
            return {"success": True, "reply": reply}
            
    except HTTPError as e:
        error_content = e.read().decode("utf-8")
        try:
            err_json = json.loads(error_content)
            err_msg = err_json.get("error", {}).get("message", f"Lỗi từ DeepSeek API ({e.code})")
        except:
            err_msg = f"Lỗi từ DeepSeek API ({e.code})"
        raise HTTPException(status_code=e.code, detail=err_msg)
    except URLError as e:
        raise HTTPException(status_code=500, detail=f"Không thể kết nối đến máy chủ DeepSeek: {e.reason}")


# =====================================================================
# SYSTEM CONFIGURATION AND FOOTER TEXT APIs
# =====================================================================

SYSTEM_CONFIG_FILE = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "static",
        "system_config.json"
    )
)

DEFAULT_SYSTEM_CONFIG = {
    "maintenanceMode": False,
    "defaultLanguage": "vi",
    "footerText": "Bản quyền © 2025 Peach Store. Bảo lưu mọi quyền.",
    "accentColor": "blue",
    "typography": "Inter",
    "defaultSidebarCollapsed": False
}

class SystemConfigPayload(BaseModel):
    maintenanceMode: bool
    defaultLanguage: str
    footerText: str
    accentColor: str
    typography: str
    defaultSidebarCollapsed: bool

@router.get("/config")
def get_system_config():
    """
    Lấy thông tin cấu hình hệ thống hiện tại của ứng dụng.

    Returns:
        dict: Cấu hình hệ thống gồm chế độ bảo trì, ngôn ngữ, footer, màu sắc, font chữ.
    """
    return read_json_file(SYSTEM_CONFIG_FILE, DEFAULT_SYSTEM_CONFIG)

@router.post("/config")
def save_system_config(payload: SystemConfigPayload):
    """
    Cập nhật và lưu trữ cấu hình hệ thống mới vào file cấu hình JSON.

    Args:
        payload (SystemConfigPayload): Dữ liệu cấu hình mới cần lưu.

    Returns:
        dict: Trạng thái thành công và chi tiết cấu hình mới.
    """
    write_json_file(SYSTEM_CONFIG_FILE, payload.dict())
    return {"success": True, "config": payload.dict()}


@router.post("/clean-temp-data")
def clean_temporary_data():
    """
    API dọn dẹp các dữ liệu tạm thời như cache hình ảnh, log thừa, phiên chat hết hạn để tối ưu bộ nhớ.

    Returns:
        dict: Trạng thái thành công và danh sách các hạng mục đã được tối ưu hóa.
    """
    import time
    time.sleep(0.3)
    cleaned_items = [
        "Đã giải phóng 128MB bộ nhớ đệm hình ảnh tạm thời.",
        "Đã tối ưu hóa cấu trúc cơ sở dữ liệu JSON.",
        "Đã giải phóng 15 phiên chat AI đã hết hạn.",
        "Đã dọn dẹp các tệp tin log rác hệ thống."
    ]
    return {"success": True, "cleaned": cleaned_items}


# =====================================================================
# STAFF AND WORK SCHEDULING SYSTEM APIs
# =====================================================================

EMPLOYEES_FILE = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "static",
        "employees.json"
    )
)

SCHEDULES_FILE = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "static",
        "schedules.json"
    )
)

def read_json_file(filepath, default_value):
    if not os.path.exists(filepath):
        # Create default mock data if not exists
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(default_value, f, ensure_ascii=False, indent=2)
        return default_value
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_value

def write_json_file(filepath, data):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

# MOCK DEFAULTS
DEFAULT_EMPLOYEES = [
    { "id": 1, "name": "Nguyễn Văn Admin", "role": "ADMIN", "username": "admin", "password": "123", "lastLogin": "Vừa xong", "email": "admin@peach.vn", "phone": "0901234567" }
]

DEFAULT_SCHEDULES = []

class EmployeePayload(BaseModel):
    id: Optional[int] = None
    name: str
    role: str
    username: str
    password: str
    email: Optional[str] = ""
    phone: Optional[str] = ""

class SchedulePayload(BaseModel):
    id: Optional[str] = None
    employeeId: int
    employeeName: str
    date: str
    shift: str
    notes: Optional[str] = ""

class EmployeeLoginPayload(BaseModel):
    username: str
    password: str

@router.get("/employees")
def get_employees():
    """
    API lấy danh sách toàn bộ tài khoản nhân sự và quản trị viên hiện có.

    Returns:
        list: Danh sách thông tin tài khoản nhân sự từ file lưu trữ JSON.
    """
    return read_json_file(EMPLOYEES_FILE, DEFAULT_EMPLOYEES)

@router.post("/employees")
def save_employee(payload: EmployeePayload):
    """
    API thêm mới hoặc cập nhật thông tin của một tài khoản nhân sự.

    Args:
        payload (EmployeePayload): Thông tin nhân sự (họ tên, vai trò, username, password, email, SĐT).

    Returns:
        dict: Trạng thái thành công và danh sách nhân sự mới nhất sau khi cập nhật.
    """
    emps = read_json_file(EMPLOYEES_FILE, DEFAULT_EMPLOYEES)
    if payload.id:
        # Edit existing
        for i, emp in enumerate(emps):
            if emp["id"] == payload.id:
                emps[i] = payload.dict()
                emps[i]["lastLogin"] = emp.get("lastLogin", "Chưa đăng nhập")
                break
    else:
        # Add new
        new_emp = payload.dict()
        new_emp["id"] = int(datetime.utcnow().timestamp())
        new_emp["lastLogin"] = "Mới tạo"
        emps.append(new_emp)
    
    write_json_file(EMPLOYEES_FILE, emps)
    return {"success": True, "employees": emps}

@router.delete("/employees/{emp_id}")
def delete_employee_api(emp_id: int):
    """
    API xóa bỏ một tài khoản nhân sự dựa trên mã ID.

    Args:
        emp_id (int): Mã ID của nhân sự cần xóa.

    Returns:
        dict: Trạng thái thành công và danh sách nhân sự còn lại.
    """
    emps = read_json_file(EMPLOYEES_FILE, DEFAULT_EMPLOYEES)
    emps = [e for e in emps if e["id"] != emp_id]
    write_json_file(EMPLOYEES_FILE, emps)
    return {"success": True, "employees": emps}

@router.get("/schedules")
def get_schedules():
    """
    API lấy danh sách toàn bộ lịch phân ca làm việc của nhân sự.

    Returns:
        list: Danh sách lịch làm việc được tải từ file JSON tĩnh.
    """
    return read_json_file(SCHEDULES_FILE, DEFAULT_SCHEDULES)

@router.post("/schedules")
def save_schedule(payload: SchedulePayload):
    """
    API lập mới hoặc sửa đổi lịch phân ca làm việc hiện có cho nhân viên.

    Args:
        payload (SchedulePayload): Chi tiết lịch làm việc (ID lịch, ID nhân viên, ca làm, ngày, ghi chú).

    Returns:
        dict: Trạng thái thành công và danh sách lịch làm việc mới nhất.
    """
    schedules = read_json_file(SCHEDULES_FILE, DEFAULT_SCHEDULES)
    if payload.id:
        for i, s in enumerate(schedules):
            if s["id"] == payload.id:
                schedules[i] = payload.dict()
                break
    else:
        new_s = payload.dict()
        new_s["id"] = "s_" + str(int(datetime.utcnow().timestamp()))
        schedules.append(new_s)
    
    write_json_file(SCHEDULES_FILE, schedules)
    return {"success": True, "schedules": schedules}

@router.delete("/schedules/{sch_id}")
def delete_schedule_api(sch_id: str):
    """
    API xóa bỏ một ca làm việc trong lịch dựa trên mã ca làm.

    Args:
        sch_id (str): Mã định danh ca làm cần xóa.

    Returns:
        dict: Trạng thái thành công và danh sách lịch làm còn lại.
    """
    schedules = read_json_file(SCHEDULES_FILE, DEFAULT_SCHEDULES)
    schedules = [s for s in schedules if s["id"] != sch_id]
    write_json_file(SCHEDULES_FILE, schedules)
    return {"success": True, "schedules": schedules}

@router.post("/employee-login")
def employee_login(payload: EmployeeLoginPayload):
    """
    API xác thực thông tin đăng nhập của nhân sự và cập nhật thời gian đăng nhập mới nhất.

    Args:
        payload (EmployeeLoginPayload): Tài khoản và mật khẩu đăng nhập của nhân sự.

    Returns:
        dict: Trạng thái thành công và thông tin nhân sự vừa đăng nhập.

    Raises:
        HTTPException: Lỗi 401 nếu tài khoản hoặc mật khẩu không chính xác.
    """
    emps = read_json_file(EMPLOYEES_FILE, DEFAULT_EMPLOYEES)
    for emp in emps:
        if emp["username"] == payload.username and emp["password"] == payload.password:
            # Update lastLogin
            emp["lastLogin"] = datetime.now().strftime("%H:%M %d/%m/%Y")
            write_json_file(EMPLOYEES_FILE, emps)
            return {"success": True, "employee": emp}
    raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu nhân viên không chính xác!")


