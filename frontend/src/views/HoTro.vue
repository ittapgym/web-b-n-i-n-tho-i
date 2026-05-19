<template>
  <div class="category-page">
    <main class="main-content">
      <section class="support-section">
        <div class="support-header">
          <span class="os-label macos">Peach Store Support</span>
          <h2 class="showcase-title">Chúng tôi ở đây để giúp bạn.</h2>
          
          <!-- Warranty Search Bar -->
          <div class="support-search">
            <input 
              type="text" 
              v-model="imeiQuery" 
              placeholder="Nhập số IMEI (gồm 10 số và 2 chữ)..." 
              class="support-input" 
              @keyup.enter="lookupWarranty"
            />
            <button 
              class="pill-btn primary support-btn" 
              @click="lookupWarranty"
              :disabled="isLoadingWarranty"
            >
              {{ isLoadingWarranty ? 'Đang kiểm tra...' : 'Kiểm tra bảo hành' }}
            </button>
          </div>

          <!-- Beautiful Premium Warranty Result Card -->
          <div v-if="warrantyResult" class="warranty-card-container fade-in">
             <div class="warranty-result-card" :class="warrantyResult.trang_thai_bao_hanh">
                <!-- Card Header -->
                <div class="card-header-row">
                   <div class="device-info">
                      <div class="device-icon">
                         <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="5" y="2" width="14" height="20" rx="3" />
                            <line x1="12" y1="18" x2="12.01" y2="18" stroke-width="3" stroke-linecap="round" />
                         </svg>
                      </div>
                      <div class="device-text">
                         <h4>{{ warrantyResult.ten_san_pham }}</h4>
                         <span class="imei-label">IMEI: {{ warrantyResult.imei }}</span>
                      </div>
                   </div>
                   <!-- Membership Tier Badge -->
                   <span class="loyalty-badge-premium" :class="getLoyaltyClass(warrantyResult.hang_the)">
                      Thẻ {{ warrantyResult.hang_the }}
                   </span>
                </div>

                <!-- Divider -->
                <div class="premium-divider"></div>

                <!-- Warranty Details Info Grid -->
                <div class="warranty-info-grid">
                   <div class="info-item">
                      <span class="info-label">Khách hàng</span>
                      <span class="info-value">{{ warrantyResult.ten_khach_hang }}</span>
                   </div>
                   <div class="info-item">
                      <span class="info-label">Số điện thoại</span>
                      <span class="info-value">{{ warrantyResult.so_dien_thoai }}</span>
                   </div>
                   <div class="info-item">
                      <span class="info-label">Ngày kích hoạt</span>
                      <span class="info-value">{{ warrantyResult.ngay_mua }}</span>
                   </div>
                   <div class="info-item">
                      <span class="info-label">Gói bảo hành</span>
                      <span class="info-value">{{ warrantyResult.thoi_han_bao_hanh }}</span>
                   </div>
                </div>

                <!-- Progress Bar & Active Status -->
                <div class="warranty-status-progress">
                   <div class="status-indicator-row">
                      <span class="status-text-bold">
                         Trạng thái: 
                         <span class="status-val" :class="warrantyResult.trang_thai_bao_hanh">
                            {{ warrantyResult.trang_thai_bao_hanh === 'ConHieuLuc' ? 'Còn Hiệu Lực' : (warrantyResult.trang_thai_bao_hanh === 'ChuaKichHoat' ? 'Chưa Kích Hoạt' : 'Đã Hết Hạn') }}
                         </span>
                      </span>
                      <span v-if="warrantyResult.trang_thai_bao_hanh === 'ConHieuLuc'" class="days-remaining">
                         Còn lại <strong>{{ warrantyResult.so_ngay_con_lai }}</strong> ngày bảo hành
                      </span>
                      <span v-else-if="warrantyResult.trang_thai_bao_hanh === 'ChuaKichHoat'" class="days-remaining" style="color: #f08c00;">Đang chờ hoàn thành đơn hàng</span><span v-else class="days-remaining expired-text" style="color: #ff3b30;">
                         Hết hạn bảo hành
                      </span>
                   </div>

                   <!-- Apple Style Visual Progress Bar -->
                   <div class="progress-bar-bg">
                      <div 
                         class="progress-bar-fill" 
                         :class="warrantyResult.trang_thai_bao_hanh"
                         :style="{ width: getProgressBarWidth(warrantyResult) }"
                      ></div>
                   </div>
                   <div class="progress-labels">
                      <span>0 tháng</span>
                      <span>Hết hạn ({{ warrantyResult.ngay_het_han }})</span>
                   </div>
                </div>
             </div>
          </div>

          <!-- Error Alert State -->
          <div v-if="warrantyError" class="warranty-error-box fade-in">
             <div class="error-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                   <circle cx="12" cy="12" r="10" />
                   <line x1="12" y1="8" x2="12" y2="12" />
                   <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
             </div>
             <p>{{ warrantyError }}</p>
          </div>
        </div>

        <div class="support-grid">
          <div class="support-card" @click="openHelpModal('password')">
            <div class="support-icon blue">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path
                  d="M12 15V17M12 7V13M12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21Z"
                  stroke-linecap="round"
                />
              </svg>
            </div>
            <p>Quên mật khẩu tài khoản</p>
          </div>
          <div class="support-card" @click="openHelpModal('pin')">
            <div class="support-icon green">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                <circle cx="12" cy="16" r="1.5" fill="currentColor"/>
              </svg>
            </div>
            <p>Quên mật khẩu mã pin</p>
          </div>
          <div class="support-card" @click="openHelpModal('terms')">
            <div class="support-icon red">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-linecap="round"/>
                <polyline points="14 2 14 8 20 8" stroke-linecap="round"/>
                <line x1="16" y1="13" x2="8" y2="13" stroke-linecap="round"/>
                <line x1="16" y1="17" x2="8" y2="17" stroke-linecap="round"/>
                <polyline points="10 9 9 9 8 9" stroke-linecap="round"/>
              </svg>
            </div>
            <p>Xem điều khoản của web</p>
          </div>
        </div>

        <!-- Reusable Apple Help Modal -->
        <div class="apple-modal-overlay" v-if="showHelpModal" @click.self="closeHelpModal">
          <div class="apple-modal-card">
            <div class="modal-icon-container" :class="helpModalData.color">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="modal-icon" v-html="helpModalData.icon"></svg>
            </div>
            <h3 class="modal-title">{{ helpModalData.title }}</h3>
            
            <!-- Paragraph Descs (Always visible for Terms, hidden for Form during Success) -->
            <div v-if="helpModalData.type === 'terms'" class="modal-desc" style="text-align: left; max-height: 250px; overflow-y: auto; padding-right: 4px; width: 100%;">
              <p v-for="(paragraph, index) in helpModalData.paragraphs" :key="index" style="margin-bottom: 12px; font-size: 14px; color: #515154; line-height: 1.6; margin-top: 0;">
                {{ paragraph }}
              </p>
            </div>

            <!-- Form for Password & PIN Reset requests -->
            <div v-if="(helpModalData.type === 'password' || helpModalData.type === 'pin') && !showSuccessState" class="modal-form" style="width: 100%; margin-top: 12px; text-align: left; display: flex; flex-direction: column; gap: 10px;">
              <p style="font-size: 12px; color: #86868b; line-height: 1.4; margin: 0 0 4px 0;">
                Vui lòng cung cấp chính xác 4 trường thông tin đã đăng ký để Admin đối chiếu và cấp lại bảo mật cho bạn.
              </p>
              
              <div class="modal-input-group">
                <label>Họ và tên đăng ký đầy đủ *</label>
                <input 
                  type="text" 
                  v-model="requestForm.fullName" 
                  placeholder="Nhập họ và tên đầy đủ..." 
                  class="modal-input-field"
                  style="padding: 10px 14px; font-size: 14px;"
                />
              </div>
              
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                <div class="modal-input-group">
                  <label>Email đăng ký *</label>
                  <input 
                    type="email" 
                    v-model="requestForm.email" 
                    placeholder="email@example.com" 
                    class="modal-input-field"
                    style="padding: 10px 14px; font-size: 14px;"
                  />
                </div>
                <div class="modal-input-group">
                  <label>Số điện thoại *</label>
                  <input 
                    type="tel" 
                    v-model="requestForm.phone" 
                    placeholder="09xxxxxxxx" 
                    class="modal-input-field"
                    style="padding: 10px 14px; font-size: 14px;"
                  />
                </div>
              </div>

              <div class="modal-input-group">
                <label>Địa chỉ thường trú đăng ký *</label>
                <input 
                  type="text" 
                  v-model="requestForm.address" 
                  placeholder="Nhập địa chỉ đăng ký tài khoản..." 
                  class="modal-input-field"
                  style="padding: 10px 14px; font-size: 14px;"
                />
              </div>

              <div class="modal-input-group">
                <label>Nội dung chi tiết yêu cầu</label>
                <textarea 
                  v-model="requestForm.message" 
                  placeholder="Nhập thêm chi tiết nếu có..." 
                  class="modal-input-field"
                  style="height: 55px; resize: none; padding: 10px 14px; font-size: 14px;"
                ></textarea>
              </div>
            </div>

            <!-- Success State -->
            <div v-if="showSuccessState" style="text-align: center; padding: 12px 0; width: 100%;">
              <div style="width: 50px; height: 50px; background: #e3f9e5; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; color: #34c759;">
                <svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="3">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <h4 style="font-size: 16px; font-weight: 700; color: #1d1d1f; margin: 0 0 8px 0;">Gửi yêu cầu thành công!</h4>
              <p style="font-size: 13px; color: #86868b; line-height: 1.5; margin: 0;">
                Yêu cầu hỗ trợ của bạn đã được chuyển đến hệ thống Peach Store. Admin sẽ kiểm tra và phản hồi thông tin sớm nhất có thể.
              </p>
            </div>

            <!-- Action buttons -->
            <div class="modal-actions-row" style="margin-top: 24px; width: 100%; display: flex; gap: 12px;">
              <!-- For terms or success state -->
              <button 
                v-if="helpModalData.type === 'terms' || showSuccessState" 
                class="modal-btn-primary" 
                style="width: 100%; flex: 1;" 
                @click="closeHelpModal"
              >
                {{ showSuccessState ? 'Đóng' : 'Đã hiểu' }}
              </button>

              <!-- For active forms -->
              <template v-else>
                <button 
                  class="modal-btn-secondary" 
                  style="flex: 1;" 
                  @click="closeHelpModal"
                  :disabled="isSubmittingRequest"
                >
                  Hủy bỏ
                </button>
                <button 
                  class="modal-btn-primary" 
                  style="flex: 1;" 
                  @click="submitStaticRequest"
                  :disabled="isSubmittingRequest || !requestForm.fullName || !requestForm.email || !requestForm.phone || !requestForm.address"
                >
                  {{ isSubmittingRequest ? 'Đang gửi...' : 'Gửi yêu cầu' }}
                </button>
              </template>
            </div>
          </div>
        </div>

        <div class="search-topics">
          <h3>Tìm kiếm thêm các chủ đề</h3>
          <div class="topic-input-wrap">
            <svg
              viewBox="0 0 24 24"
              width="18"
              height="18"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="search-icon"
            >
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
            <input type="text" placeholder="Tìm kiếm hỗ trợ" />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showHelpModal = ref(false)
const isSubmittingRequest = ref(false)
const showSuccessState = ref(false)

// Warranty lookup state
const imeiQuery = ref('')
const isLoadingWarranty = ref(false)
const warrantyResult = ref(null)
const warrantyError = ref('')

const lookupWarranty = async () => {
  const query = imeiQuery.value ? imeiQuery.value.trim() : ''
  if (!query) {
    warrantyError.value = 'Vui lòng nhập mã IMEI để tra cứu!'
    warrantyResult.value = null
    return
  }
  
  isLoadingWarranty.value = true
  warrantyError.value = ''
  warrantyResult.value = null
  
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}/don-hang/tra-cuu-bao-hanh/${encodeURIComponent(query)}`)
    if (res.ok) {
      const data = await res.json()
      warrantyResult.value = data
    } else {
      const err = await res.json()
      warrantyError.value = err.detail || 'Không tìm thấy thông tin bảo hành cho mã IMEI này.'
    }
  } catch (err) {
    console.error("Lỗi tra cứu bảo hành:", err)
    warrantyError.value = 'Không thể kết nối đến máy chủ. Vui lòng thử lại!'
  } finally {
    isLoadingWarranty.value = false
  }
}

const getProgressBarWidth = (result) => {
  if (result.trang_thai_bao_hanh === 'ChuaKichHoat') return '0%'
  if (result.trang_thai_bao_hanh !== 'ConHieuLuc') return '0%'
  const totalDays = parseInt(result.thoi_han_bao_hanh) * 30 || 180
  const remainingDays = result.so_ngay_con_lai
  const percentage = Math.min(100, Math.max(0, (remainingDays / totalDays) * 100))
  return `${percentage}%`
}

const getLoyaltyClass = (tier) => {
  if (tier === 'Kim cương') return 'diamond'
  if (tier === 'Vàng') return 'gold'
  return 'silver'
}
const requestForm = ref({
  fullName: '',
  email: '',
  phone: '',
  address: '',
  message: ''
})

const helpModalData = ref({
  type: '',
  title: '',
  color: '',
  icon: '',
  paragraphs: []
})

const openHelpModal = (type) => {
  // Reset form and success state on modal open
  showSuccessState.value = false
  isSubmittingRequest.value = false
  requestForm.value = {
    fullName: '',
    email: '',
    phone: '',
    address: '',
    message: ''
  }

  if (type === 'password') {
    helpModalData.value = {
      type: 'password',
      title: 'Khôi phục mật khẩu tài khoản',
      color: 'blue',
      icon: '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>',
      paragraphs: [
        'Vui lòng cung cấp họ tên và số điện thoại/email đăng ký của tài khoản để gửi yêu cầu hỗ trợ khôi phục mật khẩu trực tiếp đến Admin.'
      ]
    }
  } else if (type === 'pin') {
    helpModalData.value = {
      type: 'pin',
      title: 'Khôi phục mật khẩu mã PIN',
      color: 'green',
      icon: '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path>',
      paragraphs: [
        'Vui lòng cung cấp thông tin tài khoản của bạn để gửi yêu cầu hỗ trợ xóa/khôi phục lại mã PIN giao dịch trực tiếp đến Admin.'
      ]
    }
  } else if (type === 'terms') {
    helpModalData.value = {
      type: 'terms',
      title: 'Điều khoản dịch vụ Peach Store',
      color: 'red',
      icon: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline>',
      paragraphs: [
        '1. Cam kết chính hãng: Peach Store cam kết 100% tất cả các mặt hàng điện thoại, máy tính bảng và phụ kiện bán ra đều là hàng Apple chính hãng, có nguồn gốc rõ ràng.',
        '2. Chính sách bảo mật: Peach Store bảo vệ tuyệt đối dữ liệu giao dịch của khách hàng bằng công nghệ mã PIN hiện đại được băm mã hóa lưu trực tiếp trên máy chủ.',
        '3. Điều khoản đổi trả: Khách hàng được quyền đồng kiểm khi nhận hàng, được đổi trả sản phẩm miễn phí trong vòng 7 ngày đầu nếu có bất kỳ lỗi phần cứng nào từ nhà sản xuất.'
      ]
    }
  }
  showHelpModal.value = true
}

const closeHelpModal = () => {
  showHelpModal.value = false
}

const submitStaticRequest = async () => {
  isSubmittingRequest.value = true
  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}/api/support/reset-requests`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        type: helpModalData.value.type,
        fullName: requestForm.value.fullName,
        email: requestForm.value.email,
        phone: requestForm.value.phone,
        address: requestForm.value.address,
        message: requestForm.value.message
      })
    })
    
    if (response.ok) {
      showSuccessState.value = true
    } else {
      alert("Đã xảy ra lỗi khi gửi yêu cầu. Vui lòng thử lại!")
    }
  } catch (error) {
    console.error("Lỗi gửi yêu cầu hỗ trợ:", error)
    alert("Không thể kết nối đến máy chủ.")
  } finally {
    isSubmittingRequest.value = false
  }
}
</script>

<style scoped>
.category-page {
  min-height: 100vh;
  background-color: #ffffff;
}

.main-content {
  padding-top: 44px;
}

.showcase-title {
  font-size: 56px;
  font-weight: 700;
  line-height: 1.1;
  color: #1d1d1f;
  letter-spacing: -0.02em;
}

.os-label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  display: block;
}

.os-label.macos {
  color: #e74c3c;
  font-size: 20px;
}

/* SUPPORT SECTION */
.support-section {
  padding: 100px 20px;
  background-color: #ffffff; /* Đổi sang trắng tinh */
  text-align: center;
}

.support-header {
  margin-bottom: 60px;
}

.support-search {
  margin-top: 32px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

.support-input {
  width: 100%;
  max-width: 400px;
  padding: 12px 20px;
  border-radius: 12px;
  border: 1px solid #d2d2d7;
  font-size: 17px;
  background-color: #ffffff;
}

.pill-btn {
  padding: 12px 26px;
  border-radius: 980px;
  font-size: 17px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.pill-btn.primary {
  background-color: #0071e3;
  color: #ffffff;
}

.pill-btn.primary:hover {
  background-color: #0077ed;
}

.support-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto 80px;
}

.support-card {
  background-color: #ffffff;
  padding: 40px 20px;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.support-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.support-icon {
  width: 48px;
  height: 48px;
}

.support-icon.blue {
  color: #0071e3;
}
.support-icon.green {
  color: #2ecc71;
}
.support-icon.red {
  color: #ff3b30;
}

.support-card p {
  font-size: 14px;
  color: #0066cc;
  font-weight: 500;
}

.search-topics {
  max-width: 800px;
  margin: 0 auto;
}

.search-topics h3 {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 32px;
}

.topic-input-wrap {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.topic-input-wrap .search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #86868b;
}

.topic-input-wrap input {
  width: 100%;
  padding: 16px 16px 16px 48px;
  border-radius: 12px;
  border: 1px solid #d2d2d7;
  font-size: 17px;
  background-color: #ffffff;
}

@media (max-width: 768px) {
  .showcase-title {
    font-size: 40px;
  }
  .support-grid {
    grid-template-columns: 1fr;
  }
  .support-search {
    flex-direction: column;
    align-items: center;
  }
  .support-input {
    max-width: 100%;
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
  max-width: 440px;
  padding: 32px 28px 24px;
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

.modal-icon-container.green {
  background: #f2faf5;
  border: 2px solid #34c759;
  color: #34c759;
}

.modal-icon-container.red {
  background: #fff0f0;
  border: 2px solid #ff3b30;
  color: #ff3b30;
}

.modal-icon {
  width: 28px;
  height: 28px;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 16px 0;
}

.modal-desc {
  width: 100%;
}

.modal-form {
  width: 100%;
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}

.modal-input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.modal-input-group label {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
}

.modal-input-field {
  width: 100%;
  background: #f5f5f7;
  border: 1px solid #d2d2d7;
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 15px;
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
  text-align: center;
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
  text-align: center;
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

/* WARRANTY CARD PREMIUM STYLING */
.warranty-card-container {
  display: flex;
  justify-content: center;
  margin-top: 32px;
  width: 100%;
}

.warranty-result-card {
  width: 100%;
  max-width: 550px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 24px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  padding: 28px;
  text-align: left;
  box-sizing: border-box;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.device-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.device-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(0, 113, 227, 0.08);
  color: #0071e3;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.device-icon svg {
  width: 24px;
  height: 24px;
}

.device-text h4 {
  font-size: 18px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 2px 0;
  line-height: 1.2;
}

.imei-label {
  font-size: 13px;
  color: #86868b;
  font-family: 'SF Mono', Monaco, monospace;
}

.loyalty-badge-premium {
  padding: 6px 12px;
  border-radius: 980px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.loyalty-badge-premium.silver {
  background: rgba(142, 142, 147, 0.1);
  color: #8e8e93;
  border: 1px solid rgba(142, 142, 147, 0.2);
}

.loyalty-badge-premium.gold {
  background: rgba(255, 204, 0, 0.1);
  color: #b8860b;
  border: 1px solid rgba(255, 204, 0, 0.2);
}

.loyalty-badge-premium.diamond {
  background: rgba(0, 122, 255, 0.1);
  color: #007aff;
  border: 1px solid rgba(0, 122, 255, 0.2);
}

.premium-divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.06);
  margin: 20px 0;
}

.warranty-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: #86868b;
  font-weight: 500;
}

.info-value {
  font-size: 15px;
  color: #1d1d1f;
  font-weight: 600;
}

.warranty-status-progress {
  margin-top: 24px;
}

.status-indicator-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 13px;
}

.status-text-bold {
  font-weight: 600;
  color: #1d1d1f;
}

.status-val {
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}

.status-val.ConHieuLuc {
  color: #34c759;
  background: rgba(52, 199, 89, 0.1);
}

.status-val.HetHieuLuc {
  color: #ff3b30;
  background: rgba(255, 59, 48, 0.1);
}

.status-val.ChuaKichHoat {
  color: #f08c00;
  background: rgba(240, 140, 0, 0.1);
}

.days-remaining {
  color: #34c759;
  font-weight: 500;
}

.days-remaining strong {
  font-size: 15px;
  font-weight: 700;
}

.days-remaining.expired-text {
  color: #ff3b30;
  font-weight: 600;
}

.progress-bar-bg {
  height: 8px;
  background: #e5e5ea;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-bar-fill.ConHieuLuc {
  background: linear-gradient(90deg, #34c759, #30b0c7);
}

.progress-bar-fill.HetHieuLuc {
  background: #ff3b30;
  width: 0% !important;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #86868b;
  margin-top: 6px;
}

.warranty-error-box {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 24px auto 0;
  padding: 16px 20px;
  background: rgba(255, 59, 48, 0.05);
  border: 1px solid rgba(255, 59, 48, 0.15);
  border-radius: 16px;
  max-width: 550px;
  text-align: left;
  box-sizing: border-box;
}

.error-icon {
  color: #ff3b30;
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.error-icon svg {
  width: 20px;
  height: 20px;
}

.warranty-error-box p {
  margin: 0;
  font-size: 14px;
  color: #ff3b30;
  font-weight: 500;
  line-height: 1.4;
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}
</style>
