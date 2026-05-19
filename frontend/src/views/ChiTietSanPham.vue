<template>
  <div class="product-detail-page" v-if="product">
    <!-- Custom Toast Notification -->
    <transition name="toast">
      <div v-if="notification.show" class="toast-notification" :class="notification.type">
        <div class="toast-content">
          <div class="toast-icon-circle">
            <svg v-if="notification.type === 'success'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6L9 17l-5-5"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          </div>
          <span class="toast-message">{{ notification.message }}</span>
        </div>
      </div>
    </transition>
    <div class="product-container">
      <!-- Left: Gallery -->
      <div class="gallery-section">
        <div class="main-image-container">
          <img 
            :key="selectedImage || product.hinh_anh" 
            :src="selectedImage || product.hinh_anh" 
            :alt="product.ten" 
            class="main-image"
            :class="{ 'is-first': selectedImage === product.hinh_anh }"
          >
        </div>
        <div class="thumbnail-list" v-if="product.thu_vien_anh && product.thu_vien_anh.length > 0">
          <div 
            class="thumbnail-item" 
            :class="{ active: !selectedImage || selectedImage === product.hinh_anh }"
            @click="selectImage(product.hinh_anh, $event)"
          >
            <img :src="product.hinh_anh" alt="main">
          </div>
          <div 
            v-for="(img, idx) in product.thu_vien_anh" 
            :key="idx" 
            class="thumbnail-item"
            :class="{ active: selectedImage === img }"
            @click="selectImage(img, $event)"
          >
            <img :src="img" :alt="'gallery-' + idx">
          </div>
        </div>
      </div>

      <!-- Right: Info -->
      <div class="info-section">
        <div class="category-tag">{{ product.danh_muc }}</div>
        <h1 class="product-name">{{ product.ten }}</h1>
        <div class="product-price">{{ formatPrice(product.gia) }}</div>
        
        <!-- RAM Selection -->
        <div class="variant-section" v-if="ramList.length > 0">
          <div class="variant-label">RAM:</div>
          <div class="variant-options">
            <button 
              v-for="r in ramList" 
              :key="r" 
              class="variant-btn"
              :class="{ active: selectedRam === r }"
              @click="selectedRam = r"
            >{{ r }}</button>
          </div>
        </div>

        <!-- Storage Capacity Selection -->
        <div class="variant-section" v-if="dungLuongList.length > 0">
          <div class="variant-label">Dung lượng:</div>
          <div class="variant-options">
            <button 
              v-for="dl in dungLuongList" 
              :key="dl" 
              class="variant-btn"
              :class="{ active: selectedDungLuong === dl }"
              @click="selectedDungLuong = dl"
            >{{ dl }}</button>
          </div>
        </div>

        <!-- Color Selection -->
        <div class="variant-section" v-if="mauSacList.length > 0">
          <div class="variant-label">Màu sắc:</div>
          <div class="variant-options">
            <button 
              v-for="ms in mauSacList" 
              :key="ms" 
              class="color-btn"
              :class="{ active: selectedMauSac === ms }"
              :style="{ backgroundColor: ms }"
              @click="selectedMauSac = ms"
              :title="ms"
            ></button>
          </div>
        </div>

        <div class="attribute-box">
          <div class="attr-item">
            <span class="attr-label">Trạng thái:</span>
            <span v-if="product.so_luong_kho <= 0" class="status-stock" style="color: #FF3B30; background: rgba(255, 59, 48, 0.08); padding: 4px 8px; border-radius: 4px; font-weight: 700;">Hết hàng</span>
            <span v-else-if="product.so_luong_kho <= 5" class="status-stock" style="color: #FF9500; background: rgba(255, 149, 0, 0.08); padding: 4px 8px; border-radius: 4px; font-weight: 700;">Chỉ còn {{ product.so_luong_kho }} sản phẩm</span>
            <span v-else class="status-stock" style="color: #34C759; background: rgba(52, 199, 89, 0.08); padding: 4px 8px; border-radius: 4px; font-weight: 700;">Còn hàng ({{ product.so_luong_kho }} sản phẩm)</span>
          </div>
        </div>

        <div class="description-section">
          <h3>Mô tả sản phẩm</h3>
          <p class="description-text">{{ cleanDescription }}</p>
        </div>

        <div class="action-buttons">
          <button 
            class="btn-add-cart" 
            @click="addToCart(true)" 
            :disabled="submitting || product.so_luong_kho <= 0"
          >
            {{ product.so_luong_kho <= 0 ? 'Hết hàng' : (submitting ? 'Đang thêm...' : 'Thêm vào giỏ hàng') }}
          </button>
          <button 
            class="btn-buy-now" 
            @click="buyNow" 
            :disabled="submitting || product.so_luong_kho <= 0"
          >
            {{ product.so_luong_kho <= 0 ? 'Tạm hết hàng' : 'Mua ngay' }}
          </button>
          <button 
            class="btn-wishlist" 
            :class="{ active: isFavorite }" 
            @click="toggleFavorite"
            :title="isFavorite ? 'Xóa khỏi yêu thích' : 'Thêm vào yêu thích'"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" class="heart-icon">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
            </svg>
          </button>
        </div>

        <div class="policy-list">
          <div class="policy-item">✓ Bảo hành chính hãng 12 tháng</div>
          <div class="policy-item">✓ Đổi trả trong 30 ngày</div>
          <div class="policy-item">✓ Giao hàng miễn phí toàn quốc</div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="loading-state">
    <div class="spinner"></div>
    <p>Đang tải thông tin sản phẩm...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { sanPhamApi, gioHangApi, yeuThichApi } from '../services/api'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()

const route = useRoute()
const router = useRouter()
const product = ref(null)
const selectedImage = ref('')
const selectedRam = ref('')
const selectedDungLuong = ref('')
const selectedMauSac = ref('')
const submitting = ref(false)

const notification = ref({
  show: false,
  message: '',
  type: 'success'
})

const showToast = (msg, type = 'success') => {
  notification.value = { show: true, message: msg, type: type }
  setTimeout(() => { notification.value.show = false }, 3000)
}

const activePairings = computed(() => {
  if (!product.value?.mo_ta) return []
  const match = product.value.mo_ta.match(/<!--SPECS_PAIRINGS:(.*?)-->/)
  if (match) {
    try {
      return JSON.parse(match[1])
    } catch (e) {
      console.error("Lỗi parse pairings: ", e)
    }
  }
  return []
})

const cleanDescription = computed(() => {
  if (!product.value?.mo_ta) return ''
  return product.value.mo_ta.replace(/<!--SPECS_PAIRINGS:(.*?)-->/, '').trim()
})

const dungLuongList = computed(() => {
  if (activePairings.value.length > 0 && selectedRam.value) {
    const pair = activePairings.value.find(p => p.ram === selectedRam.value)
    if (pair && pair.capacities && pair.capacities.length > 0) {
      return pair.capacities
    }
  }
  if (!product.value?.dung_luong) return []
  return product.value.dung_luong.split(',').map(s => s.trim()).filter(Boolean)
})

const ramList = computed(() => {
  if (!product.value?.ram) return []
  return product.value.ram.split(',').map(s => s.trim()).filter(Boolean)
})

const mauSacList = computed(() => {
  if (!product.value?.mau_sac) return []
  return product.value.mau_sac.split(',').map(s => s.trim()).filter(Boolean)
})

watch(selectedRam, (newRam) => {
  if (newRam && activePairings.value.length > 0) {
    const pair = activePairings.value.find(p => p.ram === newRam)
    if (pair && pair.capacities && pair.capacities.length > 0) {
      if (!pair.capacities.includes(selectedDungLuong.value)) {
        selectedDungLuong.value = ''
      }
    }
  }
})

const selectImage = (img, event) => {
  selectedImage.value = img
  // Tự động cuộn ảnh được chọn vào giữa
  if (event && event.currentTarget) {
    event.currentTarget.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'center'
    })
  }
}

const handleWheel = (e) => {
  const container = document.querySelector('.thumbnail-list')
  if (container) {
    e.preventDefault()
    container.scrollLeft += e.deltaY
  }
}

const isFavorite = ref(false)

const checkFavoriteStatus = async () => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  if (!token || token === 'null' || token === 'undefined') {
    isFavorite.value = false
    return
  }
  try {
    const res = await yeuThichApi.checkWishlist(product.value.id)
    isFavorite.value = res.data.is_favorite
  } catch (e) {
    console.error("Lỗi kiểm tra yêu thích:", e)
  }
}

const toggleFavorite = async () => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  if (!token || token === 'null' || token === 'undefined') {
    showToast('Vui lòng đăng nhập để thêm sản phẩm vào danh sách yêu thích', 'error')
    return
  }
  try {
    const res = await yeuThichApi.toggleWishlist(product.value.id)
    if (res.data.status === 'da_them') {
      isFavorite.value = true
      showToast('Đã thêm vào danh sách yêu thích!', 'success')
    } else {
      isFavorite.value = false
      showToast('Đã xóa khỏi danh sách yêu thích', 'info')
    }
  } catch (e) {
    console.error("Lỗi khi thêm/xóa yêu thích:", e)
    showToast('Có lỗi xảy ra, vui lòng thử lại sau', 'error')
  }
}

const fetchProductDetail = async () => {
  try {
    const id = route.params.id
    const res = await sanPhamApi.getById(id)
    product.value = res.data
    selectedImage.value = product.value.hinh_anh
    checkFavoriteStatus()
  } catch (e) {
    console.error("Lỗi tải chi tiết sản phẩm:", e)
  }
}

const formatPrice = (p) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

const addToCart = async (showMsg = true) => {
  if (submitting.value) return

  // Bắt buộc chọn option và màu sắc nếu sản phẩm có các tùy chọn đó
  if (ramList.value.length > 0 && !selectedRam.value) {
    showToast('Vui lòng chọn dung lượng RAM!', 'error')
    return false
  }
  if (dungLuongList.value.length > 0 && !selectedDungLuong.value) {
    showToast('Vui lòng chọn dung lượng bộ nhớ trong!', 'error')
    return false
  }
  if (mauSacList.value.length > 0 && !selectedMauSac.value) {
    showToast('Vui lòng chọn màu sắc sản phẩm!', 'error')
    return false
  }

  submitting.value = true
  
  try {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token')
    if (!token || token === 'null' || token === 'undefined') {
      showToast('Vui lòng đăng nhập để mua hàng', 'error')
      localStorage.setItem('redirect_after_login', route.fullPath)
      setTimeout(() => router.push('/login'), 1500)
      return false
    }
    
    const payload = {
      san_pham_id: product.value.id,
      so_luong: 1,
      dung_luong: selectedDungLuong.value || "",
      ram: selectedRam.value || "",
      mau_sac: selectedMauSac.value || ""
    }
    
    const res = await gioHangApi.addToCart(payload)
    
    if (res.status === 200 || res.status === 201) {
      if (showMsg) showToast(`Đã thêm ${product.value.ten} vào giỏ hàng!`, 'success')
      // Cập nhật số lượng trên Navbar
      cartStore.fetchCart()
      
      // Thêm độ trễ nhân tạo để tránh spam nhanh
      await new Promise(r => setTimeout(r, 800))
      return true
    }
    return false
  } catch (e) {
    console.error("Lỗi giỏ hàng:", e)
    if (e.response && e.response.status !== 401) {
      showToast('Lỗi: ' + (e.response.data?.detail || 'Không thể thêm vào giỏ hàng'), 'error')
    }
    return false
  } finally {
    submitting.value = false
  }
}

const buyNow = async () => {
  const success = await addToCart(false)
  if (success) {
    router.push('/cart')
  }
}

onMounted(() => {
  fetchProductDetail()
  // Lắng nghe sự kiện cuộn chuột trên PC
  const container = document.querySelector('.thumbnail-list')
  if (container) {
    container.addEventListener('wheel', handleWheel, { passive: false })
  }
})
</script>

<style scoped>
.product-detail-page, .loading-state {
  padding: 20px 10px 100px; 
  background-color: #ffffff;
  min-height: 100vh;
  position: relative;
}

/* Toast Styles */
.toast-notification {
  position: fixed;
  top: 100px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  padding: 10px 20px;
  border-radius: 40px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
}

.toast-content { display: flex; align-items: center; gap: 10px; }
.toast-icon-circle { width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.toast-notification.success .toast-icon-circle { background: #28c840; color: white; }
.toast-notification.error .toast-icon-circle { background: #ff3b30; color: white; }
.toast-message { font-size: 13px; font-weight: 600; color: #1d1d1f; white-space: nowrap; }

.toast-enter-active, .toast-leave-active { transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1); }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translate(-50%, -40px); }

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.product-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr; 
  gap: 60px;
  align-items: start;
}

.gallery-section {
  width: 100%;
  min-width: 0; /* Quan trọng: Ngăn chặn item làm vỡ grid layout */
  overflow: hidden;
}

.main-image-container {
  background: transparent; 
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 85%;
  margin: 0 auto;
  aspect-ratio: 1;
  padding: 60px; 
}

.main-image {
  width: 170%; 
  height: 170%;
  object-fit: contain;
  display: block;
  transition: all 0.4s ease;

}

/* Style riêng dành cho ảnh đầu tiên */
.main-image.is-first {
  width: 100%; 
  height: 100%;
  transform: translateY(-20px); 
}

.thumbnail-list {
  display: flex;
  gap: 14px;
  justify-content: center; /* Căn giữa khi ít ảnh */
  margin-top: 10px; 
  overflow-x: auto;
  padding: 10px 0;
  width: 100%;
  scrollbar-width: none; /* Ẩn thanh cuộn trên Firefox */
  -ms-overflow-style: none; /* Ẩn thanh cuộn trên IE/Edge */
}

/* Đảm bảo khi cuộn trên PC không bị mất ảnh ở bên trái */
.thumbnail-list::before,
.thumbnail-list::after {
  content: '';
  margin: auto;
}

.thumbnail-item {
  width: 60px; 
  height: 60px;
  border-radius: 10px;
  border: 2px solid transparent;
  cursor: pointer;
  overflow: hidden;
  background: #ffffff;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.thumbnail-item.active { border-color: #007aff; }
.thumbnail-item img { width: 100%; height: 100%; object-fit: cover; } 

/* Info Styles */
.info-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-top: 70px; 
}

.category-tag {
  font-size: 11px;
  font-weight: 600;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.product-name {
  font-size: 32px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
  line-height: 1.1;
}

.product-price {
  font-size: 24px;
  font-weight: 500;
  color: #1d1d1f;
}

.variant-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.variant-label {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
}

.variant-options {
  display: flex;
  gap: 8px;
}

.variant-btn {
  padding: 8px 16px;
  border: 1px solid #d2d2d7;
  border-radius: 8px;
  background: white;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.variant-btn.active {
  border-color: #007aff;
  background: #007aff;
  color: white;
}

.color-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid #d2d2d7;
  cursor: pointer;
}

.color-btn.active { border-color: #007aff; box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.2); }

.attribute-box {
  border-top: 1px solid #e5e5e5;  
  border-bottom: 1px solid #e5e5e5;
  padding: 12px 0;
  font-size: 13px;
}

.status-stock { color: #28c840; font-weight: 600; margin-left: 5px; }

.description-section h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 6px;
}

.description-text { 
  color: #424245; 
  font-size: 14px; 
  line-height: 1.5; 
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

.btn-add-cart {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #007aff;
  color: #007aff;
  background: white;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
}

.btn-buy-now {
  flex: 1.5;
  padding: 12px;
  border-radius: 10px;
  background: #007aff;
  color: white;
  border: none;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
}

.policy-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.policy-item { font-size: 12px; color: #86868b; }

.btn-add-cart:disabled, .btn-buy-now:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  filter: grayscale(0.4);
  transform: none !important;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(0,122,255,0.1);
  border-top-color: #007aff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 850px) {
  .product-detail-page {
    padding: 60px 15px 100px; /* Giảm padding trên mobile */
  }

  .product-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .gallery-section {
    width: 100%;
    overflow: hidden; /* Chặn hoàn toàn tràn ngang */
  }

  .main-image-container {
    width: 100%;
    padding: 20px; /* Giảm padding ảnh chính trên mobile */
  }

  .thumbnail-list {
    justify-content: flex-start; /* Trên mobile nếu nhiều ảnh thì căn trái để dễ cuộn */
    /* Nếu ít ảnh vẫn muốn căn giữa thì dùng 'safe center' hoặc giữ nguyên 'center' */
    justify-content: center; 
    margin: 0;
    padding: 10px 0;
    width: 100%;
  }

  .thumbnail-item {
    width: 50px; /* Thu nhỏ ảnh thumb một chút trên mobile */
    height: 50px;
  }

  .info-section {
    padding-top: 0; /* Bỏ padding top vì đã stacking dọc */
  }

  .product-name {
    font-size: 26px;
  }

  .action-buttons {
    display: flex;
    flex-direction: row !important;
    gap: 10px;
  }

  .btn-add-cart {
    flex: 1 !important;
    padding: 14px 6px !important;
    font-size: 13px !important;
  }
  
  .btn-buy-now {
    flex: 1.2 !important;
    padding: 14px 6px !important;
    font-size: 13px !important;
  }
}

/* Ẩn thanh cuộn nhưng vẫn cho cuộn (tùy chọn để đẹp hơn) */
.thumbnail-list::-webkit-scrollbar {
  display: none;
}
.thumbnail-list {
  scrollbar-width: none;
}

.btn-wishlist {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 10px;
  background: #f5f5f7;
  border: none;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  color: #86868b;
  flex-shrink: 0;
}

.btn-wishlist:hover {
  background: #e8e8ed;
  color: #1d1d1f;
  transform: scale(1.05);
}

.btn-wishlist:active {
  transform: scale(0.95);
}

.btn-wishlist.active {
  background: #fff0f0;
  color: #ff3b30;
}

.btn-wishlist.active .heart-icon {
  fill: #ff3b30;
  stroke: #ff3b30;
}

.heart-icon {
  width: 20px;
  height: 20px;
  transition: all 0.2s ease;
}

@media (max-width: 850px) {
  .btn-wishlist {
    width: 48px !important;
    height: 48px !important;
    border-radius: 10px !important;
  }
}
</style>
