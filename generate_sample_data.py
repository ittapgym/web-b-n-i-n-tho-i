import urllib.request
import json
import time

API_URL = "https://peach-store-backend.onrender.com/san-pham/"

sample_products = [
    {
        "ten": "iPhone 15 Pro Max",
        "mau_sac": "#000000,#ffffff,#4B4845",
        "dung_luong": "256GB, 512GB, 1TB",
        "ram": "8GB",
        "mo_ta": "iPhone 15 Pro Max sở hữu thiết kế titan chuẩn hàng không vũ trụ, siêu bền và siêu nhẹ. Chip A17 Pro mang đến hiệu năng đồ họa khủng.",
        "gia": 34990000,
        "hinh_anh": "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/iphone-15-pro-max-natural-titanium-select?wid=940&hei=1112&fmt=png-alpha",
        "thu_vien_anh": [],
        "danh_muc": "iphone",
        "is_new": 1,
        "so_luong_kho": 50
    },
    {
        "ten": "MacBook Pro 14 M3",
        "mau_sac": "#1E1E1E,#B0B5B9",
        "dung_luong": "512GB, 1TB",
        "ram": "18GB, 36GB",
        "mo_ta": "MacBook Pro 14 inch với chip M3 Pro siêu mạnh mẽ. Màn hình Liquid Retina XDR tuyệt đẹp.",
        "gia": 49990000,
        "hinh_anh": "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/mbp14-spaceblack-select-202310?wid=904&hei=840&fmt=jpeg",
        "thu_vien_anh": [],
        "danh_muc": "mac",
        "is_new": 1,
        "so_luong_kho": 30
    },
    {
        "ten": "iPad Pro M4 11-inch",
        "mau_sac": "#2D2D2D,#E3E4E5",
        "dung_luong": "256GB, 512GB",
        "ram": "8GB",
        "mo_ta": "iPad Pro mỏng nhất từ trước tới nay. Màn hình Ultra Retina XDR siêu nét với sức mạnh đột phá từ chip M4.",
        "gia": 28990000,
        "hinh_anh": "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/ipad-pro-11-select-wifi-spaceblack-202405?wid=940&hei=1112&fmt=png-alpha",
        "thu_vien_anh": [],
        "danh_muc": "ipad",
        "is_new": 1,
        "so_luong_kho": 100
    },
    {
        "ten": "Apple Watch Series 9",
        "mau_sac": "#1D1D1F,#F5F5F7,#E30039",
        "dung_luong": "",
        "ram": "",
        "mo_ta": "Apple Watch Series 9 thông minh hơn, sáng hơn và mạnh mẽ hơn. Tính năng Chạm Hai Lần cực kỳ tiện lợi.",
        "gia": 10490000,
        "hinh_anh": "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/watch-s9-alum-midnight-nc-select_VW_34FR+watch-45-alum-midnight-nc-s9_VW_34FR_WF_CO?wid=2000&hei=2000&fmt=png-alpha",
        "thu_vien_anh": [],
        "danh_muc": "watch",
        "is_new": 1,
        "so_luong_kho": 150
    },
    {
        "ten": "AirPods Pro (Gen 2)",
        "mau_sac": "#FFFFFF",
        "dung_luong": "",
        "ram": "",
        "mo_ta": "AirPods Pro 2 mang đến trải nghiệm Âm thanh không gian cá nhân hóa. Chống ồn chủ động xuất sắc hơn gấp 2 lần.",
        "gia": 6190000,
        "hinh_anh": "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/MTJV3?wid=1144&hei=1144&fmt=jpeg",
        "thu_vien_anh": [],
        "danh_muc": "phu_kien",
        "is_new": 1,
        "so_luong_kho": 200
    }
]

print(">>> ĐANG TỰ ĐỘNG TẠO DỮ LIỆU SẢN PHẨM MẪU LÊN RENDER...")
success_count = 0

for item in sample_products:
    try:
        req = urllib.request.Request(API_URL, data=json.dumps(item).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            if response.status in (200, 201):
                print(f"[OK] Đã thêm sản phẩm: {item['ten']}")
                success_count += 1
        time.sleep(1) # Nghỉ 1 giây để tránh quá tải
    except Exception as e:
        print(f"[LỖI] Không thể thêm {item['ten']}: {e}")

print(f">>> HOÀN TẤT! Đã thêm thành công {success_count}/{len(sample_products)} sản phẩm.")
