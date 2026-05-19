<template>
  <div id="app">
    <AppleToast />
    
    <!-- Premium Maintenance Overlay -->
    <div v-if="isMaintenance && !isStaffRoute" class="maintenance-overlay">
      <div class="maintenance-card">
        <div class="maintenance-icon" style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-bottom: 24px;">
          <!-- Tools Wrench SVG -->
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF9500" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 8px rgba(255, 149, 0, 0.3));">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>
          </svg>
          <!-- Peach-like Heart Shape SVG -->
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF453A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 8px rgba(255, 69, 58, 0.3));">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
          </svg>
        </div>
        <h2>Bảo Trì Hệ Thống</h2>
        <p>Peach Store hiện đang đóng cửa để nâng cấp hệ thống và tối ưu hóa hiệu năng phục vụ. Chúng tôi sẽ trở lại hoạt động bình thường trong thời gian ngắn nhất.</p>
        <div class="maintenance-badge">Trở lại hoạt động sớm!</div>
        <div class="maintenance-footer">Vui lòng liên hệ Hotline 1800-xxxx nếu cần hỗ trợ khẩn cấp.</div>
      </div>
    </div>

    <template v-else>
      <!-- Hien thi Navbar/Footer chi khi khong phai trang Dang Nhap/Dang Ky -->
      <SiteHeader v-if="showLayout" />

      <!-- Premium Scrolling Study Notice Banner (Đặt dưới Navbar, trên Hero) -->
      <div v-if="showLayout" class="study-notice-bar">
        <div class="notice-marquee-container">
          <div class="notice-marquee-content">
            <div class="notice-item">
              <span class="notice-badge">HỌC TẬP</span>
              <span class="notice-text">Dự án phục vụ học tập, nghiên cứu công nghệ & phi thương mại.</span>
            </div>
            <div class="notice-item">
              <span class="notice-badge">HỌC TẬP</span>
              <span class="notice-text">Dự án phục vụ học tập, nghiên cứu công nghệ & phi thương mại.</span>
            </div>
          </div>
        </div>
      </div>
      
      <main :class="{ 'has-layout': showLayout }">
        <router-view />
      </main>

      <SiteFooter v-if="showLayout" />
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import AppleToast from './components/AppleToast.vue';
import SiteHeader from './components/SiteHeader.vue';
import SiteFooter from './components/SiteFooter.vue';
import { initInactivityTracking } from './utils/inactivity';

const route = useRoute();
const isMaintenance = ref(false);

const isStaffRoute = computed(() => {
  return route.path.startsWith('/nhan-vien');
});

// Danh sach cac trang khong hien thi Navbar/Footer chung
const showLayout = computed(() => {
  const hideOn = ['DangNhap', 'DangKy', 'NhanVienDangNhap', 'NhanVienLichLam'];
  return !hideOn.includes(route.name);
});

const checkMaintenance = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/admin/config');
    if (res.ok) {
      const data = await res.json();
      isMaintenance.value = !!data.maintenanceMode;
    }
  } catch (e) {
    console.error("Lỗi kiểm tra trạng thái bảo trì: ", e);
  }
};

// Khoi dong theo doi inactivity (tu dong logout sau 15 phut khong thao tac)
let cleanupInactivity = null;

onMounted(() => {
  cleanupInactivity = initInactivityTracking();
  checkMaintenance();
  // Poll maintenance mode state every 10 seconds for real-time safety
  const interval = setInterval(checkMaintenance, 10000);
  onUnmounted(() => {
    clearInterval(interval);
  });
});

onUnmounted(() => {
  if (cleanupInactivity) cleanupInactivity();
});
</script>

<style>
/* Style global cho phan content khi co Navbar */
.has-layout {
  min-height: 100vh;
}

.study-notice-bar {
  background: rgba(50, 215, 200, 0.06); /* Nền xanh xanh kính gương ngọc nhạt trải dài hết chiều ngang */
  border-bottom: 1px solid rgba(50, 215, 200, 0.12); /* Đường viền ngọc dưới trải dài */
  padding: 10px 0; /* Độ cao vừa vặn cho dòng chữ */
  width: 100%; /* Dài hết chiều ngang */
  box-sizing: border-box;
  backdrop-filter: blur(10px); /* Hiệu ứng kính gương ngọc */
  -webkit-backdrop-filter: blur(10px);
  margin-top: 48px; /* Khớp sát dưới thanh Navbar 48px */
  position: relative;
  z-index: 99;
}

.notice-marquee-container {
  max-width: 600px; /* Khung chạy chữ ở giữa - CHỮ KHÔNG CHẠY HẾT CHIỀU NGANG */
  margin: 0 auto; /* Căn giữa khung hiển thị */
  overflow: hidden; /* Cắt chữ tràn ngoài để chữ chỉ xuất hiện và chạy trong vùng 600px giữa màn hình */
  white-space: nowrap;
  width: 90%; /* Tự động co giãn trên thiết bị di động */
}

.notice-marquee-content {
  display: inline-flex;
  align-items: center;
  animation: marquee 16s linear infinite; /* Chạy liên tục trơn tru trong phạm vi khung */
}

.notice-item {
  display: inline-flex;
  align-items: center;
  gap: 12px; /* Giãn cách giữa badge và text */
  padding-right: 60px; /* Tạo khoảng cách nối giữa các bản sao */
}

.notice-badge {
  background: rgba(0, 122, 255, 0.08); /* Nền xanh dương trong suốt */
  color: #007aff; /* Màu xanh dương chuẩn Series 11 */
  font-size: 10px; /* Kích thước tinh tế */
  font-weight: 500; /* Chữ nhẹ, thanh mảnh */
  padding: 2px 8px; /* Hộp badge gọn gàng */
  border-radius: 4px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  font-family: 'Outfit', -apple-system, sans-serif;
}

.notice-text {
  font-size: 12.5px; /* Kích thước chữ vô cùng vừa vặn */
  font-weight: 400; /* Giữ chữ nhẹ, thanh mảnh */
  color: #007aff; /* Màu xanh dương chuẩn Series 11 */
  letter-spacing: -0.01em;
  font-family: 'Outfit', -apple-system, sans-serif;
}

@keyframes marquee {
  0% { transform: translateX(0); }
  /* Chuyển động đúng bằng chiều rộng của 1 item (50% của 2 item nối tiếp) để lặp vô hạn seamless */
  100% { transform: translateX(-50%); }
}
@media (max-width: 734px) {
  .notice-text {
    font-size: 10.5px;
  }
  .notice-badge {
    font-size: 8.5px;
    padding: 1.5px 6px;
  }
  .study-notice-bar {
    padding: 8px 0;
  }
  .notice-marquee-container {
    max-width: 90%;
  }
  .notice-item {
    padding-right: 30px;
  }
}
</style>

<style scoped>
.maintenance-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, #1c1c1e 0%, #0a0a0c 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999999;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  padding: 24px;
  color: #ffffff;
}

.maintenance-card {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  padding: 48px 32px;
  max-width: 480px;
  width: 100%;
  text-align: center;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
  animation: cardFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.maintenance-icon {
  font-size: 64px;
  margin-bottom: 24px;
  filter: drop-shadow(0 0 15px rgba(255,149,0,0.35));
  animation: pulseIcon 2.5s ease-in-out infinite;
}

.maintenance-card h2 {
  font-size: 26px;
  font-weight: 700;
  margin: 0 0 16px 0;
  letter-spacing: -0.5px;
}

.maintenance-card p {
  color: #a1a1aa;
  font-size: 14.5px;
  line-height: 1.6;
  margin: 0 0 28px 0;
}

.maintenance-badge {
  display: inline-block;
  background: rgba(255, 149, 0, 0.1);
  border: 1px solid rgba(255, 149, 0, 0.2);
  color: #ff9500;
  font-weight: 600;
  font-size: 13px;
  padding: 8px 20px;
  border-radius: 100px;
  margin-bottom: 28px;
}

.maintenance-footer {
  font-size: 12.5px;
  color: #71717a;
  border-top: 1px solid rgba(255,255,255,0.06);
  padding-top: 20px;
}

@keyframes cardFadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes pulseIcon {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.06); }
}
</style>
