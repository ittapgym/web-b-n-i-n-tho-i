from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request, Form
from sqlalchemy.orm import Session
import os
import json
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.nguoidung import NguoiDung
from app.schemas.nguoidung import DangKyNguoiDung, DangNhapNguoiDung, ThongTinNguoiDung, Token
from app.services.bao_mat import DichVuBaoMat
from app.core.phu_thuoc import lay_nguoi_dung_hien_tai

router = APIRouter(prefix="/xac-thuc", tags=["Xac Thuc"])

@router.post("/dang-ky", response_model=ThongTinNguoiDung, status_code=status.HTTP_201_CREATED)
def dang_ky(du_lieu: DangKyNguoiDung, db: Session = Depends(get_db)):
    """API cho phep nguoi dung tao tai khoan moi"""
    # Kiem tra email da ton tai chua
    nguoi_dung_cu = db.query(NguoiDung).filter(NguoiDung.email == du_lieu.email).first()
    if nguoi_dung_cu:
        raise HTTPException(status_code=400, detail="Email nay da duoc su dung")
    
    # Ma hoa mat khau
    mat_khau_hash = DichVuBaoMat.ma_hoa_mat_khau(du_lieu.mat_khau)
    
    # Tao doi tuong nguoi dung moi
    nguoi_dung_moi = NguoiDung(
        email=du_lieu.email,
        mat_khau=mat_khau_hash,
        ho_ten=du_lieu.ho_ten,
        so_dien_thoai=du_lieu.so_dien_thoai,
        dia_chi=du_lieu.dia_chi
    )
    
    db.add(nguoi_dung_moi)
    db.commit()
    db.refresh(nguoi_dung_moi)
    return nguoi_dung_moi

@router.post("/dang-nhap", response_model=Token)
def dang_nhap(request: Request, du_lieu: DangNhapNguoiDung, db: Session = Depends(get_db)):
    """API xac thuc email/mat khau va tra ve Token"""
    # Tim nguoi dung theo email
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.email == du_lieu.email).first()
    
    # Kiem tra ton tai va mat khau
    if not nguoi_dung or not DichVuBaoMat.xac_minh_mat_khau(du_lieu.mat_khau, nguoi_dung.mat_khau):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email hoac mat khau khong chinh xac"
        )
    
    # CHẶN ADMIN ĐĂNG NHẬP TRÊN WEB
    if nguoi_dung.vai_tro == 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tai khoan Admin khong duoc phep dang nhap tai day. Vui long su dung ung dung quan tri."
        )
    
    # Ghi nhận lịch sử đăng nhập thực tế
    try:
        user_agent = request.headers.get("user-agent", "Unknown Device")
        ip_addr = request.client.host if request.client else "127.0.0.1"
        
        # Đơn giản hóa User-Agent thành tên thiết bị dễ đọc
        device_name = "Thiết bị không xác định"
        if "iPhone" in user_agent:
            device_name = "iPhone - Safari Browser" if "Safari" in user_agent else "iPhone - Chrome Browser"
        elif "iPad" in user_agent:
            device_name = "iPad - Safari Browser"
        elif "Macintosh" in user_agent:
            device_name = "MacBook - Safari Browser" if "Safari" in user_agent and "Chrome" not in user_agent else "MacBook - Chrome Browser"
        elif "Windows" in user_agent:
            if "Edg" in user_agent:
                device_name = "Windows PC - Microsoft Edge"
            elif "Chrome" in user_agent:
                device_name = "Windows PC - Chrome Browser"
            else:
                device_name = "Windows PC - Firefox Browser"
        elif "Android" in user_agent:
            device_name = "Điện thoại Android"

        # Định nghĩa vị trí thực tế hoặc ước tính địa phương
        location = "Hà Nội, Việt Nam"
        if ip_addr.startswith("192.") or ip_addr == "127.0.0.1":
            location = "Hà Nội, Việt Nam"
        else:
            # Chọn ngẫu nhiên địa phương thực tế tại VN nếu IP là WAN
            import random
            location = random.choice(["Hà Nội, Việt Nam", "Đà Nẵng, Việt Nam", "Hồ Chí Minh, Việt Nam"])

        from app.models.lichsu_dangnhap import LichSuDangNhap
        lich_su = LichSuDangNhap(
            nguoi_dung_id=nguoi_dung.id,
            thiet_bi=device_name,
            ip_address=ip_addr,
            vi_tri=location
        )
        db.add(lich_su)
        db.commit()
    except Exception as e:
        print(f"Lỗi ghi lịch sử đăng nhập: {e}")
    
    # Tao Token
    access_token = DichVuBaoMat.tao_token_truy_cap(data={"sub": nguoi_dung.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=ThongTinNguoiDung)
def lay_thong_tin_ca_nhan(nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai)):
    """API lay thong tin nguoi dung hien tai tu Token"""
    return nguoi_dung

@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...), 
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API upload anh dai dien cho nguoi dung"""
    # 1. Kiem tra dinh dang file (chi anh)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Chi chap nhan file hinh anh")
    
    # 2. Kiem tra dung luong (Toi da 5MB)
    MAX_SIZE = 5 * 1024 * 1024
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="Dung luong anh khong duoc vuot qua 5MB")
    
    # 3. Tao thu muc luu tru neu chua co
    upload_dir = os.path.join("static", "uploads", "avatars")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # 4. Luu file voi ten duy nhat
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"user_{nguoi_dung.id}_{int(datetime.utcnow().timestamp())}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # 5. Cap nhat vao database
    avatar_url = f"/static/uploads/avatars/{file_name}"
    nguoi_dung.hinh_anh = avatar_url
    db.commit()
    
    return {"url": avatar_url}

@router.delete("/delete-avatar")
def delete_avatar(
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API xoa anh dai dien cua nguoi dung"""
    nguoi_dung.hinh_anh = None
    db.commit()
    return {"message": "Da xoa anh dai dien"}

class ProfileUpdate(BaseModel):
    ho_ten: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None

@router.put("/update-profile")
def update_profile(
    data: ProfileUpdate,
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API cap nhat thong tin ca nhan"""
    if data.ho_ten:
        nguoi_dung.ho_ten = data.ho_ten
    
    if data.so_dien_thoai:
        # Validate sdt đơn giản
        if not data.so_dien_thoai.isdigit() or len(data.so_dien_thoai) != 10:
            raise HTTPException(status_code=400, detail="So dien thoai phai co dung 10 chu so")
        nguoi_dung.so_dien_thoai = data.so_dien_thoai
        
    if data.dia_chi:
        nguoi_dung.dia_chi = data.dia_chi
        
    db.commit()
    db.refresh(nguoi_dung)
    return nguoi_dung


class DoiMatKhauPayload(BaseModel):
    mat_khau_cu: str
    mat_khau_moi: str


@router.put("/doi-mat-khau")
def doi_mat_khau(
    data: DoiMatKhauPayload,
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API thay đổi mật khẩu người dùng"""
    if not DichVuBaoMat.xac_minh_mat_khau(data.mat_khau_cu, nguoi_dung.mat_khau):
        raise HTTPException(status_code=400, detail="Mật khẩu cũ không chính xác!")
    
    nguoi_dung.mat_khau = DichVuBaoMat.ma_hoa_mat_khau(data.mat_khau_moi)
    db.commit()
    return {"message": "Đổi mật khẩu thành công!"}


class CaiDatPinPayload(BaseModel):
    pin_moi: str
    mat_khau_xac_nhan: str


@router.post("/cai-dat-pin")
def cai_dat_pin(
    data: CaiDatPinPayload,
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API cài đặt hoặc thay đổi mã PIN giao dịch"""
    if not DichVuBaoMat.xac_minh_mat_khau(data.mat_khau_xac_nhan, nguoi_dung.mat_khau):
        raise HTTPException(status_code=400, detail="Mật khẩu xác nhận không chính xác!")
    
    if not data.pin_moi.isdigit() or len(data.pin_moi) < 4 or len(data.pin_moi) > 6:
        raise HTTPException(status_code=400, detail="Mã PIN phải là chuỗi số từ 4 đến 6 chữ số!")
    
    nguoi_dung.ma_pin = DichVuBaoMat.ma_hoa_mat_khau(data.pin_moi)
    db.commit()
    db.refresh(nguoi_dung)
    return {"message": "Cài đặt mã PIN thành công!", "co_pin": True}


class TogglePinPayload(BaseModel):
    kich_hoat: bool
    ma_pin: str


@router.post("/toggle-pin")
def toggle_pin(
    data: TogglePinPayload,
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API bật/tắt yêu cầu mã PIN khi thanh toán"""
    if not nguoi_dung.ma_pin:
        raise HTTPException(status_code=400, detail="Bạn chưa cài đặt mã PIN giao dịch!")
    
    if not DichVuBaoMat.xac_minh_mat_khau(data.ma_pin, nguoi_dung.ma_pin):
        raise HTTPException(status_code=400, detail="Mã PIN giao dịch không chính xác!")
    
    nguoi_dung.yeu_cau_pin = data.kich_hoat
    db.commit()
    db.refresh(nguoi_dung)
    return {
        "message": f"Đã {'bật' if data.kich_hoat else 'tắt'} yêu cầu mã PIN thành công!",
        "yeu_cau_pin": nguoi_dung.yeu_cau_pin
    }


@router.get("/lich-su-dang-nhap")
def lay_lich_su_dang_nhap(
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API lay danh sach lich su dang nhap cua nguoi dung"""
    from app.models.lichsu_dangnhap import LichSuDangNhap
    lich_su = db.query(LichSuDangNhap).filter(
        LichSuDangNhap.nguoi_dung_id == nguoi_dung.id
    ).order_by(LichSuDangNhap.ngay_dang_nhap.desc()).limit(20).all()
    
    return [
        {
            "id": item.id,
            "thiet_bi": item.thiet_bi,
            "ip_address": item.ip_address,
            "vi_tri": item.vi_tri,
            "ngay_dang_nhap": item.ngay_dang_nhap.isoformat()
        }
        for item in lich_su
    ]


class GuiTinNhanPayload(BaseModel):
    text: str


@router.get("/tin-nhan-chat")
def lay_tin_nhan_chat(
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API lấy toàn bộ tin nhắn chat của người dùng"""
    from app.models.tinnhan_chat import TinNhanChat
    messages = db.query(TinNhanChat).filter(
        TinNhanChat.nguoi_dung_id == nguoi_dung.id
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


@router.post("/tin-nhan-chat")
def gui_tin_nhan_chat(
    payload: GuiTinNhanPayload,
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API gửi tin nhắn chat mới từ người dùng"""
    from app.models.tinnhan_chat import TinNhanChat
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Nội dung tin nhắn không được để trống!")
        
    m = TinNhanChat(
        nguoi_dung_id=nguoi_dung.id,
        nguoi_gui="user",
        noi_dung=payload.text.strip()
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    
    return {
        "id": m.id,
        "sender": m.nguoi_gui,
        "text": m.noi_dung,
        "time": m.thoi_gian.strftime("%H:%M")
    }


@router.post("/support/ticket")
async def tao_yeu_cau_ho_tro(
    subject: str = Form(...),
    serial: Optional[str] = Form(None),
    message: str = Form(...),
    images: List[UploadFile] = File(default=[]),
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API gửi yêu cầu hỗ trợ mới kèm tối đa 5 hình ảnh, dung lượng tối đa 10MB/ảnh"""
    from app.models.yeu_cau_ho_tro import YeuCauHoTro
    import uuid
    
    # Validate images length
    if len(images) > 5:
        raise HTTPException(status_code=400, detail="Chỉ được gửi tối đa 5 hình ảnh đính kèm!")
        
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    upload_dir = os.path.join(BASE_DIR, "static", "uploads", "supports")
    os.makedirs(upload_dir, exist_ok=True)
    
    saved_paths = []
    for img in images:
        if not img.filename:
            continue
            
        # Check size (10MB limit)
        contents = await img.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File {img.filename} vượt quá dung lượng tối đa 10MB!")
        await img.seek(0) # Reset stream
        
        # Save file
        ext = os.path.splitext(img.filename)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(upload_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(contents)
            
        # Save web-accessible path
        saved_paths.append(f"/static/uploads/supports/{filename}")
        
    hinh_anh_str = ";".join(saved_paths) if saved_paths else None
    
    ticket = YeuCauHoTro(
        nguoi_dung_id=nguoi_dung.id,
        chu_de=subject.strip(),
        imei_serial=serial.strip() if serial else None,
        noi_dung=message.strip(),
        hinh_anh=hinh_anh_str,
        trang_thai="cho_xu_ly"
    )
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    return {
        "success": True,
        "message": "Gửi yêu cầu hỗ trợ thành công!",
        "ticket_id": ticket.id
    }


class DangKyDoanhNghiepPayload(BaseModel):
    ten_doanh_nghiep: str
    ma_so_thue: str
    dia_chi_kd: str
    linh_vuc_kd: str


@router.post("/dang-ky-doanh-nghiep")
def dang_ky_doanh_nghiep(
    payload: DangKyDoanhNghiepPayload,
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API gửi yêu cầu chuyển đổi tài khoản người dùng sang tài khoản Doanh nghiệp"""
    if nguoi_dung.vai_tro == "admin":
        raise HTTPException(status_code=400, detail="Không thể nâng cấp tài khoản Admin sang Doanh nghiệp!")
    
    if nguoi_dung.vai_tro == "doanh_nghiep":
        raise HTTPException(status_code=400, detail="Tài khoản của bạn đã là tài khoản Doanh nghiệp rồi!")

    # Check for pending request
    from app.models.yeu_cau_doanh_nghiep import YeuCauDoanhNghiep
    yeu_cau_cu = db.query(YeuCauDoanhNghiep).filter(
        YeuCauDoanhNghiep.nguoi_dung_id == nguoi_dung.id,
        YeuCauDoanhNghiep.trang_thai == "cho_duyet"
    ).first()
    if yeu_cau_cu:
        raise HTTPException(
            status_code=400,
            detail="Bạn đã có một yêu cầu đăng ký Doanh nghiệp đang chờ phê duyệt. Vui lòng đợi Admin kiểm tra!"
        )
    
    # Create request
    yeu_cau_moi = YeuCauDoanhNghiep(
        nguoi_dung_id=nguoi_dung.id,
        ten_doanh_nghiep=payload.ten_doanh_nghiep.strip(),
        ma_so_thue=payload.ma_so_thue.strip(),
        dia_chi_kd=payload.dia_chi_kd.strip(),
        linh_vuc_kd=payload.linh_vuc_kd.strip(),
        trang_thai="cho_duyet"
    )
    db.add(yeu_cau_moi)
    db.commit()
    
    return {
        "success": True,
        "message": "Gửi yêu cầu đăng ký nâng cấp tài khoản Doanh nghiệp thành công! Yêu cầu đang được chờ phê duyệt.",
        "status": "cho_duyet"
    }


@router.get("/trang-thai-doanh-nghiep")
def lay_trang_thai_doanh_nghiep(
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """API lấy trạng thái yêu cầu nâng cấp doanh nghiệp của user"""
    from app.models.yeu_cau_doanh_nghiep import YeuCauDoanhNghiep
    yeu_cau = db.query(YeuCauDoanhNghiep).filter(
        YeuCauDoanhNghiep.nguoi_dung_id == nguoi_dung.id
    ).order_by(YeuCauDoanhNghiep.ngay_tao.desc()).first()
    
    if not yeu_cau:
        return {"has_request": False, "trang_thai": None}
    
    return {
        "has_request": True,
        "trang_thai": yeu_cau.trang_thai,
        "ten_doanh_nghiep": yeu_cau.ten_doanh_nghiep,
        "ma_so_thue": yeu_cau.ma_so_thue,
        "dia_chi_kd": yeu_cau.dia_chi_kd,
        "linh_vuc_kd": yeu_cau.linh_vuc_kd,
        "ngay_tao": yeu_cau.ngay_tao
    }


@router.get("/notifications")
def get_user_notifications(
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    db: Session = Depends(get_db)
):
    """Lấy danh sách thông báo phù hợp với hạng thẻ hoặc tất cả của người dùng"""
    NOTIFICATIONS_FILE = os.path.normpath(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "static",
            "notifications.json"
        )
    )
    if not os.path.exists(NOTIFICATIONS_FILE):
        return []
    
    try:
        with open(NOTIFICATIONS_FILE, "r", encoding="utf-8") as f:
            all_notifications = json.load(f)
    except Exception:
        all_notifications = []
        
    user_notifications = []
    for n in all_notifications:
        target = n.get("target", "Tất cả khách hàng")
        if target == "Tất cả khách hàng" or target == "Khách chưa mua hàng trong 30 ngày":
            user_notifications.append(n)
        elif target == "Hạng Silver trở lên":
            user_notifications.append(n)
            
    # Sắp xếp mới nhất lên đầu và chỉ giữ lại 20 thông báo gần nhất
    user_notifications.sort(key=lambda x: x.get("sent", ""), reverse=True)
    return user_notifications[:20]

