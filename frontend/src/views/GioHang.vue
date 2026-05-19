<template>
  <div class="cart-page">
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

    <!-- Custom Confirmation Modal -->
    <transition name="fade">
      <div v-if="confirmModal.show" class="modal-backdrop" @click.self="closeConfirm">
        <div class="confirm-modal">
          <div class="confirm-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ff3b30" stroke-width="2">
              <path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
            </svg>
          </div>
          <h3>{{ confirmModal.title }}</h3>
          <p>{{ confirmModal.message }}</p>
          <div class="modal-actions">
            <button class="modal-btn cancel" @click="closeConfirm">Hủy</button>
            <button class="modal-btn confirm" @click="handleConfirm">Xác nhận</button>
          </div>
        </div>
      </div>
    </transition>
    <div class="cart-container" v-if="cartItems.length > 0">
      <div class="cart-header">
        <div class="header-main">
          <h1>Giỏ hàng của bạn</h1>
          <span class="cart-count">{{ cartItems.length }} sản phẩm</span>
        </div>
        <div class="header-actions" v-if="cartItems.length > 0">
          <label class="select-all">
            <div class="custom-checkbox">
              <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" />
              <span class="checkmark"></span>
            </div>
            <span>Chọn tất cả</span>
          </label>
          <button 
            v-if="selectedItems.length > 0" 
            class="remove-selected-btn" 
            @click="removeSelectedItems"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
            </svg>
            Xóa {{ selectedItems.length }} sản phẩm đã chọn
          </button>
        </div>
      </div>

      <div class="cart-items">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <div class="item-checkbox">
            <div class="custom-checkbox">
              <input type="checkbox" :value="item.id" v-model="selectedItems" />
              <span class="checkmark"></span>
            </div>
          </div>
          <div class="item-image">
            <img :src="item.san_pham?.hinh_anh || 'https://via.placeholder.com/80'" :alt="item.san_pham?.ten" />
          </div>
          <div class="item-info">
            <h3 class="item-name">{{ item.san_pham?.ten }}</h3>
              <div class="item-specs">
                <span v-if="item.ram" class="item-spec ram">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <path d="M6 19v2"></path>
                    <path d="M10 19v2"></path>
                    <path d="M14 19v2"></path>
                    <path d="M18 19v2"></path>
                    <path d="M6 3v2"></path>
                    <path d="M10 3v2"></path>
                    <path d="M14 3v2"></path>
                    <path d="M18 3v2"></path>
                    <rect x="2" y="5" width="20" height="14" rx="2"></rect>
                  </svg>
                  RAM {{ item.ram }}
                </span>
                <span v-if="item.dung_luong" class="item-spec capacity">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <rect x="2" y="2" width="20" height="20" rx="2" ry="2"></rect>
                    <path d="M7 2v20"></path>
                    <path d="M17 2v20"></path>
                    <path d="M2 7h20"></path>
                    <path d="M2 17h20"></path>
                  </svg>
                  {{ item.dung_luong }}
                </span>
                <span v-if="item.mau_sac" class="item-spec color">
                  <span class="color-circle" :style="{ backgroundColor: item.mau_sac }"></span>
                  {{ item.mau_sac }}
                </span>
              </div>
            <div class="item-price">{{ formatPrice(item.san_pham?.gia) }}</div>
            <!-- Stock Warning -->
            <div style="margin-top: 6px; font-size: 11px; font-weight: 600;">
              <span v-if="(item.san_pham?.so_luong_kho !== undefined ? item.san_pham?.so_luong_kho : 100) <= 0" style="color: #FF3B30; background: rgba(255, 59, 48, 0.08); padding: 2px 6px; border-radius: 4px;">Hết hàng</span>
              <span v-else-if="(item.san_pham?.so_luong_kho !== undefined ? item.san_pham?.so_luong_kho : 100) < item.so_luong" style="color: #FF9500; background: rgba(255, 149, 0, 0.08); padding: 2px 6px; border-radius: 4px;">Không đủ tồn kho (Còn lại: {{ item.san_pham?.so_luong_kho }})</span>
              <span v-else style="color: #86868b;">Tồn kho: {{ item.san_pham?.so_luong_kho }}</span>
            </div>
          </div>
          <div class="item-quantity">
            <button class="qty-btn" @click="updateQuantity(item, -1)">−</button>
            <span class="qty-value">{{ item.so_luong }}</span>
            <button class="qty-btn" @click="updateQuantity(item, 1)">+</button>
          </div>
          <div class="item-total">
            <div class="total-price">{{ formatPrice((item.san_pham?.gia || 0) * item.so_luong) }}</div>
            <button class="remove-btn" @click="removeItem(item.id)">Xóa</button>
          </div>
        </div>
      </div>

      <div class="checkout-section">
        <div class="customer-info-form">
          <h2 class="section-title">Thông tin nhận hàng</h2>
          <div class="form-grid">
            <div class="form-group" :class="{ 'has-error': errors.name }">
              <label>Họ và tên</label>
              <input v-model="customerInfo.name" type="text" placeholder="Nhập họ tên người nhận" maxlength="100" />
              <span class="error-text" v-if="errors.name">{{ errors.name }}</span>
            </div>
            <div class="form-group">
              <label>Số điện thoại</label>
              <input 
                type="tel" 
                v-model="customerInfo.phone" 
                placeholder="Nhập số điện thoại" 
                maxlength="10"
                @input="customerInfo.phone = customerInfo.phone.replace(/\D/g, '').slice(0, 10)"
                :class="{ 'error': errors.phone }"
              >
              <span v-if="errors.phone" class="error-text">{{ errors.phone }}</span>
            </div>
            <div class="form-group full-width" :class="{ 'has-error': errors.address }">
              <label>Địa chỉ nhận hàng</label>
              <input v-model="customerInfo.address" type="text" placeholder="Số nhà, tên đường, phường/xã, quận/huyện..." maxlength="255" />
              <span class="error-text" v-if="errors.address">{{ errors.address }}</span>
            </div>
            <div class="form-group full-width">
              <label>Ghi chú (Tùy chọn)</label>
              <textarea v-model="customerInfo.note" rows="3" placeholder="Ghi chú về đơn hàng, thời gian giao hàng..."></textarea>
            </div>
          </div>
        </div>

        <!-- Voucher Section -->
        <div class="voucher-section">
          <h2 class="section-title">Mã giảm giá</h2>
          <div class="voucher-input-row">
            <input
              v-model="voucherCode"
              type="text"
              placeholder="Nhập mã giảm giá"
              class="voucher-input"
              :disabled="appliedVoucher !== null"
            />
            <button
              v-if="!appliedVoucher"
              class="apply-voucher-btn"
              :disabled="voucherLoading || !voucherCode.trim()"
              @click="handleApplyVoucher"
            >
              {{ voucherLoading ? 'Đang kiểm tra...' : 'Áp dụng' }}
            </button>
            <button
              v-else
              class="remove-voucher-btn"
              @click="handleRemoveVoucher"
            >
              Bỏ
            </button>
          </div>
          <div v-if="voucherError" class="voucher-error">{{ voucherError }}</div>
          <div v-if="appliedVoucher" class="voucher-applied">
            <span class="voucher-applied-text">
              Giảm {{ formatPrice(appliedVoucher.so_tien_giam) }}
            </span>
          </div>

          <!-- Danh sách voucher cho người dùng -->
          <div v-if="availableVouchers.length > 0" class="voucher-list">
            <div class="voucher-list-title">Mã giảm giá có sẵn</div>
            <div
              v-for="v in availableVouchers"
              :key="v.id"
              class="voucher-list-item"
              :class="{
                'voucher-paused': v.trang_thai === 'tam_dung' || v.trang_thai === 'het_han',
                'voucher-applied-item': appliedVoucher?.ma_voucher === v.ma_voucher
              }"
              @click="selectVoucherFromList(v)"
            >
              <div class="voucher-item-left">
                <div class="voucher-item-code">{{ v.ma_voucher }}</div>
                <div class="voucher-item-desc">
                  {{ v.loai_giam_gia === 'phan_tram' ? 'Giảm ' + v.gia_tri_giam + '%' : 'Giảm ' + formatPrice(v.gia_tri_giam) }}
                  <span v-if="v.giam_toi_da"> (tối đa {{ formatPrice(v.giam_toi_da) }})</span>
                  <span> · Đơn từ {{ formatPrice(v.don_hang_toi_thieu) }}</span>
                </div>
              </div>
              <div class="voucher-item-right">
                <span v-if="v.trang_thai === 'tam_dung'" class="voucher-status-badge paused">Tạm dừng</span>
                <span v-else-if="v.trang_thai === 'het_han'" class="voucher-status-badge expired">Hết hạn</span>
                <span v-else-if="appliedVoucher?.ma_voucher === v.ma_voucher" class="voucher-status-badge applied">Đã áp dụng</span>
                <button
                  v-else
                  class="apply-mini-btn"
                  @click.stop="quickApplyVoucher(v)"
                >Áp dụng</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Shipping Section -->
        <div class="shipping-section">
          <h2 class="section-title">Phương thức vận chuyển</h2>
          <div v-if="shippingMethods.length === 0" class="section-loading">
            <span>Đang tải phương thức vận chuyển...</span>
          </div>
          <div v-else class="shipping-options">
            <label
              v-for="method in shippingMethods"
              :key="method.ma_don_vi"
              class="shipping-option"
              :class="{ selected: selectedShipMethod === method.ma_don_vi }"
            >
              <input
                type="radio"
                name="shipping"
                :value="method.ma_don_vi"
                v-model="selectedShipMethod"
                @change="handleShipMethodChange(method.ma_don_vi)"
              />
              <div class="shipping-option-info">
                <span class="shipping-name">{{ method.ten_don_vi }}</span>
                <span class="shipping-desc" v-if="method.mo_ta">{{ method.mo_ta }}</span>
                <span class="shipping-time" v-if="method.thoi_gian_du_kien">⏱ {{ method.thoi_gian_du_kien }}</span>
              </div>
              <span class="shipping-fee">
                {{ formatPrice(method.phi_co_dinh) }}
                <span v-if="method.nguong_mien_phi > 0" class="free-ship-hint">
                  (Miễn phí từ {{ formatPrice(method.nguong_mien_phi) }})
                </span>
              </span>
            </label>
          </div>
        </div>

        <!-- Payment Section -->
        <div class="payment-section">
          <h2 class="section-title">Phương thức thanh toán</h2>
          <div v-if="paymentMethods.length === 0" class="section-loading">
            <span>Đang tải phương thức thanh toán...</span>
          </div>
          <div v-else class="payment-options">
            <label
              v-for="method in paymentMethods"
              :key="method.ma_phuong_thuc"
              class="payment-option"
              :class="{ selected: selectedPaymentMethod === method.ma_phuong_thuc }"
            >
              <input
                type="radio"
                name="payment"
                :value="method.ma_phuong_thuc"
                v-model="selectedPaymentMethod"
                @change="handlePaymentMethodChange(method.ma_phuong_thuc)"
              />
              <div class="payment-option-info">
                <span class="payment-name">{{ method.ten_doi_tac }}</span>
                <span class="payment-desc" v-if="method.mo_ta">{{ method.mo_ta }}</span>
              </div>
              <span class="payment-type-badge">{{ method.loai_hinh === 'online' ? 'Online' : 'COD' }}</span>
            </label>
          </div>
        </div>

        <div class="cart-summary">
          <h2 class="section-title">Tóm tắt thanh toán</h2>
          <div class="summary-row">
            <span>Tạm tính</span>
            <span class="summary-value">{{ formatPrice(cartTotal) }}</span>
          </div>
          <div class="summary-row" v-if="appliedVoucher">
            <span>Giảm giá</span>
            <span class="summary-value discount">-{{ formatPrice(appliedVoucher.so_tien_giam) }}</span>
          </div>
          <div class="summary-row">
            <span>Phí vận chuyển</span>
            <span class="summary-value" :class="phiShip > 0 ? '' : 'success'">
              {{ phiShip > 0 ? formatPrice(phiShip) : 'Miễn phí' }}
            </span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-row total">
            <span>Tổng cộng</span>
            <span class="summary-value total-value">{{ formatPrice(finalTotal) }}</span>
          </div>
          <button
            class="checkout-btn"
            :disabled="!canCheckout"
            @click="handleCheckout"
            :style="{ background: hasOutOfStockItems ? '#86868b' : '' }"
          >
            {{ checkoutLoading ? 'Đang xử lý...' : (hasOutOfStockItems ? 'Giỏ hàng có sản phẩm hết hàng' : 'Tiến hành thanh toán') }}
          </button>
          <p v-if="!isFormValid" class="form-hint">Vui lòng điền đủ thông tin để thanh toán</p>
          <p v-else-if="!selectedShipMethod" class="form-hint">Vui lòng chọn phương thức vận chuyển</p>
          <p v-else-if="!selectedPaymentMethod" class="form-hint">Vui lòng chọn phương thức thanh toán</p>
        </div>
      </div>
    </div>

    <!-- Guest UI: Chưa đăng nhập -->
    <div v-else-if="isGuest" class="empty-cart">
      <div class="empty-icon">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#86868b" stroke-width="1">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
      </div>
      <h1>Giỏ hàng của bạn</h1>
      <p>Vui lòng đăng nhập để xem giỏ hàng của bạn.</p>
      <router-link to="/login" class="continue-link">Đăng nhập ngay</router-link>
    </div>

    <div v-else class="empty-cart">
      <div class="empty-icon">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#86868b" stroke-width="1">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
      </div>
      <h1>Giỏ hàng của bạn</h1>
      <p>Giỏ hàng hiện tại đang trống.</p>
      <router-link to="/" class="continue-link">Tiếp tục mua sắm</router-link>
    </div>
    <!-- Transaction PIN Verification Modal (macOS Style) -->
    <div class="apple-modal-overlay" v-if="showCheckoutPinModal">
      <div class="apple-modal-card">
        <div class="modal-icon-container blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="modal-icon">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>
        <h3 class="modal-title">Xác thực mã PIN</h3>
        <p class="modal-desc">Vui lòng nhập mã PIN giao dịch của bạn để hoàn tất thanh toán.</p>
        
        <div class="modal-form">
          <div class="modal-input-group">
            <input 
              type="password" 
              v-model="checkoutPinValue" 
              placeholder="Nhập 4-6 chữ số mã PIN" 
              maxlength="6"
              style="text-align: center; font-size: 24px; letter-spacing: 6px;"
              class="modal-input-field"
              autofocus
            />
          </div>
        </div>

        <div class="modal-actions-row">
          <button class="modal-btn-secondary" @click="showCheckoutPinModal = false; checkoutPinValue = ''">Hủy bỏ</button>
          <button 
            class="modal-btn-primary" 
            @click="submitCheckoutPin" 
            :disabled="!checkoutPinValue"
          >
            Xác nhận
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { xacThucApi, gioHangApi, donHangApi, voucherApi, shippingApi, paymentApi } from '../services/api'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()

const router = useRouter()

const cartItems = ref([])
const selectedItems = ref([])
const token = ref(localStorage.getItem('access_token') || localStorage.getItem('token'))

const isGuest = computed(() => {
  return !token.value
})

const cartTotal = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + (item.san_pham?.gia || 0) * item.so_luong, 0)
})

// ---- Shipping, Payment, Voucher state ----
const shippingMethods = ref([])
const paymentMethods = ref([])
const selectedShipMethod = ref(null)
const selectedPaymentMethod = ref(null)
const phiShip = ref(0)
const appliedVoucher = ref(null)
const voucherCode = ref('')
const voucherLoading = ref(false)
const voucherError = ref(null)
const availableVouchers = ref([])
const checkoutLoading = ref(false)

const isAllSelected = computed(() => {
  return cartItems.value.length > 0 && selectedItems.value.length === cartItems.value.length
})

const toggleSelectAll = () => {
  if (isAllSelected.value) {
    selectedItems.value = []
  } else {
    selectedItems.value = cartItems.value.map(item => item.id)
  }
}

const customerInfo = ref({
  name: '',
  phone: '',
  address: '',
  note: ''
})

const errors = ref({
  name: '',
  phone: '',
  address: ''
})

const notification = ref({
  show: false,
  message: '',
  type: 'success'
})

const confirmModal = ref({
  show: false,
  title: '',
  message: '',
  onConfirm: null
})

const openConfirm = (title, message, callback) => {
  confirmModal.value = {
    show: true,
    title,
    message,
    onConfirm: callback
  }
}

const closeConfirm = () => {
  confirmModal.value.show = false
}

const handleConfirm = () => {
  if (confirmModal.value.onConfirm) {
    confirmModal.value.onConfirm()
  }
  closeConfirm()
}

const showToast = (msg, type = 'success') => {
  notification.value = { show: true, message: msg, type: type }
  setTimeout(() => { notification.value.show = false }, 4000)
}

const validateForm = () => {
  let isValid = true
  errors.value = { name: '', phone: '', address: '' }

  if (!customerInfo.value.name.trim()) {
    errors.value.name = 'Vui lòng nhập họ và tên'
    isValid = false
  } else if (customerInfo.value.name.trim().length < 2) {
    errors.value.name = 'Họ tên quá ngắn'
    isValid = false
  }

  if (!customerInfo.value.phone || !/^\d{10}$/.test(customerInfo.value.phone)) {
    errors.value.phone = "Số điện thoại phải đúng 10 chữ số."
    isValid = false
  }

  if (!customerInfo.value.address.trim()) {
    errors.value.address = 'Vui lòng nhập địa chỉ'
    isValid = false
  } else if (customerInfo.value.address.trim().length < 10) {
    errors.value.address = 'Địa chỉ cần chi tiết hơn (tối thiểu 10 ký tự)'
    isValid = false
  }

  return isValid
}

const isFormValid = computed(() => {
  return customerInfo.value.name.trim().length >= 2 &&
         customerInfo.value.phone.trim().length >= 10 &&
         customerInfo.value.address.trim().length >= 5
})

const hasOutOfStockItems = computed(() => {
  return cartItems.value.some(item => {
    const stock = item.san_pham?.so_luong_kho !== undefined ? item.san_pham.so_luong_kho : 100
    return stock < item.so_luong
  })
})

const canCheckout = computed(() => {
  return isFormValid.value && selectedShipMethod.value && selectedPaymentMethod.value && !hasOutOfStockItems.value
})

const finalTotal = computed(() => {
  const giamGia = appliedVoucher.value?.so_tien_giam || 0
  return cartTotal.value - giamGia + phiShip.value
})

// ---- Voucher Methods ----
const handleApplyVoucher = async () => {
  if (!voucherCode.value.trim()) return
  voucherLoading.value = true
  voucherError.value = null
  try {
    const res = await voucherApi.checkVoucher(voucherCode.value, cartTotal.value)
    if (res.data.hop_le) {
      appliedVoucher.value = {
        ma_voucher: res.data.ma_voucher,
        so_tien_giam: res.data.so_tien_giam,
        loai_giam_gia: res.data.loai_giam_gia,
        gia_tri_giam: res.data.gia_tri_giam,
        giam_toi_da: res.data.giam_toi_da
      }
      voucherError.value = null
    } else {
      appliedVoucher.value = null
      voucherError.value = res.data.loi || 'Mã giảm giá không hợp lệ'
    }
  } catch (error) {
    appliedVoucher.value = null
    voucherError.value = 'Lỗi khi kiểm tra mã giảm giá'
    console.error("Lỗi voucher:", error)
  } finally {
    voucherLoading.value = false
  }
}

const handleRemoveVoucher = () => {
  appliedVoucher.value = null
  voucherCode.value = ''
  voucherError.value = null
}

const fetchAvailableVouchers = async () => {
  try {
    const res = await voucherApi.getUserVouchers()
    availableVouchers.value = res.data || []
  } catch (error) {
    console.error("Lỗi tải danh sách voucher:", error)
  }
}

const selectVoucherFromList = (v) => {
  // If paused, do nothing
  if (v.trang_thai === 'tam_dung') return
  // If already applied, remove it
  if (appliedVoucher.value?.ma_voucher === v.ma_voucher) {
    handleRemoveVoucher()
    return
  }
  // Auto-fill code and apply
  voucherCode.value = v.ma_voucher
  handleApplyVoucher()
}

const quickApplyVoucher = (v) => {
  if (v.trang_thai === 'tam_dung') return
  voucherCode.value = v.ma_voucher
  handleApplyVoucher()
}

// ---- Shipping Methods ----
const handleShipMethodChange = async (maDonVi) => {
  try {
    const res = await shippingApi.tinhPhiShip(maDonVi, cartTotal.value)
    phiShip.value = res.data.phi_ship
  } catch (error) {
    console.error("Lỗi tính phí ship:", error)
    phiShip.value = 0
  }
}

// ---- Payment Methods ----
const handlePaymentMethodChange = (maPhuongThuc) => {
  // Nothing extra needed for now
}

// ---- Checkout ----
const showCheckoutPinModal = ref(false)
const checkoutPinValue = ref('')

const submitCheckoutPin = () => {
  if (!checkoutPinValue.value) {
    showToast('Vui lòng nhập mã PIN!', 'error')
    return
  }
  handleCheckout()
}

const handleCheckout = async () => {
  if (!validateForm()) {
    showToast('Thông tin không hợp lệ, vui lòng kiểm tra lại!', 'error')
    return
  }
  if (!selectedShipMethod.value) {
    showToast('Vui lòng chọn phương thức vận chuyển!', 'error')
    return
  }
  if (!selectedPaymentMethod.value) {
    showToast('Vui lòng chọn phương thức thanh toán!', 'error')
    return
  }
  
  const userProfile = JSON.parse(localStorage.getItem('user_profile') || '{}')
  if (userProfile.vai_tro !== 'doanh_nghiep' && userProfile.vai_tro !== 'admin') {
    const totalCartQty = cartItems.value.reduce((sum, item) => sum + item.so_luong, 0)
    if (totalCartQty > 10) {
      showToast('Tài khoản Cá nhân giới hạn đặt mua tối đa 10 sản phẩm mỗi ngày. Vui lòng đăng ký tài khoản Doanh nghiệp trong trang Hồ sơ cá nhân để mua số lượng lớn!', 'error')
      return
    }
  }
  
  if (userProfile.yeu_cau_pin && !checkoutPinValue.value) {
    checkoutPinValue.value = ''
    showCheckoutPinModal.value = true
    return
  }
  
  checkoutLoading.value = true
  try {
    const orderPayload = {
      ten_khach_hang: customerInfo.value.name,
      so_dien_thoai: customerInfo.value.phone,
      dia_chi: customerInfo.value.address,
      ghi_chu: customerInfo.value.note,
      tong_tien: Number(finalTotal.value),
      phuong_thuc_thanh_toan: selectedPaymentMethod.value,
      phuong_thuc_van_chuyen: selectedShipMethod.value,
      ma_voucher: appliedVoucher.value?.ma_voucher || null,
      ma_pin: checkoutPinValue.value || null,
      items: cartItems.value.map(item => ({
        san_pham_id: Number(item.san_pham?.id),
        so_luong: Number(item.so_luong),
        gia: Number(item.san_pham?.gia || 0),
        dung_luong: item.dung_luong || "",
        ram: item.ram || "",
        mau_sac: item.mau_sac || ""
      }))
    }

    const response = await donHangApi.taoDonHang(orderPayload)

    if (response.status === 200 || response.status === 201) {
      showToast(`Cảm ơn ${customerInfo.value.name} đã đặt hàng thành công!`, 'success')
      cartItems.value = []
      selectedShipMethod.value = null
      selectedPaymentMethod.value = null
      phiShip.value = 0
      appliedVoucher.value = null
      voucherCode.value = ''
      checkoutPinValue.value = ''
      showCheckoutPinModal.value = false
      cartStore.fetchCart()
      setTimeout(() => router.push('/'), 2000)
    }
  } catch (error) {
    console.error("Lỗi thanh toán:", error)
    const errorMsg = error.response?.data?.detail || "Đã có lỗi xảy ra, vui lòng thử lại sau."
    showToast("Lỗi đặt hàng: " + errorMsg, 'error')
    checkoutPinValue.value = ''
  } finally {
    checkoutLoading.value = false
  }
}

const fetchCart = async () => {
  try {
    if (!token.value || token.value === 'null' || token.value === 'undefined') {
      console.warn("No valid token found in localStorage, skipping cart fetch");
      return
    }

    const res = await gioHangApi.getCart()
    cartItems.value = res.data
  } catch (e) {
    console.error("Lỗi tải giỏ hàng:", e)
  }
}

const updateQuantity = async (item, delta) => {
  const newQty = item.so_luong + delta
  if (newQty < 1) return

  try {
    const res = await gioHangApi.updateQuantity(item.id, { so_luong: newQty })
    if (res.status === 200) {
      item.so_luong = newQty
      cartStore.fetchCart() // Cập nhật lại Navbar
    }
  } catch (e) {
    console.error("Lỗi cập nhật số lượng:", e)
  }
}

const removeItem = (itemId) => {
  openConfirm(
    'Xóa sản phẩm',
    'Bạn có chắc chắn muốn xóa sản phẩm này khỏi giỏ hàng?',
    async () => {
      try {
        const res = await gioHangApi.removeItem(itemId)
        if (res.status === 200) {
          cartItems.value = cartItems.value.filter(i => i.id !== itemId)
          selectedItems.value = selectedItems.value.filter(id => id !== itemId)
          cartStore.fetchCart()
          showToast('Đã xóa sản phẩm khỏi giỏ hàng', 'success')
        }
      } catch (e) {
        console.error("Lỗi xóa sản phẩm:", e)
        showToast('Không thể xóa sản phẩm. Vui lòng thử lại.', 'error')
      }
    }
  )
}

const removeSelectedItems = () => {
  if (selectedItems.value.length === 0) return
  
  openConfirm(
    'Xóa nhiều sản phẩm',
    `Bạn có chắc chắn muốn xóa ${selectedItems.value.length} sản phẩm đã chọn?`,
    async () => {
      let successCount = 0
      let failCount = 0

      for (const itemId of [...selectedItems.value]) {
        try {
          const res = await gioHangApi.removeItem(itemId)
          if (res.status === 200) {
            cartItems.value = cartItems.value.filter(i => i.id !== itemId)
            selectedItems.value = selectedItems.value.filter(id => id !== itemId)
            successCount++
          }
        } catch (e) {
          console.error(`Lỗi xóa sản phẩm ${itemId}:`, e)
          failCount++
        }
      }

      cartStore.fetchCart()
      
      if (successCount > 0) {
        showToast(`Đã xóa thành công ${successCount} sản phẩm`, 'success')
      }
      if (failCount > 0) {
        showToast(`Có ${failCount} sản phẩm không thể xóa`, 'error')
      }
    }
  )
}

const formatPrice = (p) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

onMounted(async () => {
  fetchCart()
  
  // Tải danh sách phương thức vận chuyển và thanh toán
  fetchShippingMethods()
  fetchPaymentMethods()

  // Tải danh sách voucher cho người dùng
  fetchAvailableVouchers()
  
  // Tự động điền thông tin từ hồ sơ tài khoản
  try {
    if (token.value && token.value !== 'null' && token.value !== 'undefined') {
      const res = await xacThucApi.getMe()
      const profile = res.data
      if (profile.ho_ten) customerInfo.value.name = profile.ho_ten
      if (profile.so_dien_thoai) customerInfo.value.phone = profile.so_dien_thoai
      if (profile.dia_chi) customerInfo.value.address = profile.dia_chi
      
      // Cập nhật lại cache local
      localStorage.setItem('user_profile', JSON.stringify(profile))
    }
  } catch (e) {
    console.error("Không thể lấy thông tin hồ sơ:", e)
    // Fallback về localStorage nếu API lỗi (trừ 401 đã redirect)
    if (e.response && e.response.status !== 401) {
      const savedProfile = localStorage.getItem('user_profile')
      if (savedProfile) {
        const profile = JSON.parse(savedProfile)
        if (profile.ho_ten) customerInfo.value.name = profile.ho_ten
        if (profile.so_dien_thoai) customerInfo.value.phone = profile.so_dien_thoai
        if (profile.dia_chi) customerInfo.value.address = profile.dia_chi
      }
    }
  }
})

const fetchShippingMethods = async () => {
  try {
    const res = await shippingApi.getDonVi()
    shippingMethods.value = res.data
  } catch (error) {
    console.error("Lỗi tải phương thức vận chuyển:", error)
  }
}

const fetchPaymentMethods = async () => {
  try {
    const res = await paymentApi.getDoiTac()
    paymentMethods.value = res.data
  } catch (error) {
    console.error("Lỗi tải phương thức thanh toán:", error)
  }
}
</script>

<style scoped>
/* Confirm Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.confirm-modal {
  background: white;
  width: 100%;
  max-width: 320px;
  border-radius: 20px;
  padding: 30px 24px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  animation: modalScale 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modalScale {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.confirm-icon {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.confirm-modal h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 12px;
}

.confirm-modal p {
  font-size: 14px;
  color: #86868b;
  line-height: 1.5;
  margin-bottom: 24px;
}

.modal-actions {
  display: flex;
  gap: 12px;
}

.modal-btn {
  flex: 1;
  padding: 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-btn.cancel {
  background: #f5f5f7;
  color: #1d1d1f;
  border: none;
}

.modal-btn.cancel:hover {
  background: #e8e8ed;
}

.modal-btn.confirm {
  background: #ff3b30;
  color: white;
  border: none;
}

.modal-btn.confirm:hover {
  background: #e03126;
  box-shadow: 0 4px 12px rgba(255, 59, 48, 0.3);
}

/* Animations */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.cart-page {
  padding: 120px 20px 100px;
  background: #ffffff;
  min-height: 80vh;
  position: relative;
}

/* Toast Styles */
.toast-notification {
  position: fixed;
  top: 100px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  padding: 12px 24px;
  border-radius: 40px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  pointer-events: none;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toast-icon-circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.toast-notification.success .toast-icon-circle {
  background: #28c840;
  color: white;
}

.toast-notification.error .toast-icon-circle {
  background: #ff3b30;
  color: white;
}

.toast-message {
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translate(-50%, -40px);
}

.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -40px);
}

/* Form Error Styles */
.form-group.has-error input {
  border-color: #ff3b30;
  background: #fffbfa;
}

.form-group.has-error input:focus {
  box-shadow: 0 0 0 4px rgba(255, 59, 48, 0.1);
}

.error-text {
  font-size: 11px;
  color: #ff3b30;
  font-weight: 500;
  margin-top: 2px;
}

.cart-container {
  max-width: 1000px;
  margin: 0 auto;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.cart-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0;
}

.cart-count {
  font-size: 14px;
  color: #86868b;
  font-weight: 500;
}

/* Custom Checkbox Styles */
.custom-checkbox {
  position: relative;
  display: inline-block;
  width: 22px;
  height: 22px;
}

.custom-checkbox input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 22px;
  width: 22px;
  background-color: #ffffff;
  border: 2px solid #d2d2d7;
  border-radius: 7px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.custom-checkbox:hover .checkmark {
  border-color: #007aff;
  background-color: #f5f5f7;
}

.custom-checkbox input:checked ~ .checkmark {
  background-color: #007aff;
  border-color: #007aff;
  box-shadow: 0 4px 10px rgba(0, 122, 255, 0.3);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.custom-checkbox input:checked ~ .checkmark:after {
  display: block;
}

.custom-checkbox .checkmark:after {
  left: 7px;
  top: 3px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2.5px 2.5px 0;
  transform: rotate(45deg);
}

.select-all {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  padding: 8px 16px;
  border-radius: 12px;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.select-all:hover {
  background: #f5f5f7;
  border-color: #e5e5ea;
}

.cart-items {
  display: flex;
  flex-direction: column;
  max-height: 300px; 
  overflow-y: auto;
  padding-right: 15px; 
  gap: 0;
}

.cart-items::-webkit-scrollbar {
  width: 5px;
}

.cart-items::-webkit-scrollbar-track {
  background: transparent;
}

.cart-items::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.08);
  border-radius: 10px;
}

.cart-items:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 24px 0;
  border-bottom: 1px solid #f2f2f2;
  gap: 20px;
  flex-shrink: 0;
}

.cart-item:hover {
  border-color: #d2d2d7;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
  flex-shrink: 0;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 16px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 8px 0;
}

.item-specs {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.item-spec {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  background: #f5f5f7;
  border-radius: 6px;
  color: #1d1d1f;
  border: 1px solid #e5e5e5;
  transition: all 0.2s;
}

.item-spec.capacity {
  background: #f2f2f7;
  color: #007aff;
  border-color: rgba(0, 122, 255, 0.2);
}

.item-spec.ram {
  background: #fff9db;
  color: #f08c00;
  border-color: rgba(240, 140, 0, 0.2);
}

.item-spec.color {
  background: #ffffff;
  color: #1d1d1f;
}

.color-circle {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  border: 1px solid #d2d2d7;
}

.item-price {
  font-size: 14px;
  color: #86868b;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #ffffff;
  padding: 6px 12px;
  border-radius: 10px;
  border: 1px solid #e5e5ea;
}

.qty-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: #f5f5f7;
  color: #1d1d1f;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.qty-btn:hover {
  background: #e8e8ed;
}

.qty-value {
  font-size: 16px;
  font-weight: 600;
  min-width: 24px;
  text-align: center;
}

.item-total {
  text-align: right;
  min-width: 120px;
}

.total-price {
  font-size: 18px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 4px;
}

.remove-btn {
  background: none;
  border: none;
  color: #ff3b30;
  font-size: 13px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: rgba(255, 59, 48, 0.1);
}

.remove-selected-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border-radius: 40px;
  background: #ff3b30;
  color: white;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(255, 59, 48, 0.2);
}

.remove-selected-btn:hover {
  background: #e03126;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(255, 59, 48, 0.3);
}

.remove-selected-btn:active {
  transform: translateY(0);
}

/* Checkout Section Layout */
.checkout-section {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 32px;
  margin-top: 48px;
  align-items: stretch; /* Để các cột có độ dài bằng nhau */
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 24px;
}

/* Customer Form */
.customer-info-form {
  background: #ffffff;
  padding: 32px;
  border-radius: 20px;
  border: 1px solid #e5e5ea;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
}

.form-group input, 
.form-group textarea {
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #d2d2d7;
  font-family: inherit;
  font-size: 15px;
  transition: all 0.2s;
  background: #fbfbfd;
}

.form-group input:focus, 
.form-group textarea:focus {
  border-color: #007aff;
  background: #ffffff;
  outline: none;
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
}

/* Summary */
.cart-summary {
  padding: 32px;
  background: #fbfbfd;
  border-radius: 20px;
  border: 1px solid #e5e5ea;
  display: flex;
  flex-direction: column;
}

.form-hint {
  font-size: 12px;
  color: #ff3b30;
  margin-top: 12px;
  text-align: center;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  color: #86868b;
}

.summary-value {
  font-weight: 600;
  color: #1d1d1f;
}

.summary-value.success {
  color: #28c840;
}

.summary-divider {
  height: 1px;
  background: #e5e5ea;
  margin: 16px 0;
}

.summary-row.total {
  margin-bottom: 24px;
}

.summary-row.total .summary-value {
  font-size: 20px;
  font-weight: 700;
}

.checkout-btn {
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  background: #007aff;
  color: white;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: auto; /* Đẩy nút xuống dưới cùng của khung */
}

.checkout-btn:hover {
  background: #0062cc;
  transform: translateY(-1px);
}

/* Empty Cart */
.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 70vh; /* Tăng chiều cao để căn giữa theo chiều dọc */
  padding: 40px 20px;
}

.empty-icon {
  margin-bottom: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: none !important;
  border: none !important;
  box-shadow: none !important;
}

.empty-cart h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 12px 0;
}

.empty-cart p {
  font-size: 16px;
  color: #86868b;
  margin: 0 0 24px 0;
}

.continue-link {
  display: inline-block;
  padding: 12px 32px;
  background: #007aff;
  color: white;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}

.continue-link:hover {
  background: #0062cc;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .cart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 30px;
  }

  .header-actions {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }

  .select-all {
    padding: 8px 12px;
    background: #f5f5f7;
  }

  .remove-selected-btn {
    padding: 8px 14px;
    font-size: 12px;
  }

  .cart-item {
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .item-info {
    flex: 1 1 calc(100% - 100px);
  }
  
  .item-quantity {
    order: 1;
  }
  
  .item-total {
    order: 2;
    margin-left: auto;
  }
  
  .checkout-section {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .cart-summary {
    position: static;
  }
}

/* ===== Voucher Section ===== */
.voucher-section {
  padding: 24px 32px;
  background: #fbfbfd;
  border-radius: 20px;
  border: 1px solid #e5e5ea;
}

.voucher-input-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.voucher-input {
  flex: 1;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #d2d2d7;
  font-family: inherit;
  font-size: 15px;
  background: white;
  transition: all 0.2s;
}

.voucher-input:focus {
  border-color: #007aff;
  outline: none;
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
}

.voucher-input:disabled {
  background: #f5f5f7;
  color: #86868b;
}

.apply-voucher-btn {
  padding: 12px 24px;
  border-radius: 12px;
  background: #007aff;
  color: white;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.apply-voucher-btn:hover:not(:disabled) {
  background: #0062cc;
}

.apply-voucher-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.remove-voucher-btn {
  padding: 12px 24px;
  border-radius: 12px;
  background: #ff3b30;
  color: white;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.remove-voucher-btn:hover {
  background: #e03126;
}

.voucher-error {
  margin-top: 10px;
  font-size: 13px;
  color: #ff3b30;
}

.voucher-applied {
  margin-top: 10px;
  padding: 10px 16px;
  background: #ebfbee;
  border-radius: 10px;
  border: 1px solid #d3f9d8;
}

.voucher-applied-text {
  font-size: 14px;
  font-weight: 600;
  color: #2b8a3e;
}

/* ===== Available Vouchers List ===== */
.voucher-list {
  margin-top: 16px;
  border-top: 1px solid #e5e5ea;
  padding-top: 16px;
}

.voucher-list-title {
  font-size: 13px;
  font-weight: 600;
  color: #86868b;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.voucher-list-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #e5e5ea;
  background: white;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.voucher-list-item:hover {
  border-color: #007aff;
  background: #f0f7ff;
}

.voucher-list-item.voucher-applied-item {
  border-color: #28c840;
  background: #ebfbee;
  cursor: default;
}

.voucher-list-item.voucher-paused {
  opacity: 0.55;
  filter: grayscale(1);
  cursor: not-allowed;
  pointer-events: none;
}

.voucher-item-left {
  flex: 1;
  min-width: 0;
}

.voucher-item-code {
  font-size: 14px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 4px;
  letter-spacing: 0.3px;
}

.voucher-item-desc {
  font-size: 12px;
  color: #86868b;
  line-height: 1.4;
}

.voucher-item-right {
  flex-shrink: 0;
  margin-left: 12px;
  display: flex;
  align-items: center;
}

.voucher-status-badge {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  white-space: nowrap;
}

.voucher-status-badge.paused {
  background: #fff4e6;
  color: #d9480f;
  border: 1px solid #ffe8cc;
}

.voucher-status-badge.applied {
  background: #ebfbee;
  color: #2b8a3e;
  border: 1px solid #d3f9d8;
}

.voucher-status-badge.expired {
  background: #fff5f5;
  color: #c92a2a;
  border: 1px solid #ffe3e3;
}

.apply-mini-btn {
  padding: 6px 14px;
  border-radius: 8px;
  background: #007aff;
  color: white;
  border: none;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.apply-mini-btn:hover {
  background: #0062cc;
  transform: translateY(-1px);
}

/* ===== Shipping & Payment Sections ===== */
.shipping-section,
.payment-section {
  padding: 24px 32px;
  background: #fbfbfd;
  border-radius: 20px;
  border: 1px solid #e5e5ea;
}

.section-loading {
  padding: 20px;
  text-align: center;
  color: #86868b;
  font-size: 14px;
}

.shipping-options,
.payment-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.shipping-option,
.payment-option {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 14px;
  border: 1.5px solid #e5e5ea;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.shipping-option:hover,
.payment-option:hover {
  border-color: #007aff;
  background: #f0f7ff;
}

.shipping-option.selected,
.payment-option.selected {
  border-color: #007aff;
  background: #f0f7ff;
}

.shipping-option input[type="radio"],
.payment-option input[type="radio"] {
  accent-color: #007aff;
  width: 18px;
  height: 18px;
}

.shipping-option-info,
.payment-option-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.shipping-name,
.payment-name {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
}

.shipping-desc,
.payment-desc {
  font-size: 12px;
  color: #86868b;
}

.shipping-time {
  font-size: 12px;
  color: #007aff;
  font-weight: 500;
}

.shipping-fee {
  font-size: 15px;
  font-weight: 700;
  color: #1d1d1f;
  text-align: right;
}

.free-ship-hint {
  display: block;
  font-size: 11px;
  font-weight: 400;
  color: #28c840;
}

.payment-type-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  background: #f0f0f5;
  color: #86868b;
  white-space: nowrap;
}

/* Discount in summary */
.summary-value.discount {
  color: #2b8a3e;
}

/* ===== Checkout section layout ===== */
.checkout-section {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 24px;
  margin-top: 24px;
  align-items: start;
}

.customer-info-form,
.voucher-section,
.shipping-section,
.payment-section,
.cart-summary {
  margin-bottom: 0;
}

/* Stack voucher/shipping/payment vertically in left column */
.checkout-section > .customer-info-form,
.checkout-section > .voucher-section,
.checkout-section > .shipping-section,
.checkout-section > .payment-section {
  grid-column: 1;
}

.checkout-section > .cart-summary {
  grid-column: 2;
  grid-row: 1 / 5;
  position: sticky;
  top: 100px;
}

@media (max-width: 900px) {
  .checkout-section {
    grid-template-columns: 1fr;
  }
  .checkout-section > .cart-summary {
    grid-column: 1;
    grid-row: auto;
    position: static;
  }
}

/* Apple/macOS Alert Modals */
.apple-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.25s ease-out;
}

.apple-modal-card {
  background: #ffffff;
  border-radius: 24px;
  width: 90%;
  max-width: 400px;
  padding: 30px 24px 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  animation: scaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-icon-container {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.modal-icon-container.blue {
  background: #f0f7ff;
  border: 2px solid #007aff;
  color: #007aff;
}

.modal-icon {
  width: 28px;
  height: 28px;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 10px 0;
}

.modal-desc {
  font-size: 14px;
  color: #86868b;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.modal-form {
  width: 100%;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-input-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  gap: 6px;
}

.modal-input-field {
  width: 100%;
  background: #f5f5f7;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 16px;
  color: #1d1d1f;
  outline: none;
  transition: all 0.2s;
  box-sizing: border-box;
}

.modal-input-field:focus {
  border-color: #007aff;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.15);
}

.modal-actions-row {
  display: flex;
  gap: 12px;
  width: 100%;
  margin-top: 8px;
}

.modal-btn-secondary {
  flex: 1;
  background: #f5f5f7;
  color: #1d1d1f;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  padding: 12px 20px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-btn-secondary:hover {
  background: #e8e8ed;
}

.modal-btn-primary {
  flex: 1;
  background: #007aff;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  padding: 12px 20px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-btn-primary:hover {
  background: #0066cc;
}

.modal-btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleUp {
  from { transform: scale(0.85); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>
