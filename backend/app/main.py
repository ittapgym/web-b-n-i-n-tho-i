from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import traceback
from .core.database import engine, Base
from .controllers import (
    xac_thuc,
    sanpham,
    admin,
    giohang,
    donhang,
    nguoidung,
    kho,
    voucher,
    shipping,
    payment,
    yeuthich,
)

# Tạo các bảng và xử lý Migration đơn giản
# Kết nối Database và Migration
try:
    print(">>> Đang kết nối Database PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    # Thử kết nối nhanh để kiểm tra trước khi migration
    with engine.connect() as conn:
        print(">>> Kết nối thành công. Đang kiểm tra Migration...")
        # Migration thủ công: Bổ sung các cột
        from sqlalchemy import text

        # ... (giữ nguyên các lệnh execute text)
        try:
            conn.execute(
                text(
                    "ALTER TABLE san_pham ADD COLUMN IF NOT EXISTS dung_luong VARCHAR(255) DEFAULT ''"
                )
            )
        except Exception as e:
            print(f">>> Migration warning (dung_luong): {e}")
        conn.execute(
            text(
                "ALTER TABLE san_pham ADD COLUMN IF NOT EXISTS ram VARCHAR(255) DEFAULT ''"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE gio_hang ADD COLUMN IF NOT EXISTS ram VARCHAR(255) DEFAULT ''"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE chi_tiet_don_hang ADD COLUMN IF NOT EXISTS ram VARCHAR(255) DEFAULT ''"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE san_pham ADD COLUMN IF NOT EXISTS thu_vien_anh JSON DEFAULT '[]'"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE san_pham ADD COLUMN IF NOT EXISTS is_new INTEGER DEFAULT 1"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE san_pham ADD COLUMN IF NOT EXISTS so_luong_kho INTEGER DEFAULT 100"
            )
        )
        conn.execute(
            text("ALTER TABLE don_hang ALTER COLUMN so_dien_thoai TYPE VARCHAR(50)")
        )
        conn.execute(
            text("ALTER TABLE don_hang ALTER COLUMN dia_chi TYPE VARCHAR(500)")
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS is_visible_user BOOLEAN DEFAULT TRUE"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS imei VARCHAR(50)"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS warranty_months INTEGER"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS ngay_hoan_thanh TIMESTAMP"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS diem_tich_luy INTEGER DEFAULT 0"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS hinh_anh VARCHAR(500)"
            )
        )
        
        # Tự động nạp ngay_hoan_thanh cho các đơn hàng cũ đã 'hoan_thanh' nhưng ngay_hoan_thanh bị NULL
        try:
            conn.execute(
                text("UPDATE don_hang SET ngay_hoan_thanh = ngay_tao WHERE trang_thai = 'hoan_thanh' AND ngay_hoan_thanh IS NULL")
            )
        except Exception as pop_err:
            print(f">>> Lỗi cập nhật ngay_hoan_thanh cũ: {pop_err}")
        
        # Tự động nạp IMEI cho các đơn hàng cũ chưa có
        try:
            rows = conn.execute(text("SELECT id, user_id FROM don_hang WHERE imei IS NULL OR imei = ''")).fetchall()
            if rows:
                import random
                import string
                for row in rows:
                    order_id = row[0]
                    user_id = row[1]
                    imei_digits = "".join(random.choices(string.digits, k=10))
                    imei_letters = "".join(random.choices(string.ascii_uppercase, k=2))
                    order_imei = f"{imei_digits}{imei_letters}"
                    
                    # Tính bảo hành theo điểm của khách hàng lúc đó
                    warranty_months = 6
                    if user_id:
                        user_res = conn.execute(text("SELECT diem_tich_luy FROM nguoi_dung WHERE id = :uid"), {"uid": user_id}).fetchone()
                        if user_res:
                            points = user_res[0] or 0
                            if points >= 5000:
                                warranty_months = 24
                            elif points >= 1000:
                                warranty_months = 12
                    
                    conn.execute(
                        text("UPDATE don_hang SET imei = :imei, warranty_months = :months WHERE id = :oid"),
                        {"imei": order_imei, "months": warranty_months, "oid": order_id}
                    )
                print(f">>> Đã tự động cập nhật IMEI cho {len(rows)} đơn hàng cũ thành công!")
        except Exception as migration_err:
            print(f">>> Lỗi cập nhật IMEI tự động: {migration_err}")

        # Migration cho hệ thống đặt hàng (Voucher, Shipping, Payment)
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS voucher (
                id SERIAL PRIMARY KEY,
                ma_voucher VARCHAR(50) UNIQUE NOT NULL,
                loai_giam_gia VARCHAR(20) NOT NULL DEFAULT 'phan_tram',
                gia_tri_giam FLOAT NOT NULL DEFAULT 0,
                don_hang_toi_thieu FLOAT NOT NULL DEFAULT 0,
                giam_toi_da FLOAT,
                ngay_het_han TIMESTAMP,
                so_luong_con_lai INTEGER NOT NULL DEFAULT 0,
                trang_thai VARCHAR(20) NOT NULL DEFAULT 'dang_hoat_dong',
                ngay_tao TIMESTAMP DEFAULT NOW()
            )
        """)
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS don_vi_van_chuyen (
                id SERIAL PRIMARY KEY,
                ten_don_vi VARCHAR(100) NOT NULL,
                ma_don_vi VARCHAR(50) UNIQUE NOT NULL,
                phi_co_dinh FLOAT NOT NULL DEFAULT 0,
                nguong_mien_phi FLOAT NOT NULL DEFAULT 0,
                thoi_gian_du_kien VARCHAR(100),
                mo_ta TEXT,
                kich_hoat BOOLEAN DEFAULT TRUE
            )
        """)
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS doi_tac_thanh_toan (
                id SERIAL PRIMARY KEY,
                ten_doi_tac VARCHAR(100) NOT NULL,
                ma_phuong_thuc VARCHAR(50) UNIQUE NOT NULL,
                loai_hinh VARCHAR(50) NOT NULL DEFAULT 'online',
                mo_ta TEXT,
                kich_hoat BOOLEAN DEFAULT TRUE
            )
        """)
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS yeu_thich (
                id SERIAL PRIMARY KEY,
                nguoi_dung_id INTEGER REFERENCES nguoi_dung(id) ON DELETE CASCADE NOT NULL,
                san_pham_id INTEGER REFERENCES san_pham(id) ON DELETE CASCADE NOT NULL,
                ngay_tao TIMESTAMP DEFAULT NOW(),
                UNIQUE(nguoi_dung_id, san_pham_id)
            )
        """)
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS lich_su_dang_nhap (
                id SERIAL PRIMARY KEY,
                nguoi_dung_id INTEGER REFERENCES nguoi_dung(id) ON DELETE CASCADE NOT NULL,
                thiet_bi VARCHAR(255) NOT NULL,
                ip_address VARCHAR(50) NOT NULL,
                vi_tri VARCHAR(100) NOT NULL,
                ngay_dang_nhap TIMESTAMP DEFAULT NOW()
            )
        """)
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS nhat_ky_audit (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                user_email VARCHAR(255),
                hanh_dong VARCHAR(500) NOT NULL,
                ip_address VARCHAR(50),
                thoi_gian TIMESTAMP DEFAULT NOW()
            )
        """)
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS hoat_dong_admin (
                id SERIAL PRIMARY KEY,
                nhan_vien VARCHAR(255) DEFAULT 'Admin',
                thao_tac VARCHAR(500) NOT NULL,
                thoi_gian TIMESTAMP DEFAULT NOW()
            )
        """)
        )
        # Tự động nạp các hoạt động Admin mẫu ban đầu nếu trống
        r_admin = conn.execute(text("SELECT COUNT(*) FROM hoat_dong_admin")).scalar()
        if r_admin == 0:
            conn.execute(text("""
                INSERT INTO hoat_dong_admin (nhan_vien, thao_tac, thoi_gian)
                VALUES 
                ('Admin', 'Vừa đăng nhập hệ thống', NOW() - INTERVAL '10 minutes'),
                ('Hệ thống', 'Đã đồng bộ dữ liệu sản phẩm', NOW() - INTERVAL '1 hour'),
                ('Admin', 'Đang kiểm tra báo cáo tháng', NOW() - INTERVAL '2 hours')
            """))

        # Tạo bảng nhật ký chat AI
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS nhat_ky_chat_ai (
                id SERIAL PRIMARY KEY,
                nguoi_dung_id INTEGER,
                email_nguoi_dung VARCHAR(255),
                cau_hoi TEXT NOT NULL,
                tra_loi TEXT NOT NULL,
                thoi_gian TIMESTAMP DEFAULT NOW(),
                session_id VARCHAR(50)
            )
        """)
        )
        conn.execute(
            text(
                "ALTER TABLE nhat_ky_chat_ai ADD COLUMN IF NOT EXISTS session_id VARCHAR(50)"
            )
        )
        # Tự động dọn dẹp các dòng dữ liệu chat mẫu cũ khỏi cơ sở dữ liệu
        conn.execute(
            text(
                "DELETE FROM nhat_ky_chat_ai WHERE email_nguoi_dung IN ('customer@peachstore.vn', 'vip_buyer@gmail.com', 'guest_user@outlook.com')"
            )
        )


        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS cau_hinh_loyalty (
                id SERIAL PRIMARY KEY,
                ten_hang VARCHAR(50) UNIQUE NOT NULL,
                diem_toi_thieu INTEGER NOT NULL DEFAULT 0,
                phan_tram_giam FLOAT NOT NULL DEFAULT 0.0,
                uu_dai_rieng TEXT,
                color VARCHAR(7) NOT NULL DEFAULT '#8e8e93'
            )
        """)
        )
        # Tự động nạp cấu hình Loyalty mặc định nếu bảng trống
        r = conn.execute(text("SELECT COUNT(*) FROM cau_hinh_loyalty")).scalar()
        if r == 0:
            conn.execute(text("""
                INSERT INTO cau_hinh_loyalty (ten_hang, diem_toi_thieu, phan_tram_giam, uu_dai_rieng, color)
                VALUES 
                ('Bạc', 0, 0.0, 'Tích điểm mua sắm;Hỗ trợ tiêu chuẩn;Đổi trả hàng trong 30 ngày', '#8e8e93'),
                ('Vàng', 1000, 5.0, 'Tích điểm mua sắm;Hỗ trợ ưu tiên;Đổi trả hàng trong 30 ngày', '#ffcc00'),
                ('Kim cương', 5000, 10.0, 'Tích điểm mua sắm;Đặc quyền Hỗ trợ VIP 24/7;Miễn phí vận chuyển mọi đơn hàng;Đổi trả hàng trong 30 ngày;Trải nghiệm sớm sản phẩm mới', '#007aff')
            """))
        else:
            # Clean up existing rows from redundant discount text since it is already custom configured
            conn.execute(text("""
                UPDATE cau_hinh_loyalty 
                SET uu_dai_rieng = REPLACE(REPLACE(uu_dai_rieng, 'Giảm giá 5% toàn cửa hàng;', ''), ';Giảm giá 5% toàn cửa hàng', '')
                WHERE uu_dai_rieng LIKE '%Giảm giá 5% toàn cửa hàng%';
                
                UPDATE cau_hinh_loyalty 
                SET uu_dai_rieng = REPLACE(REPLACE(uu_dai_rieng, 'Giảm giá 10% toàn cửa hàng;', ''), ';Giảm giá 10% toàn cửa hàng', '')
                WHERE uu_dai_rieng LIKE '%Giảm giá 10% toàn cửa hàng%';
            """))
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS phuong_thuc_thanh_toan VARCHAR(50)"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS phuong_thuc_van_chuyen VARCHAR(50)"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS phi_ship FLOAT DEFAULT 0"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS giam_gia_voucher FLOAT DEFAULT 0"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS voucher_id INTEGER REFERENCES voucher(id) ON DELETE SET NULL"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS ngay_cap_nhat TIMESTAMP DEFAULT NOW()"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS ma_pin VARCHAR(255) DEFAULT NULL"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS yeu_cau_pin BOOLEAN DEFAULT FALSE"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS ten_doanh_nghiep VARCHAR(255) DEFAULT NULL"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS ma_so_thue VARCHAR(100) DEFAULT NULL"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS dia_chi_kd VARCHAR(255) DEFAULT NULL"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS linh_vuc_kd VARCHAR(100) DEFAULT NULL"
            )
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS tin_nhan_chat (
                id SERIAL PRIMARY KEY,
                nguoi_dung_id INTEGER REFERENCES nguoi_dung(id) ON DELETE CASCADE NOT NULL,
                nguoi_gui VARCHAR(50) NOT NULL,
                noi_dung TEXT NOT NULL,
                thoi_gian TIMESTAMP DEFAULT NOW()
            )
        """)
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS yeu_cau_doanh_nghiep (
                id SERIAL PRIMARY KEY,
                nguoi_dung_id INTEGER REFERENCES nguoi_dung(id) ON DELETE CASCADE NOT NULL,
                ten_doanh_nghiep VARCHAR(255) NOT NULL,
                ma_so_thue VARCHAR(100) NOT NULL,
                dia_chi_kd VARCHAR(255) NOT NULL,
                linh_vuc_kd VARCHAR(100) NOT NULL,
                trang_thai VARCHAR(50) DEFAULT 'cho_duyet',
                ngay_tao TIMESTAMP DEFAULT NOW(),
                ngay_duyet TIMESTAMP NULL
            )
        """)
        )
        conn.commit()

    print(">>> Database & Migration: OK.")
except Exception as e:
    print(f"\n[!] LOI KET NOI DATABASE: {e}")
    print("[!] Vui lòng kiểm tra dịch vụ PostgreSQL đã được bật chưa.\n")

app = FastAPI(title="Peach Store API", openapi_version="3.0.3")


# Global Exception Handler để debug lỗi 500
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    print(f"\n{'!' * 20} LOI HE THONG {'!' * 20}")
    error_msg = traceback.format_exc()
    print(error_msg)
    print(f"{'!' * 54}\n")
    return JSONResponse(
        status_code=500, content={"detail": str(exc), "traceback": error_msg}
    )


# Cấu hình CORS - Cho phép tất cả origin để tránh lỗi CORS khi deploy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files - Đảm bảo đường dẫn tuyệt đối chuẩn hóa
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.normpath(os.path.join(BASE_DIR, "static"))
upload_path = os.path.normpath(os.path.join(static_path, "uploads"))

# Tạo thư mục nếu chưa có
if not os.path.exists(upload_path):
    os.makedirs(upload_path, exist_ok=True)
    # Tạo thêm thư mục avatars nếu chưa có
    os.makedirs(os.path.join(upload_path, "avatars"), exist_ok=True)

app.mount("/static", StaticFiles(directory=static_path), name="static")

# Them router
app.include_router(xac_thuc.router)
app.include_router(sanpham.router)
app.include_router(admin.router)
app.include_router(giohang.router)
app.include_router(donhang.router)
app.include_router(nguoidung.router)
app.include_router(kho.router)
app.include_router(voucher.router)
app.include_router(shipping.router)
app.include_router(payment.router)
app.include_router(yeuthich.router)


@app.get("/")
def read_root():
    return {"message": "Chao mung den voi Peach Store API (PostgreSQL)"}
