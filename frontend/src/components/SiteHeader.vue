<template>
  <header :class="['site-header', { 'is-scrolled': isScrolled }]">
    <div class="nav-container">
      <nav class="site-nav">
        <!-- Logo thương hiệu -->
        <router-link to="/" class="nav-item logo">
          <img src="@/assets/images/logo.svg" alt="MangoStore" />
        </router-link>

        <!-- Các liên kết sản phẩm -->
        <router-link to="/dien-thoai" class="nav-item text-link">{{ t.iphone }}</router-link>
        <router-link to="/may-tinh-bang" class="nav-item text-link">{{ t.ipad }}</router-link>
        <router-link to="/laptop" class="nav-item text-link">{{ t.macbook }}</router-link>
        <router-link to="/phu-kien" class="nav-item text-link">{{ t.accessories }}</router-link>
        <router-link to="/ho-tro" class="nav-item text-link">{{ t.support }}</router-link>

        <!-- Nhóm icon chức năng bên phải -->
        <div class="nav-actions">
          <button class="nav-item action-btn" aria-label="Tìm kiếm" @click="openSearch">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </button>
          
          <router-link to="/account" class="nav-item action-btn account-btn" aria-label="Tài khoản">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span v-if="headerNotificationCount > 0" class="bag-count">{{ headerNotificationCount }}</span>
          </router-link>


          <router-link to="/cart" class="nav-item action-btn bag-btn" aria-label="Giỏ hàng">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="6" width="18" height="15" rx="2" ry="2"></rect>
              <path d="M3 6l3-4h12l3 4"></path>
              <path d="M9 11a3 3 0 0 0 6 0"></path>
            </svg>
            <span v-if="cartCount > 0" class="bag-count">{{ cartCount }}</span>
          </router-link>

          <!-- Hamburger menu button (mobile) -->
          <button class="nav-item action-btn hamburger-btn" aria-label="Menu" @click="toggleMenu">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
              <line v-if="!menuVisible" x1="4" y1="8" x2="20" y2="8"></line>
              <line v-if="!menuVisible" x1="4" y1="16" x2="20" y2="16"></line>
              
              <line v-if="menuVisible" x1="18" y1="6" x2="6" y2="18"></line>
              <line v-if="menuVisible" x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </nav>
    </div>
  </header>

  <!-- Menu mobile -->
  <MenuHidden :visible="menuVisible" @close="closeMenu" />

  <!-- Premium Search Overlay Backdrop (Full screen glassmorphism) -->
  <Transition name="fade">
    <div v-if="showSearch" class="search-overlay" @click.self="closeSearch">
      <div class="search-container">
        <!-- Search input header -->
        <div class="search-input-wrapper">
          <svg class="search-input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            ref="searchInputRef"
            type="text"
            v-model="searchQuery"
            placeholder="Bạn muốn tìm sản phẩm nào?"
            class="search-input"
            @keyup.esc="closeSearch"
          />
          <button class="clear-search-btn" @click="closeSearch" aria-label="Đóng">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- Search suggestions or results list -->
        <div class="search-results-wrapper">
          <!-- Loading state -->
          <div v-if="loadingSearch" class="search-loading">
            <div class="spinner"></div>
            <span>Đang tải danh sách sản phẩm...</span>
          </div>

          <!-- Empty initial state (quick suggestions) -->
          <div v-else-if="!searchQuery.trim()" class="search-suggestions">
            <h4 class="suggestions-title">Gợi ý tìm kiếm</h4>
            <div class="suggestion-tags">
              <button class="suggestion-tag" @click="searchQuery = 'iPhone'">iPhone 16</button>
              <button class="suggestion-tag" @click="searchQuery = 'iPad'">iPad Air</button>
              <button class="suggestion-tag" @click="searchQuery = 'MacBook'">MacBook Pro</button>
              <button class="suggestion-tag" @click="searchQuery = 'Tai nghe'">Tai nghe</button>
            </div>
          </div>

          <!-- Results list -->
          <div v-else-if="filteredProducts.length > 0" class="search-results-list">
            <h4 class="results-title">Sản phẩm tìm thấy ({{ filteredProducts.length }})</h4>
            <div 
              v-for="p in filteredProducts" 
              :key="p.id" 
              class="search-result-item"
              @click="goToProduct(p)"
            >
              <div class="result-image-wrap">
                <img :src="p.hinh_anh || '/images/default-product.png'" :alt="p.ten" class="result-img" />
              </div>
              <div class="result-info">
                <h5 class="result-name">{{ p.ten }}</h5>
                <span class="result-price">{{ formatPrice(p.gia) }}</span>
              </div>
              <div class="result-action">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </div>
            </div>
          </div>

          <!-- No results state -->
          <div v-else class="search-no-results">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" class="no-results-icon">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <span>Không tìm thấy sản phẩm "{{ searchQuery }}" phù hợp.</span>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>


<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import MenuHidden from './menuhidden.vue';
import { useCartStore } from '../stores/cart';
import { xacThucApi, voucherApi, yeuThichApi, sanPhamApi } from '../services/api';
import { useRouter } from 'vue-router';

const router = useRouter();
const cartStore = useCartStore();
const cartCount = computed(() => cartStore.count);
const menuVisible = ref(false);
const isScrolled = ref(false);

// Trạng thái tìm kiếm cao cấp
const showSearch = ref(false);
const searchQuery = ref('');
const allProducts = ref([]);
const loadingSearch = ref(false);
const searchInputRef = ref(null);

const removeAccents = (str) => {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
};

const openSearch = async () => {
  showSearch.value = true;
  loadingSearch.value = true;
  // Focus tự động vào input
  setTimeout(() => {
    if (searchInputRef.value) {
      searchInputRef.value.focus();
    }
  }, 100);
  try {
    const res = await sanPhamApi.getAll();
    allProducts.value = res.data || [];
  } catch (err) {
    console.error("Lỗi lấy danh sách sản phẩm header:", err);
  } finally {
    loadingSearch.value = false;
  }
};

const closeSearch = () => {
  showSearch.value = false;
  searchQuery.value = '';
};

const filteredProducts = computed(() => {
  if (!searchQuery.value.trim()) return [];
  const queryClean = removeAccents(searchQuery.value.trim());
  return allProducts.value.filter(p => {
    const nameClean = removeAccents(p.ten || '');
    const descClean = removeAccents(p.mo_ta || '');
    return nameClean.includes(queryClean) || descClean.includes(queryClean);
  }).slice(0, 5); // Giới hạn tối đa 5 sản phẩm hiển thị gọn gàng
});

const goToProduct = (product) => {
  closeSearch();
  router.push('/san-pham/' + product.id);
};

const formatPrice = (value) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
};
const lang = ref('vi');
const t = computed(() => {
  if (lang.value === 'en') {
    return {
      iphone: "iPhone",
      ipad: "iPad",
      macbook: "MacBook",
      accessories: "Accessories",
      support: "Support"
    };
  }
  return {
    iphone: "Điện thoại",
    ipad: "Máy tính bảng",
    macbook: "Laptop",
    accessories: "Phụ kiện",
    support: "Hỗ trợ"
  };
});

const headerNotificationCount = ref(0);
let headerPollingInterval = null;

const fetchHeaderNotificationCount = async () => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token');
  if (!token || token === 'null' || token === 'undefined') {
    headerNotificationCount.value = 0;
    return;
  }
  
  try {
    const [resNotif, resVouchers, resChat, resWishlist] = await Promise.all([
      xacThucApi.getNotifications().catch(() => ({ data: [] })),
      voucherApi.getUserVouchers().catch(() => ({ data: [] })),
      xacThucApi.getChatMessages().catch(() => ({ data: [] })),
      yeuThichApi.getWishlist().catch(() => ({ data: [] }))
    ]);
    
    // 1. Thông báo chưa đọc
    const readNotificationIds = JSON.parse(localStorage.getItem('read_notification_ids') || '[]');
    const unreadNotifCount = (resNotif.data || []).filter(n => !readNotificationIds.includes(n.id)).slice(0, 20).length;
    
    // 2. Vouchers hiện có
    const vouchersCount = (resVouchers.data || []).length;
    
    // 3. Sản phẩm yêu thích (Wishlist)
    const wishlistCount = (resWishlist.data || []).length;
    
    // 4. Tin nhắn hỗ trợ từ Admin
    const chatMessages = resChat.data || [];
    let unreadChatCount = 0;
    const isAtChatTab = window.location.pathname.includes('/account') && (window.location.search.includes('tab=chat') || window.location.hash.includes('chat'));
    if (!isAtChatTab) {
      const readChatIds = JSON.parse(localStorage.getItem('read_chat_ids') || '[]');
      unreadChatCount = chatMessages.filter(msg => msg.sender !== 'user' && !readChatIds.includes(msg.id)).length;
    }
    
    headerNotificationCount.value = unreadNotifCount + vouchersCount + wishlistCount + unreadChatCount;
  } catch (error) {
    console.error('Lỗi khi cập nhật số lượng thông báo header:', error);
  }
};

const startHeaderPolling = () => {
  stopHeaderPolling();
  fetchHeaderNotificationCount();
  headerPollingInterval = setInterval(fetchHeaderNotificationCount, 10000);
};

const stopHeaderPolling = () => {
  if (headerPollingInterval) {
    clearInterval(headerPollingInterval);
    headerPollingInterval = null;
  }
};

const toggleMenu = () => {
  menuVisible.value = !menuVisible.value;
};

const closeMenu = () => {
  menuVisible.value = false;
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

onMounted(async () => {
  window.addEventListener('scroll', handleScroll);
  cartStore.fetchCart();
  startHeaderPolling();

  try {
    const res = await fetch('http://127.0.0.1:8000/api/admin/config');
    if (res.ok) {
      const data = await res.json();
      if (data && data.defaultLanguage) {
        lang.value = data.defaultLanguage;
      }
    }
  } catch (e) {
    console.error("Lỗi lấy ngôn ngữ header: ", e);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  stopHeaderPolling();
});
</script>


<style scoped>
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 48px;
  background: rgba(251, 251, 253, 0.8);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  z-index: 9999;
  transition: background 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.site-header.is-scrolled {
  background: rgba(255, 255, 255, 0.92);
  border-bottom: 0.5px solid rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1024px;
  margin: 0 auto;
  height: 100%;
  padding: 0 22px;
}

.site-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 38px;
  height: 100%;
  user-select: none;
}

.nav-item {
  display: flex;
  align-items: center;
  height: 100%;
  text-decoration: none;
  color: #1d1d1f;
  transition: transform 0.1s;
  outline: none; 
}

.nav-item svg,
.nav-item.text-link {
  opacity: 0.8;
  transition: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover svg,
.nav-item:hover.text-link {
  opacity: 1;
}

.nav-item:focus {
  outline: none;
}

.router-link-active svg,
.router-link-active.text-link {
  opacity: 1 !important;
}

.router-link-active {
  font-weight: 500;
}

.logo img {
  height: 28px;
  width: auto;
}

.text-link {
  font-size: 12px;
  font-weight: 400;
  letter-spacing: -0.01em;
}

.action-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-item:active {
  transform: scale(0.92);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 25px; /* Giãn cách giữa các icon */
  height: 100%;
}

.bag-btn,
.account-btn {
  position: relative;
}

.bag-count {
  position: absolute;
  top: 8px;
  right: -8px;
  background: #ff3b30; 
  color: white;
  font-size: 10px;
  font-weight: 700;
  min-width: 15px;
  height: 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}



/* Hamburger button: ẩn trên desktop, hiện trên mobile */
.hamburger-btn {
  display: none;
}

@media (max-width: 734px) {
  .hamburger-btn {
    display: flex;
  }
}

/* Responsive cho Mobile */
@media (max-width: 834px) {
  .site-nav {
    gap: 25px;
    
  }
}

@media (max-width: 734px) {
  .text-link {
    display: none;
  }
  .site-nav {
    justify-content: space-between;
    gap: 0;
  }
  .nav-actions {
    gap: 15px; /* Giảm khoảng cách icon trên màn hình nhỏ */
  }
}

/* --- PREMIUM SEARCH OVERLAY STYLES --- */
.search-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.45); /* Nền tối mờ kiểu rạp phim */
  backdrop-filter: blur(20px) saturate(180%); /* Kính mờ siêu sâu kiểu Apple */
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  z-index: 10000; /* Hiển thị đè lên tất cả */
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 80px; /* Cách mép trên để vừa mắt */
  box-sizing: border-box;
}

.search-container {
  background: rgba(255, 255, 255, 0.85); /* Nền kính gương ngọc trắng sáng cực sang */
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 24px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, 0.15);
  padding: 20px;
  box-sizing: border-box;
  animation: searchSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes searchSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.04);
  border-radius: 14px;
  padding: 10px 16px;
  gap: 12px;
}

.search-input-icon {
  color: #86868b;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-size: 16px;
  color: #1d1d1f;
  font-family: 'Outfit', -apple-system, sans-serif;
  font-weight: 400;
  width: 100%;
}

.search-input::placeholder {
  color: #86868b;
}

.clear-search-btn {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: #86868b;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s, color 0.2s;
}

.clear-search-btn:hover {
  background: rgba(0, 0, 0, 0.08);
  color: #1d1d1f;
}

.search-results-wrapper {
  margin-top: 16px;
  max-height: 380px;
  overflow-y: auto;
}

/* Custom Scrollbar cho sang */
.search-results-wrapper::-webkit-scrollbar {
  width: 5px;
}
.search-results-wrapper::-webkit-scrollbar-track {
  background: transparent;
}
.search-results-wrapper::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.search-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 0;
  color: #86868b;
  font-size: 14px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid rgba(0, 122, 255, 0.1);
  border-top-color: #007aff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.search-suggestions {
  padding: 10px 4px;
}

.suggestions-title,
.results-title {
  font-size: 12px;
  font-weight: 500;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
  font-family: 'Outfit', sans-serif;
}

.suggestion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.suggestion-tag {
  background: rgba(0, 0, 0, 0.04);
  color: #1d1d1f;
  border: none;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  font-family: 'Outfit', sans-serif;
  transition: background 0.2s, transform 0.1s;
}

.suggestion-tag:hover {
  background: rgba(0, 0, 0, 0.08);
}

.suggestion-tag:active {
  transform: scale(0.96);
}

.search-results-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.search-result-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  gap: 16px;
}

.search-result-item:hover {
  background: rgba(0, 0, 0, 0.03);
}

.search-result-item:active {
  transform: scale(0.99);
}

.result-image-wrap {
  width: 50px;
  height: 50px;
  background: #ffffff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid rgba(0, 0, 0, 0.03);
  padding: 4px;
  box-sizing: border-box;
}

.result-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.result-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.result-name {
  font-size: 15px;
  font-weight: 500;
  color: #1d1d1f;
  margin: 0;
  font-family: 'Outfit', sans-serif;
}

.result-price {
  font-size: 13px;
  color: #86868b;
}

.result-action {
  color: #86868b;
  opacity: 0;
  transition: opacity 0.2s;
}

.search-result-item:hover .result-action {
  opacity: 1;
}

.search-no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #86868b;
  gap: 12px;
  font-size: 14px;
  text-align: center;
}

.no-results-icon {
  color: #c7c7cc;
}

/* Transition Anim */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>


