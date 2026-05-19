<template>
  <footer class="site-footer">
    <div class="footer-container">
      <!-- Breadcrumb & Socials Row -->
      <div class="footer-top-row">
        <nav class="footer-breadcrumb" v-if="currentPageName">
          <router-link to="/">Trang chủ</router-link>
          <span class="separator">></span>
          <span>{{ currentPageName }}</span>
        </nav>
        <div v-else class="footer-breadcrumb-empty"></div>
        
        <!-- Social Media Icons -->
        <div class="footer-socials">
          <a href="https://web.facebook.com/nguyen.huu.khanh.250505" target="_blank" rel="noopener noreferrer" class="social-btn facebook" title="Facebook">
            <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
          </a>
          <a href="https://www.tiktok.com/@nguyenhuukhanh_0" target="_blank" rel="noopener noreferrer" class="social-btn tiktok" title="TikTok">
            <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.01 1.62 4.19 1.11 1.22 2.6 1.98 4.19 2.22v3.74c-1.8-.1-3.56-.83-4.96-1.97-.07-.06-.11-.06-.14 0-.15.4-.33.78-.53 1.15-.02.04-.01.07.01.1 1.01 1.25 1.57 2.82 1.57 4.43 0 3.91-3.17 7.08-7.08 7.08-3.91 0-7.08-3.17-7.08-7.08 0-3.87 3.1-7.02 6.96-7.08v3.75c-2.07.13-3.69 1.86-3.69 3.93 0 2.18 1.77 3.95 3.95 3.95s3.95-1.77 3.95-3.95c0-.88-.29-1.72-.82-2.4l-.11-.14c-.03-.04-.02-.08.02-.1.3-.43.55-.9.75-1.39.02-.05.01-.1-.03-.13-1.07-.76-1.71-1.98-1.71-3.29V0h.01z"/>
            </svg>
          </a>
        </div>
      </div>

      <!-- Main Columns (Accordion on Mobile) -->
      <div class="footer-grid">
        <div class="footer-column" :class="{ 'is-open': openSection === 'shopping' }">
          <h3 @click="toggleSection('shopping')">
            Mua sắm
            <span class="toggle-icon">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
            </span>
          </h3>
          <div class="column-links">
            <router-link to="/dien-thoai">iPhone</router-link>
            <router-link to="/may-tinh-bang">iPad</router-link>
            <router-link to="/laptop">MacBook</router-link>
            <router-link to="/phu-kien">Phụ kiện</router-link>
          </div>
        </div>

        <div class="footer-column" :class="{ 'is-open': openSection === 'services' }">
          <h3 @click="toggleSection('services')">
            Dịch vụ
            <span class="toggle-icon">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
            </span>
          </h3>
          <div class="column-links">
            <a href="#" @click.prevent="showInfo('Tư vấn mua hàng', 'Peach Store hỗ trợ tư vấn trực tuyến 24/7. Bạn có thể sử dụng Trợ lý AI ở góc phải màn hình hoặc gọi Hotline miễn phí 1800-PEACH để gặp kỹ thuật viên tư vấn chi tiết.', '💬')">Tư vấn mua hàng</a>
            <a href="#" @click.prevent="showInfo('Chính sách Bán đổi trả', 'Áp dụng đổi trả miễn phí trong vòng 30 ngày đối với tất cả sản phẩm lỗi do nhà sản xuất. Sản phẩm đổi trả yêu cầu nguyên hộp và còn nguyên tem niêm phong ban đầu.', '🔄')">Bán đổi trả</a>
            <a href="#" @click.prevent="showInfo('Thu cũ đổi mới', 'Chương trình hỗ trợ lên đời dòng máy iPhone, iPad, MacBook mới tại Peach Store với giá thu mua máy cũ cao nhất thị trường, trợ giá thêm lên tới 2.000.000đ.', '📲')">Lên đời máy mới</a>
            <a href="#" @click.prevent="showInfo('Thu cũ đổi mới', 'Chương trình hỗ trợ lên đời dòng máy iPhone, iPad, MacBook mới tại Peach Store với giá thu mua máy cũ cao nhất thị trường, trợ giá thêm lên tới 2.000.000đ.', '📲')">Thu cũ đổi mới</a>
          </div>
        </div>

        <div class="footer-column" :class="{ 'is-open': openSection === 'account' }">
          <h3 @click="toggleSection('account')">
            Tài khoản
            <span class="toggle-icon">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
            </span>
          </h3>
          <div class="column-links">
            <a href="#" @click.prevent="showInfo('Quản lý Peach ID', 'Peach ID giúp bạn đồng bộ giỏ hàng, lịch sử mua sắm và nhận ưu đãi tích điểm thành viên hạng thẻ Vàng/Bạc/Kim cương trên toàn hệ thống Peach Store.', '👤')">Quản lý Peach ID</a>
            <a href="#" @click.prevent="showInfo('Tài khoản thành viên', 'Đăng nhập Peach ID giúp lưu thông tin nhận hàng, lịch sử giao dịch và điểm tích lũy mua sắm sản phẩm công nghệ của bạn.', '🔑')">Tài khoản</a>
            <a href="#" @click.prevent="showInfo('Liên kết iCloud.com', 'Trang web đồng bộ dữ liệu đám mây của Apple. Lưu ý: Mọi giao dịch mua hàng tại Peach Store được lưu tại tài khoản ID Peach Store riêng biệt của bạn.', '☁️')">iCloud.com</a>
          </div>
        </div>

        <div class="footer-column" :class="{ 'is-open': openSection === 'support' }">
          <h3 @click="toggleSection('support')">
            Hỗ trợ
            <span class="toggle-icon">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
            </span>
          </h3>
          <div class="column-links">
            <router-link to="/ho-tro">Trung tâm hỗ trợ</router-link>
            <a href="#" @click.prevent="showInfo('Hệ thống Peach Store', 'Hệ thống có 5 chi nhánh chính thức tại Hà Nội, Đà Nẵng và TP. Hồ Chí Minh. Các cửa hàng mở cửa từ 8:00 đến 22:00 hàng ngày, kể cả ngày lễ.', '📍')">Tìm cửa hàng</a>
            <a href="#" @click.prevent="showInfo('Kiểm tra đơn hàng', 'Sau khi đặt hàng, bạn có thể kiểm tra trạng thái vận chuyển qua email xác nhận hoặc liên hệ trực tiếp CSKH qua Peach Assistant để nhận mã vận đơn.', '📦')">Trạng thái đơn hàng</a>
            <router-link to="/nhan-vien/dang-nhap">Cổng Nhân Viên</router-link>
          </div>
        </div>
      </div>

      <!-- Secondary Info -->
      <div class="footer-info">
        <p>
          Xem thêm các cách để mua sắm: 
          <a href="#" @click.prevent="showInfo('Hệ thống Peach Store', 'Hệ thống có 5 chi nhánh chính thức tại Hà Nội, Đà Nẵng và TP. Hồ Chí Minh. Các cửa hàng mở cửa từ 8:00 đến 22:00 hàng ngày, kể cả ngày lễ.', '📍')" class="blue-link">Tìm một Cửa Hàng Peach Store</a> 
          hoặc <a href="#" @click.prevent="showInfo('Đối tác phân phối', 'Peach Store liên kết với các chuỗi bán lẻ công nghệ ủy quyền chính thức từ Apple trên toàn quốc để hỗ trợ khách hàng bảo hành nhanh nhất.', '🤝')" class="blue-link">nhà bán lẻ khác</a> gần bạn. 
          Hoặc gọi 1800-PEACH.
        </p>
      </div>

      <!-- Bottom Bar -->
      <div class="footer-bottom">
        <div class="copyright">
          {{ footerText }}
        </div>
        <div class="legal-links">
          <a href="#" @click.prevent="showInfo('Chính sách bảo mật', 'Peach Store cam kết bảo vệ tuyệt đối thông tin cá nhân và dữ liệu thanh toán của khách hàng. Chúng tôi không bao giờ chia sẻ thông tin của bạn cho bên thứ ba.', '🔒')">Chính sách bảo mật</a>
          <a href="#" @click.prevent="showInfo('Sử dụng Cookies', 'Chúng tôi sử dụng cookie để ghi nhớ giỏ hàng và tối ưu hóa tốc độ tải trang web, mang lại trải nghiệm duyệt sản phẩm mượt mà nhất cho bạn.', '🍪')">Sử dụng Cookies</a>
          <a href="#" @click.prevent="showInfo('Điều khoản sử dụng', 'Bằng việc sử dụng website Peach Store, bạn đồng ý với các điều khoản bảo hành sản phẩm chính hãng và thanh toán an toàn được Apple ủy quyền.', '📝')">Điều khoản sử dụng</a>
          <a href="#" @click.prevent="showInfo('Sơ đồ trang web', 'Bản đồ cấu trúc danh mục gồm: Trang chủ, iPhone, iPad, MacBook, Phụ kiện, Cổng hỗ trợ kỹ thuật và Cổng quản lý lịch nhân viên.', '🗺️')">Sơ đồ trang web</a>
        </div>
      </div>
    </div>

    <!-- Cupertino Information Modal Overlay -->
    <transition name="modal-fade">
      <div v-if="infoModal.show" class="info-modal-overlay" @click.self="infoModal.show = false">
        <div :class="['info-modal-card', { 'is-map-modal': infoModal.title === 'Hệ thống Peach Store' }]">
          <!-- Chỉ hiện icon nếu KHÔNG PHẢI là bản đồ -->
          <div v-if="infoModal.title !== 'Hệ thống Peach Store'" class="info-modal-icon">{{ infoModal.icon }}</div>
          <h3 class="info-modal-title">{{ infoModal.title }}</h3>
          
          <div v-if="infoModal.title === 'Hệ thống Peach Store'" class="map-embed-container">
            <iframe 
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3918.4749787803385!2d106.7580641!3d10.8514325!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752797e321f8e9%3A0xb3ff69197b10ec4f!2sThu%20Duc%20College%20of%20Technology!5e0!3m2!1sen!2s!4v1779161920391!5m2!1sen!2s" 
              class="map-iframe"
              style="border:0;" 
              allowfullscreen="" 
              loading="lazy" 
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
            <div class="map-address-box">
              <span class="map-pin-icon">📍</span>
              <span class="map-address-text"><strong>Trường Cao đẳng Công nghệ Thủ Đức</strong><br>53 Võ Văn Ngân, Linh Chiểu, Thủ Đức, Hồ Chí Minh</span>
            </div>
          </div>
          <p v-else class="info-modal-desc">{{ infoModal.description }}</p>
          
          <button class="info-modal-btn" @click="infoModal.show = false">Đã hiểu</button>
        </div>
      </div>
    </transition>
  </footer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const openSection = ref('');
const footerText = ref('Bản quyền © 2025 Peach Store. Bảo lưu mọi quyền.');

// Info Modal State
const infoModal = ref({
  show: false,
  title: '',
  description: '',
  icon: 'ℹ️'
});

const showInfo = (title, description, icon = 'ℹ️') => {
  infoModal.value = {
    show: true,
    title: title,
    description: description,
    icon: icon
  };
};

const routeNameMap = {
  'TrangChu': 'Peach Store',
  'DienThoai': 'Điện thoại',
  'MayTinhBang': 'Máy tính bảng',
  'Laptop': 'Laptop',
  'PhuKien': 'Phụ kiện',
  'HoTro': 'Hỗ trợ',
  'TaiKhoan': 'Tài khoản',
  'GioHang': 'Giỏ hàng',
  'ChiTietSanPham': 'Chi tiết sản phẩm'
};

const currentPageName = computed(() => {
  return routeNameMap[route.name] || '';
});

const toggleSection = (section) => {
  if (window.innerWidth > 768) return;
  openSection.value = openSection.value === section ? '' : section;
};

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/admin/config');
    if (res.ok) {
      const data = await res.json();
      if (data && data.footerText) {
        footerText.value = data.footerText;
      }
    }
  } catch (e) {
    console.error("Lỗi đồng bộ footerText: ", e);
  }
});
</script>

<style scoped>
.site-footer {
  background-color: rgba(245, 245, 247, 0.8); /* Trả về màu xám tráng gương Apple */
  backdrop-filter: blur(40px) saturate(150%); 
  -webkit-backdrop-filter: blur(40px) saturate(150%);
  padding: 60px 0 80px;
  border-top: 1px solid #d2d2d7;
  position: relative;
  z-index: 10;
}

.footer-container {
  max-width: 1024px;
  margin: 0 auto;
  padding: 0 22px;
}

.footer-breadcrumb {
  font-size: 12px;
  color: #515154;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-breadcrumb a {
  color: #515154;
  text-decoration: none;
}

.footer-breadcrumb a:hover {
  text-decoration: underline;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding-top: 20px;
  border-top: 1px solid #d2d2d7;
  margin-bottom: 30px;
}

.footer-column h3 {
  font-size: 12px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-icon {
  display: none; /* Ẩn trên desktop */
  transition: transform 0.3s ease;
}

.footer-column.is-open .toggle-icon {
  transform: rotate(180deg);
}

.footer-column a {
  display: block;
  font-size: 12px;
  color: #424245;
  text-decoration: none;
  margin-bottom: 8px;
  transition: color 0.2s;
}

.footer-column a:hover {
  text-decoration: underline;
  color: #1d1d1f;
}

.footer-info {
  font-size: 12px;
  color: #86868b;
  border-bottom: 1px solid #d2d2d7;
  padding-bottom: 15px;
  margin-bottom: 15px;
  text-align: center;
}

.blue-link {
  color: #0066cc;
  text-decoration: none;
}

.footer-bottom {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  font-size: 12px;
  color: #86868b;
  gap: 10px;
}

.legal-links {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 6px 0;
}

.legal-links a {
  color: #515154;
  text-decoration: none;
  font-size: 11px;
  transition: color 0.2s ease;
}

.legal-links a:hover {
  color: #1d1d1f;
  text-decoration: underline;
}

.legal-links a:not(:last-child)::after {
  content: "|";
  margin: 0 10px;
  color: #ccc;
  pointer-events: none;
  font-weight: 300;
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 0;
    margin-bottom: 20px;
  }
  
  .footer-column {
    border-bottom: 1px solid #d2d2d7;
  }

  .footer-column h3 {
    padding: 12px 0;
    margin-bottom: 0;
    cursor: pointer;
  }

  .toggle-icon {
    display: flex;
  }

  .column-links {
    height: 0;
    overflow: hidden;
    transition: height 0.3s ease, padding 0.3s ease;
    padding-left: 10px;
  }

  .footer-column.is-open .column-links {
    height: auto;
    padding-bottom: 12px;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 12px;
    align-items: center;
    text-align: center;
  }

  .legal-links {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    gap: 12px 0;
  }

  .legal-links a {
    width: 50%;
    padding: 0;
    margin: 0;
    border-bottom: none;
    display: inline-block;
    font-size: 11.5px;
    color: #6e6e73;
    box-sizing: border-box;
  }

  .legal-links a:nth-child(odd) {
    text-align: right;
    padding-right: 12px;
  }

  .legal-links a:nth-child(even) {
    text-align: left;
    padding-left: 12px;
    border-left: 1px solid #d2d2d7;
  }

  .legal-links a::after {
    display: none !important;
  }
}

/* Cupertino Information Modal Overlay & Card Styling */
.info-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px) saturate(180%);
  -webkit-backdrop-filter: blur(15px) saturate(180%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
}

.info-modal-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(30px) saturate(200%);
  -webkit-backdrop-filter: blur(30px) saturate(200%);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 24px;
  width: 90%;
  max-width: 380px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12), 0 1px 3px rgba(0, 0, 0, 0.05);
  transform: scale(1);
  box-sizing: border-box;
}

.info-modal-icon {
  font-size: 44px;
  margin-bottom: 16px;
  display: inline-block;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.05));
}

.info-modal-title {
  font-size: 19px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 12px 0 !important;
  letter-spacing: -0.5px;
}

.info-modal-desc {
  font-size: 13.5px;
  line-height: 1.6;
  color: #515154;
  margin: 0 0 24px 0 !important;
  font-weight: 500;
}

.info-modal-btn {
  background: #007aff;
  color: #ffffff;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  width: 100%;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.2);
}

.info-modal-btn:hover {
  background: #0066cc;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 122, 255, 0.3);
}

.info-modal-btn:active {
  transform: translateY(0);
}

/* Modal Pop & Fade Animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

.modal-fade-enter-active .info-modal-card {
  animation: modalScaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-fade-leave-active .info-modal-card {
  animation: modalScaleDown 0.2s cubic-bezier(0.25, 1, 0.5, 1);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@keyframes modalScaleUp {
  from { transform: scale(0.92); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes modalScaleDown {
  from { transform: scale(1); opacity: 1; }
  to { transform: scale(0.95); opacity: 0; }
}

/* --- PREMIUM MAP EMBED MODAL STYLES --- */
.info-modal-card.is-map-modal {
  max-width: 580px !important;
  padding: 20px 24px !important;
}

.map-embed-container {
  margin: 16px 0 20px;
  width: 100%;
}

.map-iframe {
  width: 100%;
  height: 220px;
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.map-address-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 12px;
  padding: 10px 14px;
  margin-top: 12px;
  text-align: left;
}

.map-pin-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.map-address-text {
  font-size: 13px;
  color: #424245;
  font-family: 'Outfit', sans-serif;
  line-height: 1.45;
}

/* --- FOOTER SOCIAL MEDIA BUTTONS --- */
.footer-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.footer-breadcrumb {
  margin-bottom: 0 !important;
}

.footer-socials {
  display: flex;
  gap: 12px;
  align-items: center;
}

.social-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #515154;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(0, 0, 0, 0.03);
}

.social-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.social-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.social-btn:hover .social-icon {
  transform: scale(1.08);
}

.social-btn.facebook:hover {
  background: #1877f2 !important;
  color: #ffffff !important;
  border-color: #1877f2 !important;
}

.social-btn.tiktok:hover {
  background: #000000 !important;
  color: #ffffff !important;
  border-color: #000000 !important;
}
</style>
