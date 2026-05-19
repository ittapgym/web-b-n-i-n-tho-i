<template>
  <div class="orders-page">
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

    <!-- Custom Confirm Modal -->
    <transition name="modal">
      <div v-if="confirmModal.show" class="confirm-overlay" @click.self="closeConfirm(false)">
        <div class="confirm-modal">
          <div class="confirm-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#ff3b30" stroke-width="1.5">
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/>
            </svg>
          </div>
          <h3>Xác nhận xóa</h3>
          <p>{{ confirmModal.message }}</p>
          <div class="confirm-buttons">
            <button class="btn-cancel" @click="closeConfirm(false)">Hủy</button>
            <button class="btn-confirm" @click="closeConfirm(true)">Xác nhận</button>
          </div>
        </div>
      </div>
    </transition>
    <div class="orders-container">
      <header class="page-header">
        <h1>Đơn hàng của tôi</h1>
        <p class="subtitle">Theo dõi lộ trình và trạng thái đơn hàng của bạn</p>
      </header>

      <div v-if="orders.length > 0" class="order-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <div class="order-id">
              <span class="label">Mã đơn hàng</span>
              <span class="value">#{{ order.id }}</span>
              <div v-if="order.imei" class="order-imei-row" style="margin-top: 8px; font-size: 12px; color: #86868b; display: flex; align-items: center; gap: 6px;">
                <span class="imei-tag" style="background: rgba(0, 113, 227, 0.08); color: #0071e3; font-weight: 700; padding: 2px 6px; border-radius: 6px; font-family: monospace; letter-spacing: 0.5px;">
                  IMEI: {{ order.imei }}
                </span>
                <span class="warranty-tag" style="font-weight: 500;">
                  (Bảo hành: {{ order.warranty_months }} tháng)
                </span>
              </div>
            </div>
            <div class="order-status-pill" :class="getStatusClass(order.trang_thai)">
              {{ getStatusText(order.trang_thai) }}
            </div>
          </div>

          <div class="order-body">
            <!-- Timeline -->
            <div class="order-timeline">
              <div class="timeline-step" :class="{ active: isStepActive(order.trang_thai, 'cho_duyet') }">
                <div class="step-dot"></div>
                <div class="step-label">Chờ duyệt</div>
              </div>
              <div class="timeline-line"></div>
              <div class="timeline-step" :class="{ active: isStepActive(order.trang_thai, 'da_duyet') }">
                <div class="step-dot"></div>
                <div class="step-label">Đã duyệt</div>
              </div>
              <div class="timeline-line"></div>
              <div class="timeline-step" :class="{ active: isStepActive(order.trang_thai, 'dang_giao') }">
                <div class="step-dot"></div>
                <div class="step-label">Đang giao</div>
              </div>
              <div class="timeline-line"></div>
              <div class="timeline-step" :class="{ active: isStepActive(order.trang_thai, 'hoan_thanh') }">
                <div class="step-dot"></div>
                <div class="step-label">Hoàn thành</div>
              </div>
            </div>

            <div class="order-items-summary">
              <div v-for="item in order.items" :key="item.id" class="order-item-brief">
                <div class="item-details">
                  <span class="item-name">{{ item.san_pham?.ten || 'Sản phẩm' }}</span>
                  <span class="item-variant-info" v-if="item.dung_luong || item.ram">
                    ({{ item.ram ? 'RAM ' + item.ram : '' }}{{ item.dung_luong && item.ram ? ' - ' : '' }}{{ item.dung_luong }})
                  </span>
                </div>
                <span class="item-qty">x{{ item.so_luong }}</span>
              </div>
            </div>
          </div>

          <div class="order-footer">
            <div class="order-actions">
              <div class="order-date">{{ formatDate(order.ngay_tao) }}</div>
              <button class="delete-order-btn" @click="handleDeleteOrder(order.id)">Xóa đơn hàng</button>
            </div>
            <div class="order-total">
              <span class="label">Tổng thanh toán:</span>
              <span class="amount">{{ formatPrice(order.tong_tien) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Guest UI: Chưa đăng nhập -->
      <div v-else-if="isGuest" class="empty-orders">
        <div class="empty-icon">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#86868b" stroke-width="1">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
        </div>
        <h2>Đơn hàng của tôi</h2>
        <p>Vui lòng đăng nhập để xem lịch sử đơn hàng của bạn.</p>
        <router-link to="/login" class="shop-now-btn">Đăng nhập ngay</router-link>
      </div>

      <div v-else class="empty-orders">
        <div class="empty-icon">📦</div>
        <h2>Chưa có đơn hàng nào</h2>
        <p>Bạn chưa thực hiện đơn đặt hàng nào trong hệ thống.</p>
        <router-link to="/" class="shop-now-btn">Mua sắm ngay</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

/**
 * Danh sách các đơn hàng thuộc người dùng hiện tại.
 */
const orders = ref([])

/**
 * Kiểm tra xem người dùng hiện tại có phải là khách vãng lai (chưa đăng nhập) hay không.
 */
const isGuest = computed(() => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  return !token
})

/**
 * Trạng thái hiển thị và thông tin của custom Toast notification.
 */
const notification = ref({
  show: false,
  message: '',
  type: 'success'
})

/**
 * Cấu hình của Modal xác nhận hành động xóa/ẩn đơn hàng.
 */
const confirmModal = ref({
  show: false,
  message: '',
  onConfirm: null
})

/**
 * Hiển thị Toast thông báo trên màn hình.
 * @param {string} msg - Nội dung thông báo.
 * @param {string} [type='success'] - Phân loại thông báo (success, error, info).
 */
const showToast = (msg, type = 'success') => {
  notification.value = { show: true, message: msg, type: type }
  setTimeout(() => { notification.value.show = false }, 3000)
}

/**
 * Kích hoạt hiển thị Modal xác nhận hành động của người dùng.
 * @param {string} msg - Thông điệp hiển thị trên Modal.
 * @param {Function} callback - Hàm thực thi sau khi bấm xác nhận.
 */
const triggerConfirm = (msg, callback) => {
  confirmModal.value = {
    show: true,
    message: msg,
    onConfirm: callback
  }
}

/**
 * Đóng Modal xác nhận và quyết định có thực thi hành động hay không.
 * @param {boolean} result - Kết quả phản hồi của người dùng (True: Đồng ý, False: Hủy).
 */
const closeConfirm = (result) => {
  if (result && confirmModal.value.onConfirm) {
    confirmModal.value.onConfirm()
  }
  confirmModal.value.show = false
}

/**
 * Tải danh sách đơn hàng trực tuyến của tài khoản hiện tại từ API.
 */
const fetchOrders = async () => {
  try {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token')
    if (!token) {
      console.warn("User not logged in, skipping order fetch");
      return
    }
    const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}/don-hang/user/my-orders`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) {
      orders.value = await res.json()
    }
  } catch (e) {
    console.error("Lỗi tải đơn hàng:", e)
  }
}

/**
 * Gửi yêu cầu ẩn đơn hàng chỉ định khỏi giao diện lịch sử mua sắm của User.
 * @param {number} orderId - ID đơn hàng cần ẩn.
 */
const handleDeleteOrder = (orderId) => {
  triggerConfirm("Bạn có chắc chắn muốn ẩn đơn hàng này khỏi lịch sử của mình?", async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token')
      const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}/don-hang/xoa/${orderId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (res.ok) {
        showToast("Đã ẩn đơn hàng thành công.", "success")
        orders.value = orders.value.filter(o => o.id !== orderId)
      } else {
        const err = await res.json()
        showToast("Lỗi: " + (err.detail || "Không rõ nguyên nhân"), "error")
      }
    } catch (e) {
      console.error("Lỗi xóa đơn hàng:", e)
      showToast("Đã có lỗi xảy ra.", "error")
    }
  })
}

/**
 * Lấy nhãn tiếng Việt tương ứng cho mã trạng thái đơn hàng.
 * @param {string} status - Mã trạng thái của đơn hàng từ backend.
 * @returns {string} Chuỗi hiển thị thân thiện với người dùng.
 */
const getStatusText = (status) => {
  const map = {
    'cho_duyet': '⏳ Chờ xác nhận',
    'da_duyet': '✅ Đã xác nhận',
    'dang_giao': '🚚 Đang giao hàng',
    'hoan_thanh': '🏁 Giao thành công',
    'da_huy': '❌ Đã hủy'
  }
  return map[status] || status
}

/**
 * Lấy tên CSS class tương thích với trạng thái đơn hàng phục vụ đổi màu sắc giao diện.
 * @param {string} status - Trạng thái đơn hàng.
 * @returns {string} Tên class CSS tương ứng.
 */
const getStatusClass = (status) => {
  return `status-${status}`
}

/**
 * Kiểm tra xem bước trạng thái hiện tại trong thanh tiến trình (timeline) có đang hoạt động hay không.
 * @param {string} currentStatus - Trạng thái hiện tại thực tế của đơn hàng.
 * @param {string} step - Bước trạng thái trên dòng thời gian đang xét.
 * @returns {boolean} True nếu bước đó đã hoặc đang diễn ra, ngược lại là False.
 */
const isStepActive = (currentStatus, step) => {
  const levels = { 'cho_duyet': 1, 'da_duyet': 2, 'dang_giao': 3, 'hoan_thanh': 4, 'da_huy': 0 }
  return levels[currentStatus] >= levels[step]
}

/**
 * Định dạng giá trị số thành chuỗi tiền tệ VND.
 * @param {number} p - Số tiền cần định dạng.
 * @returns {string} Chuỗi tiền tệ đã định dạng.
 */
const formatPrice = (p) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

/**
 * Định dạng chuỗi ngày giờ hệ thống sang chuỗi ngày giờ định dạng địa phương Việt Nam.
 * @param {string} dateStr - Chuỗi thời gian.
 * @returns {string} Giao diện ngày giờ địa phương.
 */
const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('vi-VN')
}

onMounted(fetchOrders)
</script>

<style scoped>
.orders-page {
  padding: 80px 20px 100px;
  background-color: #f5f5f7;
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
  padding: 12px 24px;
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
.toast-icon-circle { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.toast-notification.success .toast-icon-circle { background: #28c840; color: white; }
.toast-notification.error .toast-icon-circle { background: #ff3b30; color: white; }
.toast-message { font-size: 14px; font-weight: 600; color: #1d1d1f; }

.toast-enter-active, .toast-leave-active { transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1); }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translate(-50%, -40px); }

/* Confirm Modal Styles */
.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.confirm-modal {
  background: rgba(255, 255, 255, 0.95);
  width: 90%;
  max-width: 320px;
  border-radius: 24px;
  padding: 32px 24px 24px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.confirm-icon { margin-bottom: 20px; }

.confirm-modal h3 {
  font-size: 19px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 12px 0;
}

.confirm-modal p {
  font-size: 14px;
  color: #86868b;
  margin: 0 0 28px 0;
  line-height: 1.4;
}

.confirm-buttons {
  display: flex;
  gap: 12px;
}

.confirm-buttons button {
  flex: 1;
  padding: 12px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-cancel {
  background: #f5f5f7;
  color: #1d1d1f;
}

.btn-confirm {
  background: #ff3b30;
  color: white;
}

.btn-cancel:hover { background: #e8e8ed; }
.btn-confirm:hover { background: #d70015; }

.modal-enter-active, .modal-leave-active { transition: opacity 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .confirm-modal, .modal-leave-active .confirm-modal { 
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); 
}
.modal-enter-from .confirm-modal { transform: scale(0.9); }
.modal-leave-to .confirm-modal { transform: scale(0.95); }

.orders-container {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 40px;
  text-align: center;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 8px;
}

.subtitle {
  color: #86868b;
  font-size: 16px;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.order-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f2f2f7;
}

.order-id .label {
  font-size: 12px;
  color: #86868b;
  display: block;
  text-transform: uppercase;
}

.order-id .value {
  font-size: 18px;
  font-weight: 700;
  color: #1d1d1f;
}

.order-status-pill {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.status-cho_duyet { background: #fff4e6; color: #f08c00; }
.status-da_duyet { background: #e7f5ff; color: #228be6; }
.status-dang_giao { background: #f3f0ff; color: #7950f2; }
.status-hoan_thanh { background: #ebfbee; color: #40c057; }
.status-da_huy { background: #fff5f5; color: #fa5252; }

/* Timeline */
.order-timeline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding: 0 20px;
}

.timeline-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 1;
}

.step-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #d2d2d7;
  transition: all 0.3s ease;
}

.timeline-step.active .step-dot {
  background: #007aff;
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.2);
}

.step-label {
  font-size: 11px;
  color: #86868b;
  font-weight: 500;
}

.timeline-step.active .step-label {
  color: #1d1d1f;
  font-weight: 700;
}

.timeline-line {
  flex: 1;
  height: 2px;
  background: #d2d2d7;
  margin-top: -18px;
}

.order-items-summary {
  background: #fbfbfd;
  padding: 16px;
  border-radius: 12px;
}

.item-name {
  font-weight: 600;
  color: #1d1d1f;
}

.item-variant-info {
  font-size: 12px;
  color: #86868b;
  margin-left: 6px;
}

.order-footer {
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.order-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.delete-order-btn {
  background: none;
  border: none;
  color: #ff3b30;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  text-align: left;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.delete-order-btn:hover {
  opacity: 1;
  text-decoration: underline;
}

.order-date {
  font-size: 13px;
  color: #86868b;
}

.order-total .label {
  font-size: 13px;
  color: #86868b;
}

.order-total .amount {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: #007aff;
}

.empty-orders {
  text-align: center;
  padding: 60px 0;
}

.empty-icon { font-size: 64px; margin-bottom: 24px; }

.shop-now-btn {
  display: inline-block;
  margin-top: 24px;
  padding: 12px 32px;
  background: #007aff;
  color: white;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
}
</style>
