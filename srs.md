# 🍑 PHIẾU ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)

## PEACH STORE - HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ BÁN ĐIỆN THOẠI & PHỤ KIỆN

| Thông tin | Chi tiết |
|-----------|----------|
| **Tên dự án** | Peach Store - Hệ thống bán hàng điện thoại & phụ kiện trực tuyến |
| **Phiên bản** | 1.0.0 |
| **Công ty phát triển** | Peach Studio |
| **Thời gian ban hành** | 05/2026 |
| **Địa điểm** | TP. Hồ Chí Minh, Việt Nam |

---

## MỤC LỤC

1. [Giới thiệu](#1-giới-thiệu)
2. [Mô tả tổng quan hệ thống](#2-mô-tả-tổng-quan-hệ-thống)
3. [Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
4. [Phân hệ Frontend (Web)](#4-phân-hệ-frontend-web)
5. [Phân hệ Backend (API)](#5-phân-hệ-backend-api)
6. [Phân hệ Admin (Peach Admin)](#6-phân-hệ-admin-peach-admin)
7. [Các Use Case chi tiết](#7-các-use-case-chi-tiết)
8. [Thiết kế dữ liệu](#8-thiết-kế-dữ-liệu)
9. [Luồng công việc (Workflows)](#9-luồng-công-việc-workflows)
10. [Yêu cầu phi chức năng](#10-yêu-cầu-phi-chức-năng)
11. [Phụ lục](#11-phụ-lục)

---

## LỊCH SỬ CHỈNH SỬA (Record of Change)

| Ngày | Phiên bản | Mô tả thay đổi | Phân loại |
|------|-----------|----------------|-----------|
| 19/05/2026 | 1.0.0 | Phiên bản đầu tiên - Đặc tả toàn bộ hệ thống Peach Store | A |

*Phân loại: (A) = Thêm mới, (M) = Sửa đổi, (D) = Xóa*

---

## 1. Giới thiệu

### 1.1. Mục đích
Tài liệu này mô tả chi tiết các yêu cầu chức năng và phi chức năng cho hệ thống thương mại điện tử **Peach Store** - nền tảng bán điện thoại di động, máy tính bảng, laptop và phụ kiện công nghệ trực tuyến.

### 1.2. Phạm vi
Hệ thống bao gồm 3 phân hệ chính:
- **Web Frontend**: Giao diện người dùng (Vue 3 + Vite)
- **Backend API**: Xử lý nghiệp vụ (FastAPI + PostgreSQL)
- **Peach Admin**: Trang quản trị nội bộ (Electron-based)

### 1.3. Đối tượng sử dụng
| Đối tượng | Mô tả |
|-----------|-------|
| **Khách hàng (Customer)** | Người mua hàng, có thể đăng ký/đăng nhập, xem sản phẩm, đặt hàng, thanh toán |
| **Admin** | Quản trị viên hệ thống, quản lý sản phẩm, đơn hàng, khách hàng, voucher |
| **Nhân viên (Employee)** | Nhân viên cửa hàng, có lịch làm việc, hỗ trợ khách hàng |

---

## 2. Mô tả tổng quan hệ thống

### 2.1. Sơ đồ tổng quan

```
┌─────────────────────────────────────────────────────────────┐
│                    NGƯỜI DÙNG (User)                        │
├──────────────────────┬──────────────────┬───────────────────┤
│   Khách hàng         │   Admin          │   Nhân viên       │
│   (Web)              │   (Electron App) │   (Web)           │
├──────────┬───────────┴──────────────────┴───────────────────┤
│          │                                                    │
│  ┌───────▼────────┐  ┌─────────────────┐  ┌───────────────┐ │
│  │  Frontend      │  │  Peach Admin    │  │ Employee App  │ │
│  │  (Vue 3/Vite)  │  │  (HTML/JS/CSS)  │  │ (Same as Web) │ │
│  └───────┬────────┘  └────────┬────────┘  └───────┬───────┘ │
│          │                    │                    │         │
│          └────────────────────┼────────────────────┘         │
│                               │                              │
│                      ┌────────▼────────┐                    │
│                      │   Backend API   │                    │
│                      │   (FastAPI)     │                    │
│                      └────────┬────────┘                    │
│                               │                              │
│                      ┌────────▼────────┐                    │
│                      │   PostgreSQL    │                    │
│                      └─────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2. Các module chính

| Module | Phân hệ | Mô tả |
|--------|---------|-------|
| Xác thực & Người dùng | Backend | Đăng ký, đăng nhập, JWT token, quản lý hồ sơ |
| Sản phẩm | Backend + Web | Danh mục sản phẩm, tìm kiếm, lọc, chi tiết |
| Giỏ hàng | Backend + Web | Thêm/xóa/sửa sản phẩm trong giỏ |
| Đơn hàng | Backend + Web | Đặt hàng, theo dõi trạng thái, lịch sử |
| Thanh toán | Backend | Xử lý thanh toán, đối tác thanh toán |
| Vận chuyển | Backend | Quản lý đơn vị vận chuyển, phí ship |
| Voucher | Backend | Mã giảm giá, khuyến mãi |
| Yêu thích | Backend + Web | Danh sách sản phẩm yêu thích |
| Hỗ trợ | Backend + Web + Admin | Ticket hỗ trợ, chat, yêu cầu khôi phục |
| Admin Dashboard | Admin | Thống kê, quản lý toàn bộ hệ thống |
| AI Chat | Admin | Tích hợp DeepSeek AI hỗ trợ admin |
| Loyalty | Admin | Quản lý cấp bậc thành viên, tích điểm |
| Audit Log | Admin | Nhật ký hoạt động admin |

---

## 3. Kiến trúc hệ thống

### 3.1. Công nghệ sử dụng

| Thành phần | Công nghệ | Mục đích |
|------------|-----------|----------|
| Frontend Framework | Vue 3 (Composition API) | Xây dựng giao diện web |
| Build Tool | Vite | Bundle và dev server |
| Backend Framework | FastAPI (Python) | RESTful API server |
| Database | PostgreSQL | Lưu trữ dữ liệu |
| Admin UI | HTML + CSS + Vanilla JS | Giao diện quản trị nhẹ |
| Authentication | JWT (HS256) | Xác thực người dùng |
| AI Integration | DeepSeek API | Chat AI hỗ trợ admin |
| Hosting | Render (Backend + Database) | Triển khai cloud |

### 3.2. Cấu trúc thư mục

```
d:/peach_store/
├── backend/                    # FastAPI Backend
│   └── app/
│       ├── controllers/        # API endpoints (11 files)
│       ├── models/             # SQLAlchemy models (17 files)
│       ├── services/           # Business logic (7 files)
│       ├── schemas/            # Pydantic schemas (7 files)
│       ├── core/               # Config, database setup
│       └── main.py             # App entry point
├── frontend/                   # Vue 3 Web App
│   └── src/
│       ├── views/              # Page components (15 files)
│       ├── components/         # Reusable components
│       ├── stores/             # Pinia stores
│       ├── router/             # Vue Router config
│       ├── services/           # API services
│       └── utils/              # Utilities
└── peach_admin/                # Admin Electron App
    ├── src/views/              # Admin pages (HTML)
    ├── src/viewmodels/         # ViewModel logic (JS)
    └── js/                     # Admin scripts
```

---

## 4. Phân hệ Frontend (Web)

### 4.1. Danh sách màn hình & tuyến đường

| STT | Tên màn hình | Route | Component | Mô tả |
|-----|-------------|-------|-----------|-------|
| 1 | Trang Chủ | `/` | TrangChu.vue | Banner, danh sách sản phẩm nổi bật, danh mục |
| 2 | Đăng Nhập | `/login` | DangNhap.vue | Form đăng nhập khách hàng |
| 3 | Đăng Ký | `/dang-ky` | DangKy.vue | Form đăng ký tài khoản mới |
| 4 | Điện Thoại | `/dien-thoai` | DienThoai.vue | Danh sách điện thoại, lọc theo hãng/giá |
| 5 | Máy Tính Bảng | `/may-tinh-bang` | MayTinhBang.vue | Danh sách tablet |
| 6 | Laptop | `/laptop` | Laptop.vue | Danh sách laptop |
| 7 | Phụ Kiện | `/phu-kien` | PhuKien.vue | Danh sách phụ kiện |
| 8 | Chi Tiết Sản Phẩm | `/san-pham/:id` | ChiTietSanPham.vue | Xem chi tiết, chọn màu/RAM/dung lượng |
| 9 | Giỏ Hàng | `/cart` | GioHang.vue | Quản lý giỏ hàng, áp dụng voucher |
| 10 | Tài Khoản | `/account` | TaiKhoan.vue | Thông tin cá nhân, lịch sử đơn hàng |
| 11 | Hỗ Trợ | `/ho-tro` | HoTro.vue | Gửi ticket hỗ trợ, chat trực tuyến |
| 12 | NV Đăng Nhập | `/nhan-vien/dang-nhap` | NhanVienDangNhap.vue | Đăng nhập cho nhân viên |
| 13 | NV Lịch Làm | `/nhan-vien/lich-lam` | NhanVienLichLam.vue | Xem lịch làm việc |

### 4.2. Bảo vệ tuyến đường

Các route được bảo vệ (cần token JWT):
- `/cart` (Giỏ hàng)
- `/account` (Tài khoản)

Khi chưa đăng nhập, hệ thống tự động chuyển hướng đến `/login` và lưu lại đường dẫn để quay lại sau khi đăng nhập thành công.

---

## 5. Phân hệ Backend (API)

### 5.1. Danh sách API Controllers

| Controller | Router Prefix | Số lượng API | Chức năng chính |
|------------|--------------|--------------|-----------------|
| `xac_thuc.py` | `/xac-thuc` | ~20 | Auth, user CRUD, profile, chat, ticket, notification |
| `admin.py` | `/api/admin` | ~30 | Dashboard stats, audit, loyalty, push, AI, employee |
| `sanpham.py` | `/san-pham` | 8 | Product CRUD, filter, category |
| `donhang.py` | `/don-hang` | 12 | Order create/update/delete, warranty |
| `giohang.py` | `/gio-hang` | 6 | Cart add/remove/update/clear |
| `kho.py` | `/api/kho` | 4 | Inventory sync, allocation |
| `voucher.py` | `/vouchers` | 6 | Voucher CRUD, validation |
| `shipping.py` | `/shipping` | 6 | Shipping unit CRUD |
| `payment.py` | `/payment` | 6 | Payment partner CRUD |
| `yeuthich.py` | `/yeu-thich` | 4 | Wishlist add/remove/list |

---

## 6. Phân hệ Admin (Peach Admin)

### 6.1. Danh sách Tab Admin

| STT | Tab | File View | File ViewModel | Chức năng |
|-----|-----|-----------|----------------|-----------|
| 1 | Dashboard | (inline) | AdminViewModel.js | Thống kê doanh thu, đơn hàng, người dùng |
| 2 | Sản phẩm | products.html | AdminViewModel.js | CRUD sản phẩm, quản lý tồn kho |
| 3 | Đơn hàng | Orders.html | AdminViewModel.js | Duyệt/từ chối/cập nhật đơn hàng |
| 4 | Khách hàng | Customers.html | AdminViewModel.js | Xem/sửa thông tin khách hàng |
| 5 | Voucher | (inline) | AdminViewModel.js | Tạo/sửa/xóa mã giảm giá |
| 6 | Vận chuyển | (inline) | AdminViewModel.js | Quản lý đơn vị vận chuyển |
| 7 | Thanh toán | Payments.html | AdminViewModel.js | Quản lý đối tác thanh toán |
| 8 | Admin | Admins.html | AdminViewModel.js | Quản lý tài khoản admin |
| 9 | Hỗ trợ | Support.html | AdminViewModel.js | Xử lý ticket hỗ trợ |
| 10 | Nhật ký | (inline) | AdminViewModel.js | Audit log hoạt động admin |
| 11 | Loyalty | (inline) | AdminViewModel.js | Cấu hình cấp bậc thành viên |
| 12 | Thông báo | Notifications.html | AdminViewModel.js | Push notification campaigns |
| 13 | Chat | Chat.html | AdminViewModel.js | Chat real-time với khách hàng |
| 14 | AI | (inline) | AdminViewModel.js | Nhật ký chat AI, cấu hình model |

---

## 7. Các Use Case chi tiết

### 7.1. UC_DangNhap - Đăng nhập người dùng

#### Thông tin chung
- **Use-Case ID:** UC_DangNhap
- **Use-Case Name:** Đăng nhập người dùng
- **Brief Description:** Cho phép người dùng đăng nhập vào hệ thống bằng email/username và mật khẩu. Hệ thống xác thực thông tin và trả về JWT token để duy trì phiên đăng nhập.
- **Primary Actor:** Khách hàng, Nhân viên

#### Flow of Events

**Basic Flow (Luồng chính):**
1. Người dùng truy cập trang đăng nhập (`/login`)
2. Hệ thống hiển thị form đăng nhập (email, mật khẩu)
3. Người dùng nhập email và mật khẩu
4. Người dùng nhấn nút "Đăng nhập"
5. Hệ thống gửi request POST đến `/xac-thuc/dang-nhap`
6. Hệ thống kiểm tra thông tin đăng nhập
7. Xác thực thành công → trả về JWT access token
8. Hệ thống lưu token vào localStorage
9. Hệ thống chuyển hướng người dùng đến trang đã lưu hoặc trang chủ

**Alternative Flow 1 - Sai mật khẩu:**
- Tại bước 6, nếu mật khẩu không đúng:
  1. Hệ thống trả về lỗi "Sai mật khẩu"
  2. Hiển thị thông báo lỗi trên form
  3. Người dùng có thể nhập lại hoặc chọn "Quên mật khẩu"

**Alternative Flow 2 - Tài khoản không tồn tại:**
- Tại bước 6, nếu email không tồn tại:
  1. Hệ thống trả về lỗi "Tài khoản không tồn tại"
  2. Hiển thị thông báo lỗi kèm gợi ý đăng ký

**Alternative Flow 3 - Mất kết nối:**
- Nếu không thể kết nối đến server:
  1. Hệ thống hiển thị thông báo "Không thể kết nối tới máy chủ"
  2. Gợi ý người dùng kiểm tra lại kết nối mạng

#### Special Requirements
- Mật khẩu phải được hash bằng thuật toán bcrypt trước khi lưu
- Token JWT có thời hạn 60 phút
- Hỗ trợ đăng nhập bằng email hoặc tên đăng nhập

#### Pre-Conditions
- Người dùng chưa đăng nhập (không có token hợp lệ)

#### Post-Conditions
- Token JWT được lưu trong localStorage
- Người dùng được chuyển hướng đến trang đích

#### Extension Points
- **Quên mật khẩu:** Cho phép người dùng đặt lại mật khẩu qua email
- **Đăng nhập bằng Google/Facebook:** Tích hợp OAuth xã hội

---

### 7.2. UC_SanPham - Xem và quản lý sản phẩm

#### Thông tin chung
- **Use-Case ID:** UC_SanPham
- **Use-Case Name:** Xem và quản lý sản phẩm
- **Brief Description:** Cho phép người dùng xem danh sách sản phẩm theo danh mục, lọc theo tiêu chí (hãng, giá, RAM, dung lượng), xem chi tiết sản phẩm. Admin có thể thêm/sửa/xóa sản phẩm.
- **Primary Actor:** Khách hàng, Admin

#### Flow of Events

**Basic Flow - Xem danh sách sản phẩm:**
1. Người dùng chọn danh mục (Điện thoại, Máy tính bảng, Laptop, Phụ kiện)
2. Hệ thống gọi API GET `/san-pham?danh_muc={category}`
3. Hệ thống hiển thị danh sách sản phẩm dạng lưới (grid)
4. Mỗi sản phẩm hiển thị: hình ảnh, tên, giá, màu sắc có sẵn

**Basic Flow - Lọc sản phẩm:**
1. Người dùng chọn bộ lọc (hãng, giá, RAM, dung lượng)
2. Hệ thống gọi API `GET /san-pham?danh_muc=...&gia_min=...&gia_max=...`
3. Hệ thống cập nhật danh sách sản phẩm theo bộ lọc

**Basic Flow - Xem chi tiết sản phẩm:**
1. Người dùng click vào sản phẩm
2. Hệ thống chuyển đến trang `/san-pham/:id`
3. API `GET /san-pham/{id}` trả về thông tin đầy đủ
4. Hiển thị: hình ảnh, tên, giá, màu sắc, RAM, dung lượng, mô tả, thư viện ảnh

**Alternative Flow - Sản phẩm không tồn tại:**
- Nếu ID sản phẩm không hợp lệ:
  1. API trả về 404
  2. Hiển thị trang "Sản phẩm không tìm thấy"

#### Special Requirements
- Hỗ trợ lọc theo: danh_muc, hang (brand), gia_min/gia_max, ram, dung_luong
- Sản phẩm có thể có nhiều biến thể (RAM + Dung lượng + Màu sắc)
- Hỗ trợ upload nhiều ảnh (thư viện ảnh JSON)

#### Pre-Conditions
- Không yêu cầu đăng nhập để xem sản phẩm
- Cần quyền admin để thêm/sửa/xóa

#### Post-Conditions
- Người dùng có thể thêm sản phẩm vào giỏ hàng từ trang chi tiết

---

### 7.3. UC_GioHang - Quản lý giỏ hàng

#### Thông tin chung
- **Use-Case ID:** UC_GioHang
- **Use-Case Name:** Quản lý giỏ hàng
- **Brief Description:** Cho phép người dùng thêm sản phẩm vào giỏ hàng, xem giỏ hàng, cập nhật số lượng, xóa sản phẩm, và áp dụng voucher giảm giá.
- **Primary Actor:** Khách hàng (đã đăng nhập)

#### Flow of Events

**Basic Flow - Thêm vào giỏ hàng:**
1. Người dùng chọn sản phẩm, màu sắc, RAM, dung lượng, số lượng
2. Người dùng nhấn "Thêm vào giỏ"
3. Hệ thống gọi API POST `/gio-hang/them`
4. Hệ thống thêm sản phẩm vào giỏ hàng (backend)
5. Hiển thị thông báo "Đã thêm vào giỏ hàng"
6. Cập nhật số lượng giỏ hàng trên header

**Basic Flow - Xem giỏ hàng:**
1. Người dùng vào trang `/cart`
2. Hệ thống gọi API GET `/gio-hang`
3. Hiển thị danh sách sản phẩm trong giỏ:
   - Hình ảnh, tên, màu sắc, RAM, dung lượng
   - Đơn giá, số lượng, thành tiền
   - Tổng tiền, phí ship, giảm giá, tổng thanh toán

**Basic Flow - Áp dụng voucher:**
1. Người dùng nhập mã voucher
2. Hệ thống gọi API POST `/vouchers/apply`
3. Nếu hợp lệ: cập nhật tổng tiền sau giảm giá
4. Nếu không hợp lệ: hiển thị thông báo lỗi

**Alternative Flow - Sản phẩm đã hết hàng:**
- Khi thêm vào giỏ, nếu số lượng tồn kho = 0:
  1. Hiển thị thông báo "Sản phẩm đã hết hàng"
  2. Vô hiệu hóa nút thêm vào giỏ

#### Special Requirements
- Giỏ hàng được lưu ở backend (database) và đồng bộ theo tài khoản
- Kiểm tra tồn kho trước khi thêm vào giỏ
- Hỗ trợ nhiều biến thể sản phẩm (màu sắc, RAM, dung lượng)

#### Pre-Conditions
- Người dùng đã đăng nhập (có JWT token)
- Route `/cart` được bảo vệ bởi navigation guard

#### Post-Conditions
- Dữ liệu giỏ hàng được cập nhật trong database
- Header cập nhật số lượng giỏ hàng

---

### 7.4. UC_DonHang - Đặt hàng và quản lý đơn hàng

#### Thông tin chung
- **Use-Case ID:** UC_DonHang
- **Use-Case Name:** Đặt hàng và quản lý đơn hàng
- **Brief Description:** Cho phép khách hàng đặt hàng từ giỏ hàng. Admin có thể xem tất cả đơn hàng, duyệt/từ chối, cập nhật trạng thái, gán IMEI.
- **Primary Actor:** Khách hàng, Admin

#### Flow of Events

**Basic Flow - Đặt hàng:**
1. Người dùng xem giỏ hàng và nhấn "Đặt hàng"
2. Hệ thống kiểm tra PIN bảo mật (nếu đã cài đặt)
3. Hệ thống tạo đơn hàng qua API POST `/don-hang/dat-hang`
4. Đơn hàng được tạo với trạng thái "chờ xử lý"
5. Giỏ hàng được xóa sạch
6. Chuyển hướng đến trang xác nhận đơn hàng

**Basic Flow - Admin duyệt đơn hàng:**
1. Admin vào tab Đơn hàng
2. Hệ thống gọi API GET `/don-hang/admin/all`
3. Admin xem danh sách đơn hàng, lọc theo trạng thái
4. Admin chọn đơn hàng và nhấn "Duyệt"
5. Hệ thống gọi API PUT `/don-hang/admin/cap-nhat/{id}`
6. Trạng thái đơn hàng được cập nhật

**Alternative Flow - Admin từ chối đơn hàng:**
1. Admin nhấn "Từ chối" trên đơn hàng
2. Hệ thống yêu cầu nhập lý do từ chối
3. API cập nhật trạng thái "đã hủy" kèm lý do

**Alternative Flow - Admin xóa đơn hàng:**
1. Admin nhấn "Xóa" trên đơn hàng
2. Hệ thống hiển thị modal xác nhận
3. Admin xác nhận → API DELETE `/don-hang/admin/xoa/{id}`
4. Đơn hàng bị xóa vĩnh viễn khỏi hệ thống

**Alternative Flow - Hủy đơn hàng (người dùng):**
1. Người dùng vào lịch sử đơn hàng
2. Chọn đơn hàng và nhấn "Hủy"
3. API gọi PUT `/don-hang/huy/{id}` (soft delete)
4. Đơn hàng ẩn khỏi danh sách người dùng

#### Special Requirements
- Mỗi đơn hàng được gán IMEI duy nhất cho sản phẩm
- Hỗ trợ bảo hành theo IMEI (tra cứu bằng API)
- Tính phí ship tự động, giảm giá voucher tự động
- Cần xác thực PIN cho đơn hàng có giá trị lớn

#### Pre-Conditions
- Người dùng đã đăng nhập
- Giỏ hàng không trống
- Sản phẩm còn hàng trong kho

#### Post-Conditions
- Đơn hàng được tạo trong database
- Giỏ hàng được xóa
- Số lượng tồn kho được cập nhật

#### Extension Points
- **Tra cứu bảo hành:** Tra cứu thông tin bảo hành bằng IMEI
- **Xuất hóa đơn:** Tự động tạo hóa đơn PDF

---

### 7.5. UC_Voucher - Quản lý mã giảm giá

#### Thông tin chung
- **Use-Case ID:** UC_Voucher
- **Use-Case Name:** Quản lý mã giảm giá
- **Brief Description:** Admin có thể tạo mã giảm giá với các điều kiện (giá trị tối thiểu, % giảm, số lượng). Người dùng có thể áp dụng mã giảm giá khi đặt hàng.
- **Primary Actor:** Admin, Khách hàng

#### Flow of Events

**Basic Flow - Admin tạo voucher:**
1. Admin vào tab Voucher
2. Nhấn "Thêm voucher"
3. Nhập thông tin: mã, % giảm, giá trị tối đa, đơn tối thiểu, số lượng
4. API POST `/vouchers/admin/add`
5. Voucher được tạo, cập nhật danh sách

**Basic Flow - Khách hàng áp dụng voucher:**
1. Tại trang giỏ hàng, nhập mã voucher
2. API POST `/vouchers/apply`
3. Hệ thống kiểm tra: mã tồn tại, còn hạn, đủ điều kiện
4. Nếu hợp lệ: tính giảm giá và hiển thị tổng mới

#### Special Requirements
- Voucher có các trường: ma, phan_tram_giam, gia_toi_da, don_toi_thieu, so_luong_mac_dinh, ngay_het_han, trang_thai
- Kiểm tra điều kiện đơn hàng tối thiểu
- Giới hạn số lượng voucher có thể sử dụng

---

### 7.6. UC_HoTro - Hỗ trợ khách hàng

#### Thông tin chung
- **Use-Case ID:** UC_HoTro
- **Use-Case Name:** Hỗ trợ khách hàng
- **Brief Description:** Cho phép khách hàng gửi yêu cầu hỗ trợ (ticket), chat trực tuyến với admin, và upload ảnh đính kèm. Admin xử lý ticket và trả lời chat.
- **Primary Actor:** Khách hàng, Admin

#### Flow of Events

**Basic Flow - Gửi ticket hỗ trợ:**
1. Người dùng vào trang `/ho-tro`
2. Nhập thông tin: tiêu đề, nội dung, đính kèm ảnh (nếu có)
3. API POST `/xac-thuc/gui-yeu-cau-ho-tro`
4. Ticket được tạo với trạng thái "chờ xử lý"
5. Hiển thị thông báo thành công

**Basic Flow - Admin xử lý ticket:**
1. Admin vào tab Hỗ trợ
2. Xem danh sách ticket, lọc theo trạng thái
3. Click vào ticket để xem chi tiết
4. Trả lời hoặc cập nhật trạng thái "đã xử lý"
5. API PUT `/api/support/admin/tickets/{id}/status`

**Basic Flow - Chat admin với khách hàng:**
1. Admin vào tab Chat
2. Xem danh sách các phiên chat
3. Chọn khách hàng để chat
4. Gửi tin nhắn qua API, nhận tin nhắn mới qua polling

#### Special Requirements
- Hỗ trợ upload ảnh lên thư mục static/uploads
- Ticket có trạng thái: cho_xu_ly, dang_xu_ly, da_xu_ly
- Chat sử dụng polling interval để cập nhật real-time

---

### 7.7. UC_AdminDashboard - Trang tổng quan Admin

#### Thông tin chung
- **Use-Case ID:** UC_AdminDashboard
- **Use-Case Name:** Trang tổng quan Admin
- **Brief Description:** Hiển thị thống kê tổng quan: doanh thu, đơn hàng mới, người dùng mới, hoạt động gần đây. Tự động làm mới dữ liệu nền mỗi 30 giây.
- **Primary Actor:** Admin

#### Flow of Events

**Basic Flow - Xem dashboard:**
1. Admin đăng nhập vào hệ thống quản trị
2. Tab mặc định là Dashboard
3. Hệ thống gọi:
   - `GET /api/admin/dashboard/stats` → Thống kê doanh thu, đơn hàng, người dùng
   - `GET /api/admin/activities` → Hoạt động gần đây
4. Hiển thị các thẻ thống kê (revenue, orders, customers)
5. Hiển thị danh sách hoạt động

**Background Flow - Tự động làm mới:**
1. SetInterval 30 giây gọi `refreshData()`
2. Làm mới tất cả dữ liệu tab đang mở
3. Cập nhật số liệu mà không làm gián đoạn thao tác người dùng

#### Special Requirements
- Dashboard là tab mặc định khi vào admin
- Dữ liệu tự động refresh nền mỗi 30 giây
- Cần tối ưu số lượng API gọi đồng thời để tránh quá tải server

#### Pre-Conditions
- Admin đã đăng nhập
- Có kết nối đến backend API

---

### 7.8. UC_Loyalty - Quản lý cấp bậc thành viên

#### Thông tin chung
- **Use-Case ID:** UC_Loyalty
- **Use-Case Name:** Quản lý cấp bậc thành viên
- **Brief Description:** Admin có thể cấu hình các cấp bậc thành viên (Bạc, Vàng, Kim cương) với ngưỡng điểm và đặc quyền. Khách hàng tích lũy điểm qua đơn hàng.
- **Primary Actor:** Admin

#### Flow of Events

**Basic Flow - Cấu hình cấp bậc:**
1. Admin vào tab Loyalty
2. Xem danh sách cấp bậc hiện tại
3. Thêm/sửa cấp bậc: tên, điểm tối thiểu, màu sắc, đặc quyền
4. API POST/ PUT `/api/admin/loyalty-configs`

#### Special Requirements
- Cấp bậc mặc định: Bạc (0-999), Vàng (1000-4999), Kim cương (5000+)
- Mỗi cấp bậc có màu sắc riêng để hiển thị trên giao diện
- Xếp hạng tự động dựa trên điểm tích lũy

---

### 7.9. UC_AIChat - Chat với AI (Admin)

#### Thông tin chung
- **Use-Case ID:** UC_AIChat
- **Use-Case Name:** Chat với AI hỗ trợ quản trị
- **Brief Description:** Tích hợp DeepSeek AI để admin có thể chat với AI nhằm hỗ trợ quản lý cửa hàng, phân tích dữ liệu, tạo nội dung.
- **Primary Actor:** Admin

#### Flow of Events

**Basic Flow - Chat với AI:**
1. Admin mở chat AI trong admin
2. Nhập câu hỏi hoặc yêu cầu
3. Hệ thống gửi request đến endpoint `/api/admin/ai-chat`
4. Hệ thống gọi DeepSeek API với câu hỏi
5. Hiển thị câu trả lời từ AI
6. Lưu lịch sử chat vào database (bảng ai_logs)

**Alternative Flow - Lỗi API AI:**
- Nếu DeepSeek API không phản hồi:
  1. Hiển thị thông báo lỗi
  2. Gợi ý admin kiểm tra cấu hình API key

#### Special Requirements
- Admin cần cấu hình API key cho DeepSeek
- Lịch sử chat được lưu để tra cứu sau
- Hỗ trợ nhiều model AI (cấu hình qua biến môi trường)

---

### 7.10. UC_NhanVien - Quản lý nhân viên & lịch làm

#### Thông tin chung
- **Use-Case ID:** UC_NhanVien
- **Use-Case Name:** Quản lý nhân viên và lịch làm việc
- **Brief Description:** Admin quản lý tài khoản nhân viên, phân quyền, xem lịch làm việc. Nhân viên đăng nhập riêng để xem lịch.
- **Primary Actor:** Admin, Nhân viên

#### Flow of Events

**Basic Flow - Admin quản lý nhân viên:**
1. Admin vào tab Admin
2. Xem danh sách nhân viên
3. Thêm/sửa/xóa nhân viên
4. Phân quyền (admin/nhan_vien)

**Basic Flow - Nhân viên xem lịch:**
1. Nhân viên truy cập `/nhan-vien/dang-nhap`
2. Đăng nhập bằng tài khoản nhân viên
3. Xem lịch làm việc tại `/nhan-vien/lich-lam`

---

## 8. Thiết kế dữ liệu

### 8.1. Danh sách các bảng (Models)

| STT | Bảng | File Model | Mô tả |
|-----|------|-----------|-------|
| 1 | `nguoi_dung` | nguoidung.py | Người dùng (khách hàng + admin) |
| 2 | `san_pham` | sanpham.py | Sản phẩm |
| 3 | `gio_hang` | giohang.py | Giỏ hàng |
| 4 | `don_hang` | donhang.py | Đơn hàng |
| 5 | `chi_tiet_don_hang` | donhang.py | Chi tiết đơn hàng |
| 6 | `danh_sach_yeu_thich` | yeuthich.py | Sản phẩm yêu thích |
| 7 | `voucher` | voucher.py | Mã giảm giá |
| 8 | `don_vi_van_chuyen` | don_vi_van_chuyen.py | Đơn vị vận chuyển |
| 9 | `doi_tac_thanh_toan` | doi_tac_thanh_toan.py | Đối tác thanh toán |
| 10 | `cau_hinh_loyalty` | cau_hinh_loyalty.py | Cấu hình loyalty |
| 11 | `hoatdong_admin` | hoatdong_admin.py | Hoạt động admin |
| 12 | `nhat_ky_audit` | nhat_ky_audit.py | Nhật ký audit |
| 13 | `lichsu_dangnhap` | lichsu_dangnhap.py | Lịch sử đăng nhập |
| 14 | `nhatky_ai` | nhatky_ai.py | Nhật ký AI chat |
| 15 | `tinnhan_chat` | tinnhan_chat.py | Tin nhắn chat |
| 16 | `yeu_cau_ho_tro` | yeu_cau_ho_tro.py | Yêu cầu hỗ trợ |
| 17 | `yeu_cau_doanh_nghiep` | yeu_cau_doanh_nghiep.py | Yêu cầu nâng cấp doanh nghiệp |

### 8.2. Chi tiết bảng quan trọng

#### Bảng `nguoi_dung` (Users)

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | Integer | PK, Auto Increment | ID người dùng |
| ho_ten | String(100) | NOT NULL | Họ và tên |
| email | String(100) | UNIQUE, NOT NULL | Email đăng nhập |
| mat_khau | String(255) | NOT NULL | Mật khẩu (bcrypt hash) |
| so_dien_thoai | String(20) | NULLABLE | Số điện thoại |
| dia_chi | Text | NULLABLE | Địa chỉ |
| hinh_anh | Text | NULLABLE | URL ảnh đại diện |
| vai_tro | Enum | DEFAULT 'nguoi_dung' | Vai trò (nguoi_dung/admin/nhan_vien) |
| trang_thai | Enum | DEFAULT 'dang_hoat_dong' | Trạng thái tài khoản |
| diem_tich_luy | Integer | DEFAULT 0 | Điểm tích lũy |
| ma_pin | String(6) | NULLABLE | Mã PIN bảo mật |
| ngay_tao | DateTime | DEFAULT now() | Ngày tạo |

#### Bảng `san_pham` (Products)

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | Integer | PK, Auto Increment | ID sản phẩm |
| ten | String(200) | NOT NULL | Tên sản phẩm |
| danh_muc | String(50) | NOT NULL | Danh mục (iphone, ipad, mac, phu_kien) |
| gia | Float | NOT NULL | Giá sản phẩm |
| mau_sac | Text | NULLABLE | Màu sắc (JSON array) |
| ram | String(255) | DEFAULT '' | RAM (comma-separated) |
| dung_luong | String(255) | DEFAULT '' | Dung lượng (comma-separated) |
| mo_ta | Text | NULLABLE | Mô tả sản phẩm |
| hinh_anh | Text | NULLABLE | URL ảnh chính |
| thu_vien_anh | JSON | DEFAULT '[]' | Thư viện ảnh |
| hang | String(100) | NULLABLE | Hãng sản xuất |
| is_new | Integer | DEFAULT 1 | Sản phẩm mới (0/1) |
| so_luong_kho | Integer | DEFAULT 0 | Số lượng tồn kho |
| trang_thai | Enum | DEFAULT 'dang_hoat_dong' | Trạng thái |

#### Bảng `don_hang` (Orders)

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | Integer | PK, Auto Increment | ID đơn hàng |
| ten_khach_hang | String(200) | NOT NULL | Tên khách hàng |
| dia_chi | Text | NOT NULL | Địa chỉ giao hàng |
| so_dien_thoai | String(20) | NOT NULL | Số điện thoại |
| tong_tien | Float | NOT NULL | Tổng tiền |
| phi_ship | Float | DEFAULT 0 | Phí vận chuyển |
| giam_gia_voucher | Float | DEFAULT 0 | Giảm giá voucher |
| phuong_thuc_thanh_toan | String(100) | NULLABLE | Phương thức thanh toán |
| phuong_thuc_van_chuyen | String(100) | NULLABLE | Phương thức vận chuyển |
| ngay_tao | DateTime | DEFAULT now() | Ngày tạo |
| trang_thai | Enum | DEFAULT 'cho_xu_ly' | Trạng thái đơn hàng |
| nguoi_dung_id | Integer | FK → nguoi_dung.id | ID người dùng |
| imei | String(50) | NULLABLE | IMEI sản phẩm |
| warranty_months | Integer | DEFAULT 6 | Thời gian bảo hành |

---

## 9. Luồng công việc (Workflows)

### 9.1. Luồng mua hàng hoàn chỉnh

| Kịch bản | Hành động của người dùng (Actor) | Phản hồi của Hệ thống (System) |
|----------|--------------------------------|-------------------------------|
| 1. Xem sản phẩm | Người dùng truy cập trang chủ hoặc chọn danh mục | Hiển thị danh sách sản phẩm với hình ảnh, tên, giá |
| 2. Xem chi tiết | Click vào sản phẩm | Hiển thị trang chi tiết: ảnh, màu sắc, RAM, dung lượng, mô tả |
| 3. Chọn biến thể | Chọn màu sắc, RAM, dung lượng, số lượng | Cập nhật hình ảnh và giá theo biến thể đã chọn |
| 4. Thêm vào giỏ | Nhấn "Thêm vào giỏ" | Gọi API thêm giỏ hàng, hiển thị thông báo, cập nhật badge |
| 5. Xem giỏ hàng | Vào trang giỏ hàng | Hiển thị danh sách sản phẩm, tổng tiền, phí ship |
| 6. Áp dụng voucher | Nhập mã giảm giá | Kiểm tra và cập nhật tổng tiền sau giảm giá |
| 7. Đặt hàng | Nhấn "Đặt hàng", xác nhận thông tin | Kiểm tra PIN (nếu có), tạo đơn hàng, xóa giỏ hàng |
| 8. Xác nhận | Xem thông báo đặt hàng thành công | Chuyển hướng đến trang xác nhận đơn hàng |

### 9.2. Luồng Admin duyệt đơn hàng

| Kịch bản | Hành động của người dùng (Actor) | Phản hồi của Hệ thống (System) |
|----------|--------------------------------|-------------------------------|
| 1. Vào quản lý đơn | Admin chọn tab "Đơn hàng" | Gọi API lấy danh sách đơn hàng, hiển thị trong bảng |
| 2. Lọc đơn hàng | Chọn bộ lọc trạng thái | Lọc và hiển thị đơn hàng theo trạng thái |
| 3. Xem chi tiết | Click vào đơn hàng | Mở modal/xem chi tiết: sản phẩm, khách hàng, địa chỉ |
| 4. Duyệt đơn | Nhấn "Duyệt" | Gọi API cập nhật trạng thái, xác nhận thành công |
| 5. Gán IMEI | Nhập IMEI cho sản phẩm (nếu cần) | Cập nhật IMEI vào đơn hàng |
| 6. Hoàn tất | Đóng modal | Danh sách đơn hàng được refresh |

### 9.3. Luồng Admin hỗ trợ khách hàng

| Kịch bản | Hành động của người dùng (Actor) | Phản hồi của Hệ thống (System) |
|----------|--------------------------------|-------------------------------|
| 1. Xem ticket | Admin vào tab "Hỗ trợ" | Gọi API lấy danh sách ticket, hiển thị badge số lượng chờ |
| 2. Chọn ticket | Click vào ticket cần xử lý | Mở chi tiết ticket: nội dung, ảnh đính kèm |
| 3. Trả lời | Nhập nội dung trả lời và gửi | Gọi API cập nhật ticket, hiển thị câu trả lời |
| 4. Đóng ticket | Nhấn "Đã xử lý" | Cập nhật trạng thái ticket thành "da_xu_ly" |

### 9.4. Luồng khởi tạo Admin (onMounted)

| Kịch bản | Hành động | Mô tả |
|----------|-----------|-------|
| 1. Load tab hiện tại | `loadTabData(activeTab.value)` | Chỉ load dữ liệu cho tab đang active (lazy loading) |
| 2. Load badge data | 8 fetch calls song song | Load dữ liệu badge (orders, reset requests, business requests, tickets, audit logs, push campaigns, chat, ai logs) |
| 3. Start chat polling | `startAdminChatPolling()` | Bắt đầu polling tin nhắn chat mới |
| 4. Set refresh interval | `setInterval(refreshData, 30000)` | Tự động refresh toàn bộ dữ liệu mỗi 30 giây |

---

## 10. Yêu cầu phi chức năng

### 10.1. Hiệu năng (Performance)

| Yêu cầu | Mô tả | Chỉ tiêu |
|---------|-------|---------|
| Thời gian phản hồi API | API trả về kết quả trong thời gian chấp nhận được | < 2 giây (95% requests) |
| Số lượng request đồng thời | Hệ thống xử lý được nhiều request cùng lúc | Hỗ trợ tối thiểu 50 concurrent users |
| Thời gian tải trang | Trang web load nhanh | < 3 giây (First Contentful Paint) |
| Làm mới dữ liệu nền | Dữ liệu admin tự động cập nhật | Interval 30 giây, không gây giật lag |

### 10.2. Bảo mật (Security)

| Yêu cầu | Mô tả |
|---------|-------|
| Xác thực | Sử dụng JWT token (HS256), thời hạn 60 phút |
| Mật khẩu | Hash bằng bcrypt trước khi lưu |
| PIN bảo mật | Mã PIN 6 số cho đơn hàng giá trị lớn |
| Phân quyền | Ba vai trò: nguoi_dung, admin, nhan_vien |
| Bảo vệ route | Kiểm tra token trước khi cho phép truy cập trang cá nhân |

### 10.3. Khả năng mở rộng (Scalability)

| Yêu cầu | Mô tả |
|---------|-------|
| Database | Sử dụng PostgreSQL, có thể nâng cấp dung lượng |
| API | Kiến trúc RESTful, dễ dàng thêm endpoint mới |
| Frontend | Component-based (Vue 3), dễ dàng thêm trang mới |
| Admin | Modular theo tab, dễ dàng thêm tab mới |

### 10.4. Độ tin cậy (Reliability)

| Yêu cầu | Mô tả |
|---------|-------|
| Xử lý lỗi | Mọi API đều có try-catch, hiển thị thông báo lỗi thân thiện |
| Tự động reconnect | Chat và các polling tự động kết nối lại khi mất mạng |
| Validation | Kiểm tra dữ liệu đầu vào ở cả Frontend và Backend |

---

## 11. Phụ lục

### 11.1. Biểu đồ trạng thái đơn hàng

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ chờ xử lý│────▶│ đang xử lý│────▶│ đã giao  │
└──────────┘     └──────────┘     └──────────┘
      │                │
      ▼                ▼
┌──────────┐     ┌──────────┐
│ đã hủy   │     │ đã hủy   │
└──────────┘     └──────────┘
```

### 11.2. Biểu đồ trạng thái ticket hỗ trợ

```
┌─────────────┐     ┌─────────────┐     ┌──────────┐
│  chờ xử lý  │────▶│ đang xử lý  │────▶│ đã xử lý │
└─────────────┘     └─────────────┘     └──────────┘
```

### 11.3. Danh sách API chính

| Method | Endpoint | Controller | Chức năng |
|--------|----------|-----------|-----------|
| POST | `/xac-thuc/dang-nhap` | xac_thuc | Đăng nhập |
| POST | `/xac-thuc/dang-ky` | xac_thuc | Đăng ký |
| GET | `/san-pham` | sanpham | Danh sách sản phẩm |
| GET | `/san-pham/{id}` | sanpham | Chi tiết sản phẩm |
| POST | `/gio-hang/them` | giohang | Thêm vào giỏ |
| GET | `/gio-hang` | giohang | Xem giỏ hàng |
| POST | `/don-hang/dat-hang` | donhang | Đặt hàng |
| GET | `/don-hang/admin/all` | donhang | Admin xem tất cả đơn |
| GET | `/api/admin/dashboard/stats` | admin | Thống kê dashboard |
| POST | `/vouchers/admin/add` | voucher | Thêm voucher |
| POST | `/vouchers/apply` | voucher | Áp dụng voucher |
| POST | `/api/admin/ai-chat` | admin | Chat với AI |

---

## PHỤ LỤC A: Sơ đồ Activity

### A.1. Activity Diagram - Quy trình mua hàng

```
┌──────────────────────────────────────────────────┐
│  User                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Xem SP    │  │Chọn biến │  │Thêm vào  │       │
│  │          │  │thể       │  │giỏ       │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │              │              │             │
│       ▼              ▼              ▼             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Xem giỏ   │  │Nhập      │  │Đặt hàng  │       │
│  │hàng      │  │voucher   │  │          │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
└───────┼─────────────┼─────────────┼──────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼──────────────┐
│  System                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Validate  │  │Check     │  │Create    │       │
│  │voucher   │  │PIN (opt) │  │order     │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│                                                   │
│  ┌──────────────────────────────────────────┐     │
│  │  Return order confirmation + clear cart  │     │
│  └──────────────────────────────────────────┘     │
└──────────────────────────────────────────────────┘
```

### A.2. Activity Diagram - Quy trình Admin xử lý đơn hàng

```
┌──────────────────────────────────────────────────┐
│  Admin                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Vào tab   │  │Chọn đơn  │  │Xem chi   │       │
│  │Đơn hàng  │  │hàng      │  │tiết      │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │              │              │             │
│       ▼              ▼              ▼             │
│  ┌──────────────────────────────────────────┐     │
│  │  Quyết định                               │     │
│  │  ┌──────────┐      ┌──────────┐          │     │
│  │  │Duyệt     │      │Từ chối   │          │     │
│  │  └────┬─────┘      └────┬─────┘          │     │
│  └───────┼─────────────────┼────────────────┘     │
└──────────┼─────────────────┼──────────────────────┘
           │                 │
┌──────────▼─────────────────▼──────────────────────┐
│  System                                            │
│  ┌──────────────────┐  ┌──────────────────┐       │
│  │Update status:     │  │Update status:     │       │
│  │đang_xu_ly/giao   │  │đã_hủy + lý do    │       │
│  └──────────────────┘  └──────────────────┘       │
└──────────────────────────────────────────────────┘
```

---

> **Kết thúc tài liệu Đặc tả yêu cầu phần mềm (SRS) - Phiên bản 1.0.0**
> 
> *Peach Store - Hệ thống thương mại điện tử bán điện thoại & phụ kiện*
> *© 2026 Peach Studio. Bảo lưu mọi quyền.*
