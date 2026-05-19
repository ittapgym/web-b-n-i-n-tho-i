<template>
  <div class="account-page">
    <div class="account-container">
      <!-- Header Section -->
      <header class="account-header">
        <div class="profile-summary">
          <div class="avatar-wrapper" @click="triggerAvatarUpload">
            <div v-if="user.hinh_anh" class="avatar-img-container">
              <img :src="getImageUrl(user.hinh_anh)" alt="Avatar" class="avatar-image" />
              <div class="avatar-overlay">Thay đổi</div>
            </div>
            <button v-if="user.hinh_anh" class="remove-avatar-btn" @click.stop="removeAvatar" title="Xóa ảnh">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
            <div v-else class="avatar-circle">
              {{ user.ho_ten ? user.ho_ten.charAt(0).toUpperCase() : 'U' }}
              <div class="avatar-overlay">Tải lên</div>
            </div>
            <input 
              type="file" 
              ref="avatarInput" 
              class="hidden-input" 
              accept="image/*" 
              @change="handleAvatarUpload" 
            />
          </div>
          <div class="name-stack">
            <h1 class="user-name">{{ user.ho_ten || 'Peach User' }}</h1>
            <p class="user-email">{{ user.email }}</p>
          </div>
        </div>
        <div class="membership-status" style="display: flex; flex-direction: column; align-items: flex-end; justify-content: center; gap: 4px;">
          <span class="status-label" style="margin: 0;">Hạng thành viên</span>
          <div style="display: flex; align-items: center; gap: 8px; margin-top: 2px;">
            <span class="status-value" :class="getRankClass(user)" style="font-weight: 700;">{{ getMembershipRank(user) }}</span>
            <button 
              @click="showLoyaltyDetailsModal = true" 
              style="background: rgba(0, 122, 255, 0.08); border: none; color: #007aff; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: all 0.2s;"
              onmouseover="this.style.background='rgba(0, 122, 255, 0.15)'"
              onmouseout="this.style.background='rgba(0, 122, 255, 0.08)'"
            >
              <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor" style="display: inline-block;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
              Xem chi tiết
            </button>
          </div>
        </div>
      </header>

      <div class="content-layout">
        <!-- Sidebar Navigation (Lined Style) -->
        <nav class="account-nav">
          <button 
            v-for="item in menuItems" 
            :key="item.id"
            :class="['nav-link', { active: activeTab === item.id }]"
            @click="setActiveTab(item.id)"
            style="position: relative; display: flex; align-items: center; justify-content: space-between; width: 100%;"
          >
            <span>{{ item.label }}</span>
            <span v-if="getBadgeCount(item.id) > 0" 
                  style="background: #ff3b30; color: white; font-size: 11px; font-weight: 700; border-radius: 10px; padding: 2px 7px; display: inline-flex; align-items: center; justify-content: center; min-width: 18px; height: 18px; line-height: 1; margin-left: 8px;">
              {{ getBadgeCount(item.id) }}
            </span>
          </button>
          <div class="nav-divider"></div>
          
          <!-- Khối nút chức năng Sidebar -->
          <div class="sidebar-action-block" v-if="activeTab === 'profile'">
            <button class="action-btn-item save" @click="saveProfile" :disabled="saving">
              {{ saving ? 'Đang lưu...' : 'Lưu hồ sơ' }}
            </button>
            <button class="action-btn-item logout" @click="handleLogout">
              Đăng xuất
            </button>
          </div>
          <button v-else class="nav-link logout" @click="handleLogout">Đăng xuất</button>
        </nav>

        <!-- Main Content Area -->
        <main class="account-content">
          <!-- Mobile Navigation Trigger (only visible on mobile/tablet) -->
          <div class="mobile-nav-trigger-wrapper">
            <button class="mobile-nav-trigger-btn" @click="toggleMobileMenu">
              <span>Danh sách chức năng</span>
              <svg :class="['chevron-icon', { rotate: showMobileMenu }]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>

            <!-- Inline Expandable Menu Panel -->
            <div v-if="showMobileMenu" class="mobile-menu-inline-panel">
              <div class="inline-panel-header">
                <span>Chọn chức năng</span>
                <button class="inline-close-btn" @click="toggleMobileMenu" title="Đóng">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
              
              <nav class="mobile-account-nav">
                <button 
                  v-for="item in menuItems" 
                  :key="item.id"
                  :class="['mobile-nav-link', { active: activeTab === item.id }]"
                  @click="setActiveTab(item.id)"
                  style="display: flex; align-items: center; justify-content: space-between; width: 100%;"
                >
                  <span style="display: flex; align-items: center; gap: 8px;">
                    {{ item.label }}
                    <span v-if="getBadgeCount(item.id) > 0" 
                          style="background: #ff3b30; color: white; font-size: 11px; font-weight: 700; border-radius: 10px; padding: 2px 7px; display: inline-flex; align-items: center; justify-content: center; min-width: 18px; height: 18px; line-height: 1;">
                      {{ getBadgeCount(item.id) }}
                    </span>
                  </span>
                  <svg v-if="activeTab === item.id" class="checkmark-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="margin-left: auto;">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </button>
                
                <div class="nav-divider"></div>
                
                <!-- Khối nút chức năng Sidebar Mobile -->
                <div class="mobile-sidebar-action-block" v-if="activeTab === 'profile'">
                  <button class="mobile-action-btn save" @click="saveProfile" :disabled="saving">
                    {{ saving ? 'Đang lưu...' : 'Lưu hồ sơ' }}
                  </button>
                  <button class="mobile-action-btn logout" @click="handleLogout">
                    Đăng xuất
                  </button>
                </div>
                <button v-else class="mobile-nav-link logout" @click="handleLogout">
                  Đăng xuất
                </button>
              </nav>
            </div>
          </div>

          <!-- Tab: Hồ sơ -->
          <div v-if="activeTab === 'profile'" class="settings-section">
            <div class="profile-scroll-container">
              <div class="settings-group">
                <h2 class="group-title">Thông tin cá nhân</h2>
                
                <div class="settings-table">
                  <div class="table-row">
                    <div class="table-label">Họ và tên</div>
                    <div class="table-value">
                      <div class="input-wrapper">
                        <input type="text" v-model="user.ho_ten" placeholder="Họ và tên của bạn">
                      </div>
                    </div>
                  </div>

                  <div class="table-row">
                    <div class="table-label">Số điện thoại</div>
                    <div class="table-value">
                      <div class="input-wrapper">
                        <input 
                          type="text" 
                          v-model="user.so_dien_thoai" 
                          placeholder="Chưa cập nhật"
                          @input="validatePhone"
                          maxlength="10"
                        >
                      </div>
                    </div>
                  </div>

                  <div class="table-row">
                    <div class="table-label">Email</div>
                    <div class="table-value">
                      <div class="value-text">{{ user.email }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="settings-group">
                <h2 class="group-title">Địa chỉ nhận hàng</h2>
                <div class="settings-table">
                  <div class="table-row">
                    <div class="table-label">Địa chỉ mặc định</div>
                    <div class="table-value">
                      <div class="input-wrapper">
                        <textarea v-model="user.dia_chi" placeholder="Nhập địa chỉ giao hàng để chúng tôi tự động điền khi bạn mua sắm..."></textarea>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Phân loại tài khoản & Đăng ký Doanh nghiệp -->
              <div v-if="user.vai_role === 'doanh_nghiep' || user.vai_tro === 'doanh_nghiep'" class="settings-group business-card-verified" style="margin-top: 24px;">
                <h2 class="group-title">Thông tin Doanh nghiệp (Đã xác minh)</h2>
                <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-radius: 16px; padding: 20px; border: 1px solid #81c784; display: flex; align-items: flex-start; gap: 16px; margin-top: 10px;">
                  <div style="background: #4caf50; color: white; padding: 8px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                  </div>
                  <div style="flex: 1;">
                    <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #2e7d32; text-align: left;">Tài khoản Doanh nghiệp của bạn đã sẵn sàng!</h4>
                    <p style="margin: 4px 0 12px 0; font-size: 13px; color: #388e3c; line-height: 1.4; text-align: left;">Bạn được hưởng đặc quyền mua sắm số lượng lớn, không bị giới hạn số lượng sản phẩm mua mỗi ngày.</p>
                    <div style="background: white; border-radius: 12px; padding: 14px; border: 1px solid rgba(0,0,0,0.05); font-size: 13px; color: #1d1d1f; display: grid; grid-template-columns: 140px 1fr; gap: 8px 16px; text-align: left;">
                      <strong>Tên doanh nghiệp:</strong> <span>{{ user.ten_doanh_nghiep }}</span>
                      <strong>Mã số thuế:</strong> <span>{{ user.ma_so_thue }}</span>
                      <strong>Địa chỉ kinh doanh:</strong> <span>{{ user.dia_chi_kd }}</span>
                      <strong>Lĩnh vực hoạt động:</strong> <span>{{ user.linh_vuc_kd }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else-if="businessRequest.has_request && businessRequest.trang_thai === 'cho_duyet'" class="settings-group" style="margin-top: 24px;">
                <h2 class="group-title">Yêu cầu nâng cấp Doanh nghiệp</h2>
                <div style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border-radius: 16px; padding: 20px; border: 1px solid #fde047; display: flex; align-items: flex-start; gap: 16px; margin-top: 10px;">
                  <div style="background: #d97706; color: white; padding: 8px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 36px; height: 36px; box-sizing: border-box;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                  </div>
                  <div style="flex: 1;">
                    <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #b45309; text-align: left;">Đang chờ phê duyệt từ Ban quản trị</h4>
                    <p style="margin: 4px 0 12px 0; font-size: 13px; color: #d97706; line-height: 1.4; text-align: left;">Đội ngũ Peach Store đang kiểm định hồ sơ khai báo của bạn. Sau khi được duyệt, tài khoản của bạn sẽ tự động nâng cấp để đặt hàng không giới hạn số lượng.</p>
                    <div style="background: white; border-radius: 12px; padding: 14px; border: 1px solid rgba(0,0,0,0.05); font-size: 13px; color: #1d1d1f; display: grid; grid-template-columns: 140px 1fr; gap: 8px 16px; text-align: left;">
                      <strong>Tên doanh nghiệp:</strong> <span>{{ businessRequest.ten_doanh_nghiep }}</span>
                      <strong>Mã số thuế:</strong> <span>{{ businessRequest.ma_so_thue }}</span>
                      <strong>Địa chỉ đăng ký:</strong> <span>{{ businessRequest.dia_chi_kd }}</span>
                      <strong>Ngành nghề kinh doanh:</strong> <span>{{ businessRequest.linh_vuc_kd }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="settings-group" style="margin-top: 24px;">
                <h2 class="group-title">Đăng ký mua hàng Doanh nghiệp</h2>
                
                <!-- Thêm thông báo nếu yêu cầu trước đó bị từ chối -->
                <div v-if="businessRequest.has_request && businessRequest.trang_thai === 'tu_choi'" style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border-radius: 16px; padding: 20px; border: 1px solid #fca5a5; display: flex; align-items: flex-start; gap: 16px; margin-top: 10px; margin-bottom: 16px;">
                  <div style="background: #ef4444; color: white; padding: 8px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 36px; height: 36px; box-sizing: border-box;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
                  </div>
                  <div style="flex: 1;">
                    <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #991b1b; text-align: left;">Yêu cầu trước đó không được phê duyệt</h4>
                    <p style="margin: 4px 0 0 0; font-size: 13px; color: #b91c1c; line-height: 1.4; text-align: left;">Rất tiếc, thông tin đăng ký doanh nghiệp của bạn đã bị từ chối duyệt vì không trùng khớp hoặc không đủ điều kiện. Vui lòng kiểm tra kỹ và khai báo lại biểu mẫu đăng ký bên dưới.</p>
                  </div>
                </div>
                
                <div style="background: #f5f5f7; border-radius: 16px; padding: 20px; border: 1px solid rgba(0,0,0,0.03); display: flex; flex-direction: column; gap: 16px; margin-top: 10px;">
                  <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <div style="background: rgba(0,122,255,0.1); color: #007aff; padding: 8px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                    </div>
                    <div style="text-align: left;">
                      <h4 style="margin: 0; font-size: 15px; font-weight: 700; color: #1d1d1f;">Bạn có nhu cầu nhập hàng số lượng lớn?</h4>
                      <p style="margin: 4px 0 0 0; font-size: 13px; color: #86868b; line-height: 1.4;">Tài khoản Cá nhân mặc định bị giới hạn mua tối đa <strong>10 sản phẩm mỗi ngày</strong>. Hãy đăng ký tài khoản Doanh nghiệp để bứt phá giới hạn và đặt mua không giới hạn số lượng!</p>
                    </div>
                  </div>

                  <div class="settings-table" style="background: white; border-radius: 12px; padding: 16px; border: 1px solid rgba(0,0,0,0.05); display: flex; flex-direction: column; gap: 12px; border-bottom: none;">
                    <div style="display: flex; flex-direction: column; gap: 4px; text-align: left;">
                      <label style="font-size: 11px; font-weight: 700; color: #86868b; text-transform: uppercase; letter-spacing: 0.5px;">Tên doanh nghiệp / Hộ kinh doanh</label>
                      <input type="text" v-model="businessForm.ten_doanh_nghiep" placeholder="Ví dụ: Công ty TNHH Peach Store Việt Nam" style="width: 100%; padding: 10px 14px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; font-size: 14px; box-sizing: border-box;">
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                      <div style="display: flex; flex-direction: column; gap: 4px; text-align: left;">
                        <label style="font-size: 11px; font-weight: 700; color: #86868b; text-transform: uppercase; letter-spacing: 0.5px;">Mã số thuế</label>
                        <input type="text" v-model="businessForm.ma_so_thue" placeholder="Mã số thuế doanh nghiệp" style="width: 100%; padding: 10px 14px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; font-size: 14px; box-sizing: border-box;">
                      </div>
                      <div style="display: flex; flex-direction: column; gap: 4px; text-align: left;">
                        <label style="font-size: 11px; font-weight: 700; color: #86868b; text-transform: uppercase; letter-spacing: 0.5px;">Lĩnh vực kinh doanh</label>
                        <input type="text" v-model="businessForm.linh_vuc_kd" placeholder="Ví dụ: Bán lẻ, Bán sỉ, Thương mại" style="width: 100%; padding: 10px 14px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; font-size: 14px; box-sizing: border-box;">
                      </div>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 4px; text-align: left;">
                      <label style="font-size: 11px; font-weight: 700; color: #86868b; text-transform: uppercase; letter-spacing: 0.5px;">Địa chỉ kinh doanh / Trụ sở chính</label>
                      <input type="text" v-model="businessForm.dia_chi_kd" placeholder="Địa chỉ đăng ký kinh doanh chính thức" style="width: 100%; padding: 10px 14px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; font-size: 14px; box-sizing: border-box;">
                    </div>

                    <button 
                      @click="submitBusinessRegistration" 
                      :disabled="submittingBusiness"
                      style="background: #007aff; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.2s; margin-top: 8px; width: fit-content; align-self: flex-end;"
                    >
                      {{ submittingBusiness ? 'Đang gửi yêu cầu...' : 'Gửi yêu cầu nâng cấp Doanh nghiệp' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tab: Lịch sử mua hàng (Thanh lịch) -->
          <div v-if="activeTab === 'orders'" class="settings-section">
            <h2 class="group-title">Lịch sử đơn hàng</h2>
            
            <div class="order-list" v-if="orders.length > 0">
              <div v-for="order in orders" :key="order.id" class="order-item">
                <div class="order-header">
                  <div class="order-info-main">
                    <span class="order-id">Mã đơn: #{{ order.id }}</span>
                    <span class="order-date">Ngày đặt: {{ formatDate(order.ngay_tao) }}</span>
                  </div>
                  <div class="order-status-group">
                    <span class="order-status" :class="getStatusClass(order.trang_thai)">
                      {{ getStatusLabel(order.trang_thai) }}
                    </span>
                    <button v-if="order.trang_thai === 'cho_duyet'" class="cancel-btn-mini" @click="cancelOrder(order.id)">
                      Hủy đơn
                    </button>
                  </div>
                </div>
                <div class="order-products">
                  <div v-for="item in order.items" :key="item.id" class="product-mini">
                    <img :src="getImageUrl(item.san_pham?.hinh_anh)" class="mini-img" alt="Product" />
                    <div class="mini-details">
                      <h4>{{ item.san_pham?.ten }}</h4>
                      <p>{{ item.dung_luong }} | {{ item.mau_sac }} | SL: {{ item.so_luong }}</p>
                    </div>
                    <div class="mini-price">{{ formatPrice(item.gia) }}</div>
                  </div>
                </div>
                <div class="order-footer" style="display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; padding: 12px 16px; border-top: 1px solid rgba(0,0,0,0.05);">
                  <div v-if="order.trang_thai === 'hoan_thanh'" style="display: flex; gap: 8px;">
                    <button @click="openOrderDetail(order)" 
                            style="background: rgba(0, 122, 255, 0.08); color: #007AFF; border: 1.5px solid rgba(0, 122, 255, 0.15); border-radius: 10px; font-size: 12px; padding: 8px 16px; font-weight: 700; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 6px; box-shadow: inset 0 1px 0 rgba(255,255,255,0.4);">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                      Xem chi tiết & In hoá đơn
                    </button>
                  </div>
                  <div style="margin-left: auto; display: flex; align-items: center; gap: 8px;">
                    <span class="total-label">Tổng cộng:</span>
                    <span class="total-amount">{{ formatPrice(order.tong_tien) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="loadingOrders" class="loading-state">
              Đang tải đơn hàng...
            </div>

            <div v-else-if="orders.length === 0" class="empty-state">
              <p>Bạn chưa có đơn hàng nào.</p>
            </div>

            <!-- Modal Chi Tiết Đơn Hàng & Hóa Đơn PDF -->
            <div v-if="showOrderDetailModal && selectedOrderDetail" class="modal-overlay" @click.self="closeOrderDetail"
                 style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(10px); display: flex; align-items: center; justify-content: center; z-index: 99999; padding: 20px; box-sizing: border-box;">
              <div class="modal-content" 
                   style="background: white; border-radius: 20px; width: 680px; max-width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 40px rgba(0,0,0,0.15); display: flex; flex-direction: column; border: 1px solid rgba(0,0,0,0.08); animation: modalFadeIn 0.3s ease-out; text-align: left;">
                
                <!-- Modal Header -->
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid #e8e8ed;">
                  <div>
                    <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #1d1d1f;">Chi tiết đơn hàng #{{ selectedOrderDetail.id }}</h3>
                    <span style="font-size: 12px; color: #86868b; font-weight: 500;">Đặt ngày {{ formatDate(selectedOrderDetail.ngay_tao) }}</span>
                  </div>
                  <button @click="closeOrderDetail" style="background: rgba(0,0,0,0.05); border: none; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#86868b" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                  </button>
                </div>

                <!-- Modal Body -->
                <div style="padding: 24px; display: flex; flex-direction: column; gap: 20px;">
                  
                  <!-- Recipient & Delivery Info -->
                  <div style="background: #f5f5f7; border-radius: 16px; padding: 18px; border: 1.5px solid rgba(0, 0, 0, 0.03);">
                    <h4 style="margin: 0 0 12px 0; font-size: 13px; font-weight: 700; color: #86868b; text-transform: uppercase; letter-spacing: 0.5px;">Thông tin nhận hàng</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 13.5px; line-height: 1.5; text-align: left;">
                      <div>
                        <p style="margin: 0 0 6px 0; color: #1d1d1f;"><strong>Người nhận:</strong> {{ selectedOrderDetail.ten_khach_hang }}</p>
                        <p style="margin: 0; color: #1d1d1f;"><strong>Số điện thoại:</strong> {{ selectedOrderDetail.so_dien_thoai }}</p>
                      </div>
                      <div>
                        <p style="margin: 0 0 6px 0; color: #1d1d1f;"><strong>Địa chỉ:</strong> {{ selectedOrderDetail.dia_chi }}</p>
                        <p style="margin: 0; color: #1d1d1f;" v-if="selectedOrderDetail.ghi_chu"><strong>Ghi chú:</strong> {{ selectedOrderDetail.ghi_chu }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- IMEI & Warranty Information (Prominent copy block) -->
                  <div style="background: rgba(0, 122, 255, 0.04); border-radius: 16px; padding: 20px; border: 1.5px dashed rgba(0, 122, 255, 0.3); display: flex; align-items: center; justify-content: space-between; gap: 16px; text-align: left;">
                    <div style="flex: 1;">
                      <h4 style="margin: 0 0 6px 0; font-size: 14px; font-weight: 700; color: #007aff; display: flex; align-items: center; gap: 6px;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                        THÔNG TIN BẢO HÀNH & IMEI
                      </h4>
                      <p style="margin: 0; font-size: 13px; color: #1d1d1f; line-height: 1.4;">
                        Toàn bộ sản phẩm được <strong>bảo hành đổi trả trong 30 ngày</strong> đầu tiên nếu phát sinh lỗi từ nhà sản xuất. Bên cạnh đó, chế độ bảo hành độc quyền Peach Store cấp theo hạng thẻ của bạn là <strong>{{ selectedOrderDetail.warranty_months || 6 }} tháng</strong> kể từ ngày hoàn thành đơn hàng.
                      </p>
                    </div>
                    <div style="text-align: right; flex-shrink: 0; display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
                      <div v-if="selectedOrderDetail.imei" 
                           style="background: #ffffff; padding: 8px 16px; border-radius: 10px; border: 1.5px solid rgba(0, 122, 255, 0.2); font-family: 'SF Mono', Monaco, Consolas, monospace; font-size: 16px; font-weight: 700; color: #007aff; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(0, 122, 255, 0.05);"
                           @click="copyImeiToClipboard(selectedOrderDetail.imei)" title="Click để sao chép IMEI">
                        {{ selectedOrderDetail.imei }}
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                      </div>
                      <span v-else style="font-style: italic; color: #86868b; font-size: 13px;">Chưa cấp IMEI</span>
                      <span v-if="selectedOrderDetail.imei" style="font-size: 11px; font-weight: 700; color: #86868b; text-transform: uppercase;">Thời hạn: {{ selectedOrderDetail.warranty_months || 6 }} tháng</span>
                    </div>
                  </div>

                  <!-- Purchased Product List -->
                  <div>
                    <h4 style="margin: 0 0 12px 0; font-size: 13px; font-weight: 700; color: #86868b; text-transform: uppercase; letter-spacing: 0.5px; text-align: left;">Sản phẩm đã đặt</h4>
                    <div style="border: 1px solid #e8e8ed; border-radius: 16px; overflow: hidden;">
                      <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13.5px;">
                        <thead>
                          <tr style="background: #f5f5f7; border-bottom: 1px solid #e8e8ed;">
                            <th style="padding: 12px 16px; font-weight: 600; color: #1d1d1f;">Sản phẩm</th>
                            <th style="padding: 12px 16px; font-weight: 600; color: #1d1d1f; text-align: center;">Thông số</th>
                            <th style="padding: 12px 16px; font-weight: 600; color: #1d1d1f; text-align: center;">SL</th>
                            <th style="padding: 12px 16px; font-weight: 600; color: #1d1d1f; text-align: right;">Đơn giá</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="item in selectedOrderDetail.items" :key="item.id" style="border-bottom: 1px solid #f5f5f7;">
                            <td style="padding: 14px 16px;">
                              <div style="display: flex; align-items: center; gap: 10px;">
                                <img :src="getImageUrl(item.san_pham?.hinh_anh)" style="width: 36px; height: 36px; border-radius: 6px; object-fit: cover; border: 1px solid rgba(0,0,0,0.05);" />
                                <span style="font-weight: 600; color: #1d1d1f;">{{ item.san_pham?.ten }}</span>
                              </div>
                            </td>
                            <td style="padding: 14px 16px; text-align: center; color: #86868b;">
                              {{ item.dung_luong }} / {{ item.mau_sac }}
                            </td>
                            <td style="padding: 14px 16px; text-align: center; font-weight: 600; color: #1d1d1f;">
                              x{{ item.so_luong }}
                            </td>
                            <td style="padding: 14px 16px; text-align: right; font-weight: 600; color: #1d1d1f;">
                              {{ formatPrice(item.gia) }}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <!-- Pricing details (Fee, Discount, Grand Total) -->
                  <div style="display: flex; flex-direction: column; gap: 8px; align-self: flex-end; width: 280px; font-size: 13.5px; text-align: left; margin-left: auto;">
                    <div style="display: flex; justify-content: space-between; color: #86868b;">
                      <span>Tạm tính:</span>
                      <span style="font-weight: 600;">{{ formatPrice(selectedOrderDetail.tong_tien + selectedOrderDetail.giam_gia_voucher - selectedOrderDetail.phi_ship) }}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #ff3b30;" v-if="selectedOrderDetail.giam_gia_voucher > 0">
                      <span>Giảm giá Voucher:</span>
                      <span style="font-weight: 600;">-{{ formatPrice(selectedOrderDetail.giam_gia_voucher) }}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #86868b;">
                      <span>Phí vận chuyển:</span>
                      <span style="font-weight: 600;">+{{ formatPrice(selectedOrderDetail.phi_ship || 0) }}</span>
                    </div>
                    <div style="height: 1px; background: #e8e8ed; margin: 6px 0;"></div>
                    <div style="display: flex; justify-content: space-between; font-size: 16px; font-weight: 700; color: #1d1d1f;">
                      <span>Tổng cộng:</span>
                      <span style="color: #24b157; font-weight: bold;">{{ formatPrice(selectedOrderDetail.tong_tien) }}</span>
                    </div>
                  </div>

                </div>

                <!-- Modal Footer -->
                <div style="display: flex; justify-content: flex-end; gap: 12px; padding: 16px 24px; border-top: 1px solid #e8e8ed; background: #f5f5f7; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;">
                  <button @click="closeOrderDetail" class="modal-btn-cancel" style="background: #ffffff; color: #1d1d1f; border: 1px solid rgba(0,0,0,0.15); border-radius: 12px; height: 40px; font-size: 13.5px; font-weight: 600; padding: 0 20px; cursor: pointer; transition: all 0.2s;">
                    Đóng
                  </button>
                  <button @click="inHoaDonPDF(selectedOrderDetail)" style="background: #007aff; color: white; border: none; border-radius: 12px; height: 40px; font-size: 13.5px; font-weight: 600; padding: 0 24px; display: flex; align-items: center; gap: 8px; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 12px rgba(0, 122, 255, 0.25);">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
                    In hóa đơn (PDF)
                  </button>
                </div>

              </div>
            </div>
          </div>

          <!-- Tab: Mã giảm giá -->
          <div v-if="activeTab === 'vouchers'" class="settings-section">
            <h2 class="group-title">Mã giảm giá khả dụng</h2>
            
            <div v-if="loadingVouchers" class="loading-state">
              Đang tải mã giảm giá...
            </div>

            <div v-else-if="vouchers.length === 0" class="empty-state">
              <p>Hiện tại không có mã giảm giá nào khả dụng.</p>
            </div>

            <div v-else class="voucher-list">
              <div class="voucher-grid">
                <div v-for="v in vouchers" :key="v.id" class="voucher-item">
                  <div class="v-info">
                    <span class="v-tag">
                      {{ v.loai_giam_gia === 'phan_tram' ? `Giảm ${v.gia_tri_giam}%` : `Giảm ${formatPrice(v.gia_tri_giam)}` }}
                    </span>
                    <h3 style="font-weight: 700; color: #1d1d1f; margin-top: 12px;">{{ v.ma_voucher }}</h3>
                    <div style="display: flex; flex-direction: column; gap: 4px; margin-top: 8px;">
                      <p style="font-size: 13px; color: #1d1d1f; margin: 0;">Đơn hàng tối thiểu: <strong>{{ formatPrice(v.don_hang_toi_thieu) }}</strong></p>
                      <p v-if="v.giam_toi_da" style="font-size: 13px; color: #1d1d1f; margin: 0;">Giảm tối đa: <strong>{{ formatPrice(v.giam_toi_da) }}</strong></p>
                      <p style="font-size: 12px; color: #86868b; margin: 0;">Hạn sử dụng: <strong>{{ formatDate(v.ngay_het_han) }}</strong></p>
                      <p style="font-size: 12px; color: #86868b; margin: 0;">Số lượng còn lại: <strong>{{ v.so_luong_con_lai }} lượt</strong></p>
                    </div>
                  </div>
                  <button class="v-use" @click="copyToClipboard(v.ma_voucher)" style="background: #007aff; color: white; border: none; border-radius: 12px; font-weight: 600; padding: 10px 20px; transition: all 0.2s;">
                    Sao chép mã
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Tab: Sản phẩm yêu thích -->
          <div v-if="activeTab === 'wishlist'" class="settings-section">
            <h2 class="group-title">Sản phẩm yêu thích</h2>
            
            <div v-if="loadingWishlist" class="loading-state">
              Đang tải danh sách yêu thích...
            </div>

            <div v-else-if="wishlist.length === 0" class="empty-state">
              <p>Bạn chưa lưu sản phẩm nào vào danh sách yêu thích.</p>
              <router-link to="/" style="color: #007aff; text-decoration: none; font-weight: 500; font-size: 14px; margin-top: 10px; display: inline-block;">Khám phá các sản phẩm ngay →</router-link>
            </div>

            <div v-else class="wishlist-container">
              <div class="wishlist-grid">
                <div v-for="p in wishlist" :key="p.id" class="wishlist-item">
                  <img :src="getImageUrl(p.hinh_anh)" class="wishlist-img" alt="Product" />
                  <div class="wishlist-details">
                    <h3 class="wishlist-name">{{ p.ten }}</h3>
                    <p class="wishlist-price">{{ formatPrice(p.gia) }}</p>
                  </div>
                  <div class="wishlist-actions">
                    <router-link :to="`/san-pham/${p.id}`" class="wishlist-btn-view">
                      Xem chi tiết
                    </router-link>
                    <button class="wishlist-btn-delete" @click="removeWishlistItem(p.id)" title="Xóa khỏi yêu thích">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="trash-icon">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tab: Mật khẩu & Bảo mật -->
          <div v-if="activeTab === 'security'" class="settings-section">
            <div class="security-scroll-container">
              <h2 class="group-title" style="margin-top: 0;">Thay đổi mật khẩu</h2>
              <div class="settings-group">
                <div class="settings-table">
                  <div class="table-row">
                    <div class="table-label">Mật khẩu hiện tại</div>
                    <div class="table-value">
                      <div class="input-wrapper">
                        <input type="password" v-model="passwordForm.oldPassword" placeholder="Nhập mật khẩu hiện tại của bạn">
                      </div>
                    </div>
                  </div>

                  <div class="table-row">
                    <div class="table-label">Mật khẩu mới</div>
                    <div class="table-value">
                      <div class="input-wrapper">
                        <input type="password" v-model="passwordForm.newPassword" placeholder="Nhập mật khẩu mới (tối thiểu 6 ký tự)">
                      </div>
                    </div>
                  </div>

                  <div class="table-row">
                    <div class="table-label">Xác nhận mật khẩu mới</div>
                    <div class="table-value">
                      <div class="input-wrapper">
                        <input type="password" v-model="passwordForm.confirmPassword" placeholder="Xác nhận lại mật khẩu mới">
                      </div>
                    </div>
                  </div>
                </div>

                <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
                  <button 
                    @click="changePassword" 
                    :disabled="submittingPassword || !passwordForm.oldPassword || !passwordForm.newPassword || !passwordForm.confirmPassword"
                    :style="{ 
                      background: (submittingPassword || !passwordForm.oldPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) ? '#86868b' : '#007aff',
                      color: 'white',
                      border: 'none',
                      borderRadius: '12px',
                      fontWeight: '600',
                      padding: '10px 24px',
                      cursor: (submittingPassword || !passwordForm.oldPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) ? 'not-allowed' : 'pointer',
                      opacity: (submittingPassword || !passwordForm.oldPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) ? '0.5' : '1',
                      transition: 'all 0.2s',
                      fontSize: '14px'
                    }"
                  >
                    {{ submittingPassword ? 'Đang cập nhật...' : 'Cập nhật mật khẩu' }}
                  </button>
                </div>
              </div>

              <h2 class="group-title" style="margin-top: 40px;">Bảo mật giao dịch (Mã PIN)</h2>
              <div class="settings-group">
                <p style="font-size: 14px; color: #86868b; line-height: 1.6; margin-bottom: 20px;">
                  Mã PIN giao dịch (4-6 chữ số) giúp tăng cường bảo mật tối đa cho tài khoản của bạn. Khi được bật, hệ thống sẽ hiển thị bảng xác minh mã PIN trước khi cho phép đặt bất kỳ đơn hàng nào.
                </p>

                <div class="settings-table">
                  <div class="table-row">
                    <div class="table-label">Trạng thái mã PIN</div>
                    <div class="table-value">
                      <div style="display: flex; align-items: center; justify-content: space-between;">
                        <span :style="{ color: user.co_pin ? '#34c759' : '#ff3b30', fontWeight: '600', fontSize: '14px' }">
                          {{ user.co_pin ? '✓ Đã thiết lập mã PIN' : '✗ Chưa thiết lập mã PIN' }}
                        </span>
                        <button 
                          @click="openPinSetup" 
                          style="background: #f5f5f7; color: #007aff; border: none; border-radius: 10px; font-weight: 600; padding: 8px 16px; cursor: pointer; transition: all 0.2s; font-size: 13px;"
                        >
                          {{ user.co_pin ? 'Thay đổi mã PIN' : 'Thiết lập mã PIN' }}
                        </button>
                      </div>
                    </div>
                  </div>

                  <div class="table-row" v-if="user.co_pin">
                    <div class="table-label">Yêu cầu PIN khi mua hàng</div>
                    <div class="table-value">
                      <div style="display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-size: 14px; color: #1d1d1f;">
                          {{ user.yeu_cau_pin ? 'Đang bật (Yêu cầu nhập mã PIN khi đặt hàng)' : 'Đang tắt (Đặt hàng không cần mã PIN)' }}
                        </span>
                        <label class="apple-switch">
                          <input type="checkbox" :checked="user.yeu_cau_pin" @change="togglePinRequirement">
                          <span class="slider"></span>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tab: Gửi hỗ trợ -->
          <div v-if="activeTab === 'reviews'" class="settings-section">
            <h2 class="group-title">Gửi hỗ trợ mới</h2>
            <p style="font-size: 14px; color: #86868b; margin-top: -20px; margin-bottom: 30px;">
              Chúng tôi luôn sẵn sàng hỗ trợ bạn 24/7. Hãy gửi yêu cầu hỗ trợ để được đội ngũ Peach phản hồi sớm nhất.
            </p>

            <div class="settings-table">
              <div class="table-row">
                <div class="table-label">Chủ đề hỗ trợ</div>
                <div class="table-value">
                  <div class="input-wrapper">
                    <input type="text" v-model="supportForm.subject" placeholder="VD: Lỗi thanh toán, Cần bảo hành sản phẩm, ...">
                  </div>
                </div>
              </div>

              <div class="table-row">
                <div class="table-label">Số Serial hoặc IMEI (nếu có)</div>
                <div class="table-value">
                  <div class="input-wrapper">
                    <input type="text" v-model="supportForm.serial" placeholder="Nhập mã Serial hoặc IMEI của máy để kiểm tra nhanh">
                  </div>
                </div>
              </div>

              <div class="table-row">
                <div class="table-label">Nội dung chi tiết</div>
                <div class="table-value">
                  <div class="input-wrapper">
                    <textarea v-model="supportForm.message" placeholder="Hãy mô tả chi tiết vấn đề bạn đang gặp phải hoặc thông tin cần giải đáp..." style="height: 120px;"></textarea>
                  </div>
                </div>
              </div>

              <div class="table-row">
                <div class="table-label">Đính kèm hình ảnh</div>
                <div class="table-value">
                  <div style="display: flex; flex-direction: column; gap: 8px;">
                    <!-- Image Selection Grid -->
                    <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center;">
                      <!-- Preview items -->
                      <div v-for="(img, idx) in supportImages" :key="idx" style="position: relative; width: 70px; height: 70px; border-radius: 12px; border: 1px solid rgba(0,0,0,0.1); overflow: hidden; background: #f5f5f7;">
                        <img :src="img.preview" style="width: 100%; height: 100%; object-fit: cover;" />
                        <button type="button" @click="removeSupportImage(idx)" style="position: absolute; top: 4px; right: 4px; background: rgba(0,0,0,0.5); color: white; border: none; border-radius: 50%; width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 10px; font-weight: bold; line-height: 1;">×</button>
                      </div>

                      <!-- Add button (renders if less than 5 images selected) -->
                      <div v-if="supportImages.length < 5" @click="triggerSupportImageSelect" style="width: 70px; height: 70px; border-radius: 12px; border: 1.5px dashed rgba(0,0,0,0.15); display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; background: rgba(255,255,255,0.6);" onmouseover="this.style.borderColor='#007aff'; this.style.background='rgba(0,122,255,0.03)'" onmouseout="this.style.borderColor='rgba(0,0,0,0.15)'; this.style.background='rgba(255,255,255,0.6)'">
                        <span style="font-size: 20px; color: #86868b; font-weight: 300;">+</span>
                        <span style="font-size: 9px; color: #86868b; font-weight: 500;">Thêm ảnh</span>
                      </div>
                    </div>

                    <!-- Hidden Input File -->
                    <input type="file" ref="supportImageInput" multiple accept="image/*" class="hidden-input" @change="handleSupportImagesChange" style="display: none;" />
                    
                    <span style="font-size: 11px; color: #86868b;">Đính kèm tối đa 5 ảnh. Dung lượng tối đa 10MB/ảnh.</span>
                  </div>
                </div>
              </div>
            </div>

            <div style="margin-top: 30px; display: flex; justify-content: flex-end;">
              <button 
                @click="submitSupport" 
                :disabled="submittingSupport || !supportForm.subject || !supportForm.message"
                :style="{ 
                  background: (submittingSupport || !supportForm.subject || !supportForm.message) ? '#86868b' : '#007aff',
                  color: 'white',
                  border: 'none',
                  borderRadius: '12px',
                  fontWeight: '600',
                  padding: '12px 28px',
                  cursor: (submittingSupport || !supportForm.subject || !supportForm.message) ? 'not-allowed' : 'pointer',
                  opacity: (submittingSupport || !supportForm.subject || !supportForm.message) ? '0.5' : '1',
                  transition: 'all 0.2s',
                  fontSize: '14px'
                }"
              >
                {{ submittingSupport ? 'Đang gửi yêu cầu...' : 'Gửi yêu cầu hỗ trợ' }}
              </button>
            </div>
          </div>

          <!-- Tab: Chat với Admin -->
          <div v-if="activeTab === 'chat'" class="settings-section" style="display: flex; flex-direction: column; height: 520px; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(0,0,0,0.08); border-radius: 20px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,0,0,0.06); padding-bottom: 16px; margin-bottom: 16px;">
              <div>
                <h2 class="group-title" style="margin: 0; font-size: 20px; font-weight: 700; color: #1d1d1f; letter-spacing: -0.5px;">Chat với Admin</h2>
                <div style="display: flex; align-items: center; gap: 6px; margin-top: 4px;">
                  <span style="width: 8px; height: 8px; border-radius: 50%; background-color: #30d158; display: inline-block; box-shadow: 0 0 8px #30d158;"></span>
                  <span style="font-size: 12px; color: #86868b; font-weight: 500;">Hỗ trợ trực tuyến (Chỉ hiển thị tối đa 10 tin nhắn gần nhất)</span>
                </div>
              </div>
              <div style="background: rgba(0, 122, 255, 0.08); color: #007aff; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; text-transform: uppercase;">
                Đội ngũ Peach Store
              </div>
            </div>

            <!-- Chat Messages Container -->
            <div ref="chatContainer" class="chat-messages-container" style="flex: 1; overflow-y: auto; padding: 10px 4px; display: flex; flex-direction: column; gap: 14px; margin-bottom: 16px;">
              <!-- Loading state -->
              <div v-if="loadingChat" style="display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1; gap: 8px;">
                <div style="width: 20px; height: 20px; border: 2px solid rgba(0,122,255,0.15); border-top-color: #007aff; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <span style="font-size: 12px; color: #86868b;">Đang tải tin nhắn...</span>
              </div>
              
              <!-- Empty state -->
              <div v-else-if="allMessages.length === 0" style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0.8; gap: 10px; padding: 40px 0;">
                <span style="font-size: 32px;">💬</span>
                <span style="font-size: 13px; color: #86868b; font-weight: 500; text-align: center;">Chưa có tin nhắn nào. Bắt đầu trò chuyện với Admin!</span>
              </div>

              <!-- Message log -->
              <template v-else>
                <!-- Xem tin cũ hơn -->
                <div v-if="showLoadPrevious" @click="loadPreviousMessages" style="align-self: center; background: rgba(0, 122, 255, 0.08); color: #007aff; border: none; border-radius: 12px; font-weight: 600; padding: 6px 14px; cursor: pointer; transition: all 0.2s; font-size: 11.5px; display: flex; align-items: center; gap: 6px; margin-bottom: 8px; user-select: none;" title="Xem tin cũ hơn">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="18 15 12 9 6 15"></polyline></svg>
                  Xem 10 tin cũ hơn (còn {{ visibleStartIdx }} tin)
                </div>

                <div v-for="msg in renderedMessages" :key="msg.id" :style="{ alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start' }" style="max-width: 75%; display: flex; flex-direction: column;">
                  <div :style="{ 
                    backgroundColor: msg.sender === 'user' ? '#007aff' : '#f5f5f7',
                    color: msg.sender === 'user' ? '#ffffff' : '#1d1d1f',
                    borderRadius: msg.sender === 'user' ? '18px 18px 2px 18px' : '18px 18px 18px 2px',
                    padding: '10px 16px',
                    fontSize: '14px',
                    lineHeight: '1.45',
                    boxShadow: msg.sender === 'user' ? '0 4px 12px rgba(0,122,255,0.2)' : 'none',
                    border: msg.sender === 'user' ? 'none' : '1px solid rgba(0,0,0,0.02)'
                  }">
                    {{ msg.text }}
                  </div>
                  <span :style="{ alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start' }" style="font-size: 10px; color: #86868b; margin-top: 4px; margin-left: 4px; margin-right: 4px; font-weight: 500;">
                    {{ msg.time }}
                  </span>
                </div>

                <!-- Xem tin mới hơn -->
                <div v-if="showLoadNext" @click="loadNextMessages" style="align-self: center; background: rgba(0, 122, 255, 0.08); color: #007aff; border: none; border-radius: 12px; font-weight: 600; padding: 6px 14px; cursor: pointer; transition: all 0.2s; font-size: 11.5px; display: flex; align-items: center; gap: 6px; margin-top: 8px; user-select: none;" title="Xem tin mới hơn">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="6 9 12 15 18 9"></polyline></svg>
                  Xem 10 tin mới hơn (còn {{ allMessages.length - 10 - visibleStartIdx }} tin)
                </div>
              </template>
            </div>

            <!-- Chat Input Area -->
            <div style="display: flex; gap: 10px; align-items: center; background: #f5f5f7; padding: 6px 12px; border-radius: 20px; border: 1.5px solid rgba(0,0,0,0.02); transition: all 0.2s;">
              <input 
                type="text" 
                v-model="newMsgText" 
                @keyup.enter="sendMessage" 
                placeholder="Nhập tin nhắn của bạn với Admin..." 
                style="flex: 1; background: transparent; border: none; outline: none; font-size: 14px; color: #1d1d1f; padding: 8px 4px;"
              />
              <button 
                @click="sendMessage" 
                :disabled="!newMsgText.trim() || loadingChat"
                :style="{ 
                  backgroundColor: newMsgText.trim() ? '#007aff' : 'transparent',
                  color: newMsgText.trim() ? '#ffffff' : '#86868b',
                  cursor: newMsgText.trim() ? 'pointer' : 'not-allowed',
                  transform: newMsgText.trim() ? 'scale(1.05)' : 'scale(1)'
                }"
                style="border: none; border-radius: 50%; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
              </button>
            </div>
          </div>

          <!-- Tab: Lịch sử đăng nhập -->
          <div v-if="activeTab === 'devices'" class="settings-section">
            <h2 class="group-title">Lịch sử đăng nhập</h2>
            <p style="font-size: 14px; color: #86868b; margin-top: -20px; margin-bottom: 24px; line-height: 1.5;">
               Dưới đây là danh sách các thiết bị và phiên đăng nhập thực tế gần đây của bạn. Nếu bạn phát hiện thiết bị lạ đăng nhập, vui lòng đổi mật khẩu ngay lập tức.
            </p>

            <div class="devices-scroll-container">
               <!-- Loading State -->
               <div v-if="loadingHistory" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 0; gap: 12px;">
                  <div style="width: 24px; height: 24px; border: 2.5px solid rgba(0,122,255,0.15); border-top-color: #007aff; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                  <span style="font-size: 13px; color: #86868b;">Đang tải lịch sử đăng nhập thực tế...</span>
               </div>

               <!-- Empty State -->
               <div v-else-if="loginHistory.length === 0" style="text-align: center; padding: 40px 20px; background: #ffffff; border: 1px solid #e5e5e7; border-radius: 16px;">
                  <div style="font-size: 40px; margin-bottom: 12px;">🔒</div>
                  <h4 style="font-size: 15px; font-weight: 600; color: #1d1d1f; margin-bottom: 6px;">Không tìm thấy lịch sử</h4>
                  <p style="font-size: 13px; color: #86868b; margin: 0;">Chưa ghi nhận phiên đăng nhập nào trên hệ thống.</p>
               </div>

               <!-- Active & Past Sessions Dynamic Grid -->
               <div v-else class="device-list-grid">
                  <div v-for="(item, index) in loginHistory" :key="item.id" 
                       class="device-item" :class="{ active: index === 0 }">
                     <div class="device-icon-wrapper" :class="{ active: index === 0 }">
                        <!-- Desktop / Laptop / PC SVG -->
                        <svg v-if="item.thiet_bi.toLowerCase().includes('windows') || item.thiet_bi.toLowerCase().includes('mac') || item.thiet_bi.toLowerCase().includes('pc')"
                             viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="device-icon">
                           <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                           <line x1="8" y1="21" x2="16" y2="21"></line>
                           <line x1="12" y1="17" x2="12" y2="21"></line>
                        </svg>
                        <!-- Tablet SVG -->
                        <svg v-else-if="item.thiet_bi.toLowerCase().includes('ipad')"
                             viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="device-icon">
                           <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
                           <line x1="12" y1="18" x2="12.01" y2="18"></line>
                        </svg>
                        <!-- Phone SVG -->
                        <svg v-else
                             viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="device-icon">
                           <rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect>
                           <line x1="12" y1="18" x2="12.01" y2="18"></line>
                        </svg>
                     </div>
                     <div class="device-info">
                        <div class="device-meta">
                           <h4 class="device-name">{{ item.thiet_bi }}</h4>
                           <span v-if="index === 0" class="device-badge-active">Đang hoạt động</span>
                        </div>
                        <div class="device-details">
                           <span><strong>Địa chỉ IP:</strong> {{ item.ip_address }}</span>
                           <span><strong>Vị trí:</strong> {{ item.vi_tri }}</span>
                           <span>
                              <strong>Thời gian đăng nhập:</strong> 
                              {{ index === 0 ? 'Hoạt động ngay bây giờ (Phiên hiện tại)' : formatLoginTime(item.ngay_dang_nhap) }}
                           </span>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
          </div>

          <!-- Tab: Thông báo -->
          <div v-if="activeTab === 'notifications'" class="settings-section">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
              <h2 class="group-title" style="margin-bottom: 0;">Thông báo của bạn</h2>
              <button v-if="userNotifications.length > 0" @click="markAllAsRead" 
                      style="background: rgba(0, 122, 255, 0.08); color: #007aff; border: none; border-radius: 12px; font-size: 13px; font-weight: 600; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);"
                      onmouseover="this.style.background='rgba(0,122,255,0.14)';"
                      onmouseout="this.style.background='rgba(0, 122, 255, 0.08)';"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                Đã đọc tất cả
              </button>
            </div>
            <p style="font-size: 14px; color: #86868b; margin-top: -12px; margin-bottom: 24px; line-height: 1.5;">
              Nhận thông báo cập nhật, ưu đãi và tin tức quan trọng mới nhất từ hệ thống Peach Store.
            </p>

            <div class="notifications-scroll-container" style="max-height: 550px; overflow-y: auto; padding-right: 6px;">
               <!-- Loading State -->
               <div v-if="loadingNotifications" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 0; gap: 12px;">
                  <div style="width: 24px; height: 24px; border: 2.5px solid rgba(0,122,255,0.15); border-top-color: #007aff; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                  <span style="font-size: 13px; color: #86868b;">Đang tải thông báo...</span>
               </div>

               <!-- Empty State -->
               <div v-else-if="userNotifications.length === 0" style="text-align: center; padding: 50px 20px; background: #ffffff; border: 1px solid #e5e5e7; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.01);">
                  <div style="font-size: 44px; margin-bottom: 16px; animation: bounce 2s infinite;">🔔</div>
                  <h4 style="font-size: 16px; font-weight: 600; color: #1d1d1f; margin-bottom: 6px;">Không có thông báo mới</h4>
                  <p style="font-size: 13px; color: #86868b; margin: 0;">Bạn đã đọc hết hoặc chưa có thông báo mới nào tại đây.</p>
               </div>

               <!-- Notifications List -->
               <div v-else style="display: flex; flex-direction: column; gap: 16px;">
                  <div v-for="n in userNotifications" :key="n.id" 
                       style="background: #ffffff; border: 1px solid rgba(0,0,0,0.06); border-radius: 16px; padding: 20px; display: flex; gap: 16px; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: 0 4px 12px rgba(0,0,0,0.01);"
                       onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px rgba(0,0,0,0.04)'; this.style.borderColor='rgba(0,122,255,0.15)';"
                       onmouseout="this.style.transform='none'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.01)'; this.style.borderColor='rgba(0,0,0,0.06)';"
                  >
                     <div style="width: 44px; height: 44px; background: rgba(0, 122, 255, 0.08); border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                           <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                           <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                        </svg>
                     </div>
                     <div style="flex: 1; display: flex; flex-direction: column; gap: 6px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
                           <h4 style="font-size: 15.5px; font-weight: 700; color: #1d1d1f; margin: 0; line-height: 1.3;">{{ n.title }}</h4>
                           <div style="display: flex; align-items: center; gap: 10px;">
                              <span style="font-size: 11.5px; color: #86868b; white-space: nowrap; font-weight: 500;">{{ n.sent }}</span>
                              <button @click="markAsRead(n.id)" title="Đánh dấu đã đọc và ẩn" 
                                      style="background: none; border: none; padding: 4px; border-radius: 6px; cursor: pointer; color: #86868b; display: flex; align-items: center; justify-content: center; transition: all 0.2s;"
                                      onmouseover="this.style.color='#007aff'; this.style.background='rgba(0,122,255,0.08)';"
                                      onmouseout="this.style.color='#86868b'; this.style.background='none';"
                              >
                                 <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                 </svg>
                              </button>
                           </div>
                        </div>
                        <p style="font-size: 13.5px; color: #48484a; margin: 0; line-height: 1.45; white-space: pre-line;">{{ n.body }}</p>
                        
                        <!-- Premium Badge for segment targets -->
                        <div style="display: flex; gap: 8px; margin-top: 4px;">
                           <span style="font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 6px; background: #f5f5f7; color: #86868b;">
                              Target: {{ n.target }}
                           </span>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- PIN Setup Modal (macOS Style) -->
    <div class="apple-modal-overlay" v-if="showPinSetupModal">
      <div class="apple-modal-card">
        <div class="modal-icon-container blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="modal-icon">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>
        <h3 class="modal-title">{{ user.co_pin ? 'Thay đổi mã PIN giao dịch' : 'Thiết lập mã PIN giao dịch' }}</h3>
        <p class="modal-desc">Vui lòng nhập mã PIN mới (4-6 chữ số) và mật khẩu tài khoản để xác thực.</p>
        
        <div class="modal-form">
          <div class="modal-input-group">
            <label>Mã PIN mới (4-6 chữ số)</label>
            <input 
              type="password" 
              v-model="pinForm.pin_moi" 
              placeholder="VD: 1234" 
              maxlength="6"
              class="modal-input-field"
            />
          </div>
          <div class="modal-input-group">
            <label>Mật khẩu tài khoản</label>
            <input 
              type="password" 
              v-model="pinForm.mat_khau_xac_nhan" 
              placeholder="Nhập mật khẩu để xác nhận" 
              class="modal-input-field"
            />
          </div>
        </div>

        <div class="modal-actions-row">
          <button class="modal-btn-secondary" @click="closePinSetup">Hủy bỏ</button>
          <button 
            class="modal-btn-primary" 
            @click="submitPinSetup" 
            :disabled="!pinForm.pin_moi || !pinForm.mat_khau_xac_nhan"
          >
            Xác nhận
          </button>
        </div>
      </div>
    </div>

    <!-- PIN Verification Modal for Toggle (macOS Style) -->
    <div class="apple-modal-overlay" v-if="showPinVerifyModal">
      <div class="apple-modal-card">
        <div class="modal-icon-container red">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="modal-icon">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>
        <h3 class="modal-title">Xác thực mã PIN</h3>
        <p class="modal-desc">Vui lòng nhập mã PIN hiện tại của bạn để thay đổi cấu hình bảo mật.</p>
        
        <div class="modal-form">
          <div class="modal-input-group">
            <input 
              type="password" 
              v-model="pinVerifyValue" 
              placeholder="Nhập 4-6 chữ số mã PIN" 
              maxlength="6"
              style="text-align: center; font-size: 24px; letter-spacing: 6px;"
              class="modal-input-field"
              autofocus
            />
          </div>
        </div>

        <div class="modal-actions-row">
          <button class="modal-btn-secondary" @click="closePinVerify">Hủy bỏ</button>
          <button 
            class="modal-btn-primary" 
            @click="submitPinVerify" 
            :disabled="!pinVerifyValue"
          >
            Xác nhận
          </button>
        </div>
      </div>
    </div>

    <!-- Loyalty Rank & Points Details Modal (macOS Premium Style) -->
    <div class="apple-modal-overlay" v-if="showLoyaltyDetailsModal" style="z-index: 9999;">
      <div class="apple-modal-card" style="max-width: 480px; width: 90%; padding: 28px; border-radius: 24px; text-align: left;">
        
        <!-- Header -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div class="modal-icon-container blue" style="margin: 0; width: 42px; height: 42px; display: flex; align-items: center; justify-content: center; border-radius: 12px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="modal-icon" style="width: 22px; height: 22px;">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
            </div>
            <div>
              <h3 class="modal-title" style="margin: 0; text-align: left; font-size: 18px; font-weight: 700; color: #1d1d1f;">Quyền Lợi Hạng Thẻ</h3>
              <p class="modal-desc" style="margin: 2px 0 0 0; text-align: left; font-size: 13px; color: #86868b;">Chi tiết tích điểm & lộ trình thăng hạng</p>
            </div>
          </div>
          <button @click="showLoyaltyDetailsModal = false" style="background: #f5f5f7; border: none; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #86868b; transition: all 0.2s;" onmouseover="this.style.background='#e8e8ed'" onmouseout="this.style.background='#f5f5f7'">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>

        <!-- Scrollable Modal Body -->
        <div style="max-height: 420px; overflow-y: auto; padding-right: 6px; display: flex; flex-direction: column; gap: 20px;">
          
          <!-- Customer Digital Membership Card -->
          <div :style="{
            background: getRankBg(user),
            color: '#ffffff',
            borderRadius: '20px',
            padding: '24px',
            boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
            position: 'relative',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            height: '180px'
          }">
            <!-- Card Chips background effect -->
            <div style="position: absolute; right: -20px; bottom: -20px; opacity: 0.12; pointer-events: none;">
              <svg width="180" height="180" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: flex-start; z-index: 1;">
              <div>
                <p style="margin: 0; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.8;">THỂ THÀNH VIÊN</p>
                <h4 style="margin: 4px 0 0 0; font-size: 24px; font-weight: 800; letter-spacing: 0.5px;">{{ getMembershipRank(user) === 'Chưa có hạng' ? 'Chưa có Hạng' : 'Hạng ' + getMembershipRank(user) }}</h4>
              </div>
              <div style="background: rgba(255,255,255,0.22); backdrop-filter: blur(10px); padding: 5px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;">
                Ưu đãi giảm {{ getRankDiscount(user) }}%
              </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: flex-end; z-index: 1;">
              <div>
                <p style="margin: 0; font-size: 11px; opacity: 0.8; font-weight: 500;">Chủ sở hữu</p>
                <p style="margin: 2px 0 0 0; font-size: 15px; font-weight: 700;">{{ user.ho_ten }}</p>
              </div>
              <div style="text-align: right;">
                <p style="margin: 0; font-size: 11px; opacity: 0.8; font-weight: 500;">Điểm tích lũy</p>
                <p style="margin: 0; font-size: 22px; font-weight: 800; letter-spacing: 0.5px;">{{ user.diem_tich_luy || 0 }} <span style="font-size: 13px; font-weight: 500;">điểm</span></p>
              </div>
            </div>
          </div>

          <!-- Banner hướng dẫn thăng hạng khi Chưa Có Hạng -->
          <div v-if="getMembershipRank(user) === 'Chưa có hạng'" style="background: #fff8e1; border-radius: 16px; padding: 18px; display: flex; align-items: flex-start; gap: 12px; border: 1px solid rgba(255, 149, 0, 0.2); margin-top: 4px;">
            <div style="background: rgba(255, 149, 0, 0.1); color: #ff9500; padding: 6px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="display: block;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            </div>
            <div>
              <h5 style="margin: 0; font-size: 13px; font-weight: 700; color: #b78103; text-align: left;">Bạn chưa được phân hạng thành viên</h5>
              <p style="margin: 4px 0 0 0; font-size: 12px; color: #6d4c00; line-height: 1.4; text-align: left;">Hãy hoàn thành các đơn hàng mua sắm để tích điểm. Khi đạt tối thiểu <strong>{{ getNextRankInfo(user)?.targetPoints || 100 }} điểm</strong>, bạn sẽ được tự động kích hoạt hạng thẻ đầu tiên <strong>{{ getNextRankInfo(user)?.nextRankName || 'Bạc' }}</strong> với ngập tràn đặc quyền ưu đãi!</p>
            </div>
          </div>

          <!-- Progress Bar to Next Rank -->
          <div v-if="getNextRankInfo(user)" style="background: #f5f5f7; border-radius: 16px; padding: 18px; border: 1px solid rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-size: 13px; font-weight: 600; color: #1d1d1f;">Tiến trình lên hạng kế tiếp</span>
              <span style="font-size: 13px; font-weight: 700; color: #007aff;">Cần tích thêm {{ getNextRankInfo(user).pointsNeeded }} điểm</span>
            </div>
            
            <!-- Progress Track -->
            <div style="background: rgba(0,0,0,0.06); height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 8px;">
              <div :style="{ width: getNextRankInfo(user).percent + '%' }" style="background: #007aff; height: 100%; border-radius: 4px; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);"></div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-weight: 600; color: #86868b;">
              <span>Hạng hiện tại: {{ getMembershipRank(user) }}</span>
              <span>Lên hạng {{ getNextRankInfo(user).nextRankName }} ({{ getNextRankInfo(user).targetPoints }} điểm)</span>
            </div>
          </div>
          
          <div v-else style="background: #e8f9ee; border-radius: 16px; padding: 16px; display: flex; align-items: center; gap: 10px; border: 1px solid rgba(36, 177, 87, 0.15);">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#24b157" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <span style="font-size: 13.5px; font-weight: 600; color: #1a7f3e;">Chúc mừng! Bạn đã đạt hạng thẻ cao nhất <strong>Kim cương</strong>! 🎉</span>
          </div>

          <!-- Privileges of Current Tier -->
          <div>
            <h4 style="font-size: 13px; font-weight: 700; color: #86868b; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 0.5px;">Đặc quyền của bạn</h4>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              <div v-for="benefit in getRankBenefits(user)" :key="benefit" style="display: flex; align-items: center; gap: 10px; font-size: 13.5px; color: #1d1d1f; font-weight: 500;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#24b157" stroke-width="3" style="flex-shrink: 0;">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>{{ benefit }}</span>
              </div>
            </div>
          </div>

          <!-- How to Earn Points Section -->
          <div>
            <h4 style="font-size: 13px; font-weight: 700; color: #86868b; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 0.5px;">Làm sao để tích thêm điểm?</h4>
            <div style="background: #f5f5f7; border-radius: 16px; padding: 18px; display: flex; flex-direction: column; gap: 16px; border: 1px solid rgba(0,0,0,0.03);">
              
              <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="background: rgba(0, 122, 255, 0.08); color: #007aff; padding: 6px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg>
                </div>
                <div>
                  <h5 style="margin: 0; font-size: 13px; font-weight: 700; color: #1d1d1f;">Mua sắm tích điểm tự động</h5>
                  <p style="margin: 3px 0 0 0; font-size: 12px; color: #86868b; line-height: 1.4;">Với mỗi **10,000đ** thanh toán đơn hàng thành công, tài khoản bạn sẽ được tự động cộng **1 điểm** tích lũy.</p>
                </div>
              </div>

              <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="background: rgba(255, 149, 0, 0.08); color: #ff9500; padding: 6px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                </div>
                <div>
                  <h5 style="margin: 0; font-size: 13px; font-weight: 700; color: #1d1d1f;">Điểm tích lũy trọn đời</h5>
                  <p style="margin: 3px 0 0 0; font-size: 12px; color: #86868b; line-height: 1.4;">Không giới hạn thời gian! Điểm tích lũy được bảo lưu trọn đời và **không bao giờ hết hạn**.</p>
                </div>
              </div>

              <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="background: rgba(36, 177, 87, 0.08); color: #24b157; padding: 6px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                </div>
                <div>
                  <h5 style="margin: 0; font-size: 13px; font-weight: 700; color: #1d1d1f;">Tự động thăng hạng</h5>
                  <p style="margin: 3px 0 0 0; font-size: 12px; color: #86868b; line-height: 1.4;">Hệ thống tự động quét và nâng hạng thẻ ngay lập tức khi bạn tích lũy đủ điểm tối thiểu. Hạng thẻ mới và mức chiết khấu sẽ tự động áp dụng ngay cho đơn hàng sau.</p>
                </div>
              </div>

            </div>
          </div>

        </div>

        <!-- Footer -->
        <div style="margin-top: 24px; border-top: 1px solid #e8e8ed; padding-top: 16px; display: flex; justify-content: flex-end;">
          <button @click="showLoyaltyDetailsModal = false" class="modal-btn-primary" style="margin: 0; min-width: 100px; border-radius: 12px; height: 38px; font-size: 13px; font-weight: 600;">Đã hiểu</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useNotificationStore } from '../stores/notification'
import { xacThucApi, gioHangApi, donHangApi, voucherApi, yeuThichApi } from '../services/api'
import axios from 'axios' // Vẫn cần cho upload avatar vì cần FormData config đặc biệt nếu ko dùng method có sẵn

const router = useRouter()
const route = useRoute()
const notification = useNotificationStore()
const activeTab = ref('profile')
const showMobileMenu = ref(false)
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const setActiveTab = (tabId) => {
  activeTab.value = tabId
  router.replace({ query: { ...route.query, tab: tabId } })
  showMobileMenu.value = false // Tự động đóng menu trên mobile khi chọn chức năng
}
const saving = ref(false)
const avatarInput = ref(null)

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const submittingPassword = ref(false)

const showPinSetupModal = ref(false)
const pinForm = ref({
  pin_moi: '',
  mat_khau_xac_nhan: ''
})

const showPinVerifyModal = ref(false)
const pinVerifyValue = ref('')
const pinVerifyTargetState = ref(false)

const changePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    notification.error('Mật khẩu xác nhận không trùng khớp!')
    return
  }
  if (passwordForm.value.newPassword.length < 6) {
    notification.error('Mật khẩu mới phải từ 6 ký tự trở lên!')
    return
  }

  submittingPassword.value = true
  try {
    await xacThucApi.doiMatKhau({
      mat_khau_cu: passwordForm.value.oldPassword,
      mat_khau_moi: passwordForm.value.newPassword
    })
    notification.show('Đổi mật khẩu thành công!', 'success')
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    console.error('Lỗi khi đổi mật khẩu:', error)
    notification.error(error.response?.data?.detail || 'Không thể đổi mật khẩu. Vui lòng thử lại.')
  } finally {
    submittingPassword.value = false
  }
}

const openPinSetup = () => {
  pinForm.value = {
    pin_moi: '',
    mat_khau_xac_nhan: ''
  }
  showPinSetupModal.value = true
}

const closePinSetup = () => {
  showPinSetupModal.value = false
}

const submitPinSetup = async () => {
  const pin = pinForm.value.pin_moi
  if (!/^\d{4,6}$/.test(pin)) {
    notification.error('Mã PIN phải chứa từ 4 đến 6 chữ số!')
    return
  }

  try {
    const res = await xacThucApi.caiDatPin({
      pin_moi: pin,
      mat_khau_xac_nhan: pinForm.value.mat_khau_xac_nhan
    })
    notification.show(res.data.message || 'Thiết lập mã PIN thành công!', 'success')
    user.value.co_pin = true
    
    // Đồng bộ lại localstorage
    const localProfile = JSON.parse(localStorage.getItem('user_profile') || '{}')
    localProfile.co_pin = true
    localStorage.setItem('user_profile', JSON.stringify(localProfile))
    
    showPinSetupModal.value = false
  } catch (error) {
    console.error('Lỗi thiết lập mã PIN:', error)
    notification.error(error.response?.data?.detail || 'Không thể thiết lập mã PIN. Vui lòng thử lại.')
  }
}

const togglePinRequirement = (event) => {
  // Ngăn chặn checkbox tự đổi trạng thái, phải nhập mã PIN thành công mới đổi
  event.preventDefault()
  
  pinVerifyTargetState.value = !user.value.yeu_cau_pin
  pinVerifyValue.value = ''
  showPinVerifyModal.value = true
}

const closePinVerify = () => {
  showPinVerifyModal.value = false
}

const submitPinVerify = async () => {
  try {
    const res = await xacThucApi.togglePin({
      kich_hoat: pinVerifyTargetState.value,
      ma_pin: pinVerifyValue.value
    })
    
    notification.show(res.data.message, 'success')
    user.value.yeu_cau_pin = res.data.yeu_cau_pin
    
    // Đồng bộ lại localstorage
    const localProfile = JSON.parse(localStorage.getItem('user_profile') || '{}')
    localProfile.yeu_cau_pin = res.data.yeu_cau_pin
    localStorage.setItem('user_profile', JSON.stringify(localProfile))
    
    showPinVerifyModal.value = false
  } catch (error) {
    console.error('Lỗi khi đổi cài đặt mã PIN:', error)
    notification.error(error.response?.data?.detail || 'Xác minh mã PIN thất bại!')
  }
}

const loyaltyLevels = ref([])

const fetchLoyaltyLevels = async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}/api/admin/loyalty-configs`)
    if (res.ok) {
      loyaltyLevels.value = await res.json()
    }
  } catch (error) {
    console.error('Lỗi khi lấy cấu hình loyalty:', error)
  }
}

const user = ref({
  ho_ten: '',
  email: '',
  so_dien_thoai: '',
  dia_chi: ''
})

const businessForm = ref({
  ten_doanh_nghiep: '',
  ma_so_thue: '',
  dia_chi_kd: '',
  linh_vuc_kd: ''
})
const submittingBusiness = ref(false)

const businessRequest = ref({
  has_request: false,
  trang_thai: null,
  ten_doanh_nghiep: '',
  ma_so_thue: '',
  dia_chi_kd: '',
  linh_vuc_kd: ''
})

const fetchBusinessRequestStatus = async () => {
  try {
    const res = await xacThucApi.getTrangThaiDoanhNghiep()
    businessRequest.value = res.data
  } catch (error) {
    console.error('Lỗi khi lấy trạng thái đăng ký doanh nghiệp:', error)
  }
}

const submitBusinessRegistration = async () => {
  if (!businessForm.value.ten_doanh_nghiep.trim()) {
    notification.error('Vui lòng nhập tên doanh nghiệp / công ty!')
    return
  }
  if (!businessForm.value.ma_so_thue.trim()) {
    notification.error('Vui lòng nhập mã số thuế!')
    return
  }
  if (!businessForm.value.linh_vuc_kd.trim()) {
    notification.error('Vui lòng nhập lĩnh vực kinh doanh!')
    return
  }
  if (!businessForm.value.dia_chi_kd.trim()) {
    notification.error('Vui lòng nhập địa chỉ kinh doanh!')
    return
  }

  submittingBusiness.value = true
  try {
    const res = await xacThucApi.dangKyDoanhNghiep({
      ten_doanh_nghiep: businessForm.value.ten_doanh_nghiep,
      ma_so_thue: businessForm.value.ma_so_thue,
      dia_chi_kd: businessForm.value.dia_chi_kd,
      linh_vuc_kd: businessForm.value.linh_vuc_kd
    })

    if (res.data.success) {
      notification.show('Gửi yêu cầu đăng ký nâng cấp tài khoản Doanh nghiệp thành công! Vui lòng chờ Admin phê duyệt.', 'success')
      await fetchBusinessRequestStatus()
    }
  } catch (error) {
    console.error('Lỗi đăng ký doanh nghiệp:', error)
    notification.error(error.response?.data?.detail || 'Có lỗi xảy ra trong quá trình nâng cấp tài khoản.')
  } finally {
    submittingBusiness.value = false
  }
}

const menuItems = [
  { id: 'profile', label: 'Hồ sơ tài khoản' },
  { id: 'vouchers', label: 'Mã giảm giá' },
  { id: 'chat', label: 'Chat với Admin' },
  { id: 'wishlist', label: 'Sản phẩm yêu thích' },
  { id: 'orders', label: 'Lịch sử mua hàng' },
  { id: 'security', label: 'Mật khẩu & Bảo mật' },
  { id: 'reviews', label: 'Gửi hỗ trợ' },
  { id: 'devices', label: 'Lịch sử đăng nhập' },
  { id: 'notifications', label: 'Thông báo' }
]

const orders = ref([])
const loadingOrders = ref(false)

const showOrderDetailModal = ref(false)
const selectedOrderDetail = ref(null)

const openOrderDetail = (order) => {
  selectedOrderDetail.value = order
  showOrderDetailModal.value = true
}

const closeOrderDetail = () => {
  showOrderDetailModal.value = false
  selectedOrderDetail.value = null
}

const copyImeiToClipboard = (imei) => {
  navigator.clipboard.writeText(imei).then(() => {
    notification.show('Đã sao chép mã IMEI thành công!', 'success')
  }).catch((err) => {
    console.error('Lỗi khi sao chép IMEI:', err)
    notification.error('Không thể sao chép. Vui lòng tự sao chép thủ công.')
  })
}

const inHoaDonPDF = (order) => {
  const printWindow = window.open('', '_blank', 'width=900,height=900')
  if (!printWindow) {
    notification.error('Trình duyệt đã chặn cửa sổ bật lên. Vui lòng cấp quyền để in hóa đơn!')
    return
  }

  const itemsHtml = order.items.map(item => `
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">
        <strong style="font-size: 14px;">${item.san_pham?.ten || 'Thiết bị Apple'}</strong>
      </td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">${item.dung_luong || '-'} / ${item.mau_sac || '-'}</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-weight: bold;">x${item.so_luong}</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: right; font-weight: bold;">${formatPrice(item.gia)}</td>
      <td style="padding: 10px; border: 1px solid #ddd; text-align: right; font-weight: bold;">${formatPrice(item.gia * item.so_luong)}</td>
    </tr>
  `).join('')

  const content = `
    <html>
      <head>
        <title>Hóa đơn mua hàng #${order.id} - Peach Store</title>
        <meta charset="utf-8" />
        <style>
          body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; margin: 40px; line-height: 1.6; }
          .header { display: flex; justify-content: space-between; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
          .logo { font-size: 28px; font-weight: 800; letter-spacing: -0.5px; }
          .logo span { color: #007aff; }
          .info-block { display: flex; justify-content: space-between; margin-bottom: 30px; font-size: 14px; }
          .info-col { width: 48%; }
          .title { text-align: center; text-transform: uppercase; font-size: 22px; font-weight: 800; margin-bottom: 30px; letter-spacing: 0.5px; }
          table { width: 100%; border-collapse: collapse; margin-bottom: 30px; font-size: 14px; }
          th { background: #f5f5f7; padding: 12px 10px; border: 1px solid #ddd; font-weight: 700; text-align: left; }
          .total-block { width: 300px; margin-left: auto; margin-bottom: 40px; font-size: 14px; }
          .total-row { display: flex; justify-content: space-between; padding: 6px 0; }
          .grand-total { font-size: 18px; font-weight: bold; border-top: 1px solid #333; padding-top: 8px; margin-top: 6px; }
          .imei-box { border: 2px dashed #007aff; background: #f0f8ff; border-radius: 8px; padding: 15px; margin-bottom: 4px; font-size: 14.5px; text-align: center; }
          .footer-sig { display: flex; justify-content: space-between; margin-top: 60px; font-size: 14px; text-align: center; }
          .sig-col { width: 45%; }
          @media print {
            body { margin: 20px; }
            .no-print { display: none; }
          }
        </style>
      </head>
      <body>
        <div class="header">
          <div>
            <div class="logo">PEACH <span>STORE</span></div>
            <div style="font-size: 12px; color: #666; margin-top: 4px;">Hệ thống bán lẻ Apple & Phụ kiện cao cấp</div>
            <div style="font-size: 12px; color: #666;">Hotline: 1900.6868 | Website: peachstore.vn</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 16px; font-weight: bold;">HÓA ĐƠN ĐIỆN TỬ</div>
            <div style="font-size: 13px; color: #666; margin-top: 4px;">Số hóa đơn: <strong>#MS-${order.id}</strong></div>
            <div style="font-size: 13px; color: #666;">Ngày lập: ${formatDate(order.ngay_tao)}</div>
          </div>
        </div>

        <div class="title">HÓA ĐƠN BÁN HÀNG & PHIẾU BẢO HÀNH</div>

        <div class="info-block">
          <div class="info-col">
            <h4 style="margin: 0 0 10px 0; text-transform: uppercase; color: #666; font-size: 12px; border-bottom: 1px solid #ddd; padding-bottom: 4px;">Thông tin khách hàng</h4>
            <div style="font-size: 14px; line-height: 1.7;">
              <strong>Họ và tên:</strong> ${order.ten_khach_hang}<br/>
              <strong>Số điện thoại:</strong> ${order.so_dien_thoai}<br/>
              <strong>Địa chỉ nhận hàng:</strong> ${order.dia_chi}
            </div>
          </div>
          <div class="info-col" style="text-align: right;">
            <h4 style="margin: 0 0 10px 0; text-transform: uppercase; color: #666; font-size: 12px; border-bottom: 1px solid #ddd; padding-bottom: 4px; text-align: right;">Thông tin thanh toán</h4>
            <div style="font-size: 14px; line-height: 1.7;">
              <strong>Phương thức thanh toán:</strong> ${order.phuong_thuc_thanh_toan || 'Tiền mặt/Chuyển khoản'}<br/>
              <strong>Phương thức vận chuyển:</strong> ${order.phuong_thuc_van_chuyen || 'Tiêu chuẩn'}<br/>
              <strong>Tình trạng:</strong> <span style="color: green; font-weight: bold;">Hoàn thành</span>
            </div>
          </div>
        </div>

        <table>
          <thead>
            <tr>
              <th style="width: 45%;">Tên sản phẩm</th>
              <th style="width: 20%; text-align: center;">Thông số</th>
              <th style="width: 10%; text-align: center;">SL</th>
              <th style="width: 12%; text-align: right;">Đơn giá</th>
              <th style="width: 13%; text-align: right;">Thành tiền</th>
            </tr>
          </thead>
          <tbody>
            ${itemsHtml}
          </tbody>
        </table>

        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div style="width: 50%;">
            ${order.imei ? `
              <div class="imei-box">
                <div style="font-weight: bold; color: #007aff; margin-bottom: 4px; font-size: 15px;">MÃ IMEI BẢO HÀNH CHÍNH HÃNG</div>
                <div style="font-family: 'SF Mono', Monaco, monospace; font-size: 20px; font-weight: bold; letter-spacing: 1px; color: #333; margin: 8px 0;">${order.imei}</div>
                <div style="font-size: 12px; color: #666;">Quý khách vui lòng lưu trữ mã IMEI này để tra cứu bảo hành.<br/><strong>Đổi trả 1-đổi-1:</strong> 30 ngày nếu lỗi do NSX.<br/><strong>Bảo hành Peach Store:</strong> ${order.warranty_months || 6} tháng kể từ ngày hoàn thành đơn hàng.</div>
              </div>
            ` : `
              <div style="font-style: italic; color: #666; font-size: 13px;">Thiết bị chưa được kích hoạt IMEI. Vui lòng liên hệ bộ phận hỗ trợ khách hàng để được xử lý.</div>
            `}
          </div>
          
          <div class="total-block">
            <div class="total-row">
              <span style="color: #666;">Cộng tiền hàng:</span>
              <span style="font-weight: bold;">${formatPrice(order.tong_tien + order.giam_gia_voucher - order.phi_ship)}</span>
            </div>
            ${order.giam_gia_voucher > 0 ? `
              <div class="total-row" style="color: #ff3b30;">
                <span>Giảm giá Voucher:</span>
                <span>-${formatPrice(order.giam_gia_voucher)}</span>
              </div>
            ` : ''}
            <div class="total-row">
              <span style="color: #666;">Phí vận chuyển:</span>
              <span style="font-weight: bold;">+${formatPrice(order.phi_ship || 0)}</span>
            </div>
            <div class="total-row grand-total">
              <span>TỔNG THANH TOÁN:</span>
              <span style="color: #24b157;">${formatPrice(order.tong_tien)}</span>
            </div>
          </div>
        </div>

        <div style="margin-top: 30px; font-size: 12px; color: #666; font-style: italic; text-align: center;">
          Cảm ơn quý khách đã mua sắm tại Peach Store! Peach Store cam kết bảo mật thông tin khách hàng và cung cấp chế độ hậu mãi chuẩn Apple.
        </div>

        <div class="footer-sig">
          <div class="sig-col">
            <strong>KHÁCH HÀNG</strong><br/>
            <span style="font-size: 11px; color: #999;">(Ký, ghi rõ họ tên)</span>
            <div style="margin-top: 40px; font-weight: bold;">${order.ten_khach_hang}</div>
          </div>
          <div class="sig-col">
            <strong>ĐẠI DIỆN PEACH STORE</strong><br/>
            <span style="font-size: 11px; color: #999;">(Ký, đóng dấu)</span>
            <div style="margin-top: 40px; font-weight: bold; color: #007aff;">Đã xác nhận thanh toán</div>
          </div>
        </div>

        <script>
          window.onload = function() {
            window.print();
            setTimeout(function() { window.close(); }, 1000);
          }
        <\/script>
      </body>
    </html>
  `

  printWindow.document.write(content)
  printWindow.document.close()
}

const fetchOrders = async () => {
  loadingOrders.value = true
  try {
    const response = await donHangApi.getOrders()
    orders.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy đơn hàng:', error)
  } finally {
    loadingOrders.value = false
  }
}

const cancelOrder = async (orderId) => {
  if (!confirm('Bạn có chắc chắn muốn hủy đơn hàng này?')) return

  try {
    await donHangApi.updateStatus(orderId, { trang_thai: 'da_huy' })
    notification.show('Đã hủy đơn hàng thành công', 'success')
    fetchOrders() // Tải lại danh sách
  } catch (error) {
    console.error('Lỗi khi hủy đơn hàng:', error)
    notification.error('Không thể hủy đơn hàng. Vui lòng thử lại.')
  }
}

const vouchers = ref([])
const loadingVouchers = ref(false)

const fetchVouchers = async () => {
  loadingVouchers.value = true
  try {
    const response = await voucherApi.getUserVouchers()
    vouchers.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy mã giảm giá:', error)
  } finally {
    loadingVouchers.value = false
  }
}

const wishlist = ref([])
const loadingWishlist = ref(false)

const fetchWishlist = async () => {
  loadingWishlist.value = true
  try {
    const response = await yeuThichApi.getWishlist()
    wishlist.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy danh sách yêu thích:', error)
  } finally {
    loadingWishlist.value = false
  }
}

const removeWishlistItem = async (productId) => {
  try {
    await yeuThichApi.toggleWishlist(productId)
    notification.show('Đã xóa sản phẩm khỏi danh sách yêu thích', 'success')
    fetchWishlist() // Tải lại danh sách
  } catch (error) {
    console.error('Lỗi khi xóa sản phẩm yêu thích:', error)
    notification.error('Có lỗi xảy ra, vui lòng thử lại sau.')
  }
}

const loginHistory = ref([])
const loadingHistory = ref(false)

const fetchLoginHistory = async () => {
  loadingHistory.value = true
  try {
    const response = await xacThucApi.getLoginHistory()
    // Sắp xếp các phiên đăng nhập theo thứ tự thời gian giảm dần (mới nhất lên đầu)
    const sorted = (response.data || []).sort((a, b) => new Date(b.ngay_dang_nhap) - new Date(a.ngay_dang_nhap))
    // Chỉ lưu trữ tối đa 10 phiên đăng nhập gần đây nhất
    loginHistory.value = sorted.slice(0, 10)
  } catch (error) {
    console.error('Lỗi khi lấy lịch sử đăng nhập:', error)
  } finally {
    loadingHistory.value = false
  }
}

const userNotifications = ref([])
const loadingNotifications = ref(false)
const readNotificationIds = ref(JSON.parse(localStorage.getItem('read_notification_ids') || '[]'))
const readChatIds = ref(JSON.parse(localStorage.getItem('read_chat_ids') || '[]'))

const fetchUserNotifications = async () => {
  loadingNotifications.value = true
  try {
    const response = await xacThucApi.getNotifications()
    const allNotifs = response.data || []
    const readIds = readNotificationIds.value
    // Lọc bỏ những thông báo đã đọc, sau đó giới hạn tối đa 20 tin mới nhất
    userNotifications.value = allNotifs
      .filter(n => !readIds.includes(n.id))
      .slice(0, 20)
  } catch (error) {
    console.error('Lỗi khi lấy danh sách thông báo:', error)
  } finally {
    loadingNotifications.value = false
  }
}

const markAsRead = (id) => {
  if (!readNotificationIds.value.includes(id)) {
    readNotificationIds.value.push(id)
    localStorage.setItem('read_notification_ids', JSON.stringify(readNotificationIds.value))
    userNotifications.value = userNotifications.value.filter(n => n.id !== id)
    notification.show('Đã đánh dấu đã đọc và ẩn khỏi danh sách', 'success')
  }
}

const markAllAsRead = () => {
  const unreadIds = userNotifications.value.map(n => n.id)
  unreadIds.forEach(id => {
    if (!readNotificationIds.value.includes(id)) {
      readNotificationIds.value.push(id)
    }
  })
  localStorage.setItem('read_notification_ids', JSON.stringify(readNotificationIds.value))
  userNotifications.value = []
  notification.show('Đã đánh dấu đọc tất cả thông báo', 'success')
}

const getBadgeCount = (id) => {
  if (id === 'notifications') {
    return userNotifications.value.length
  }
  if (id === 'vouchers') {
    return vouchers.value.length
  }
  if (id === 'wishlist') {
    return wishlist.value.length
  }
  if (id === 'chat') {
    if (activeTab.value === 'chat') return 0
    return allMessages.value.filter(msg => msg.sender !== 'user' && !readChatIds.value.includes(msg.id)).length
  }
  return 0
}

const allMessages = ref([])
const visibleStartIdx = ref(0)
const newMsgText = ref('')
const loadingChat = ref(false)
const chatContainer = ref(null)

const renderedMessages = computed(() => {
  return allMessages.value.slice(visibleStartIdx.value, visibleStartIdx.value + 10)
})

const showLoadPrevious = computed(() => visibleStartIdx.value > 0)
const showLoadNext = computed(() => visibleStartIdx.value < allMessages.value.length - 10)

const loadPreviousMessages = () => {
  visibleStartIdx.value = Math.max(0, visibleStartIdx.value - 10)
  scrollToBottom()
}

const loadNextMessages = () => {
  visibleStartIdx.value = Math.min(allMessages.value.length - 10, visibleStartIdx.value + 10)
  scrollToBottom()
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

const markCurrentChatAsRead = () => {
  if (activeTab.value === 'chat' && allMessages.value.length > 0) {
    let updated = false
    const currentReadIds = [...readChatIds.value]
    allMessages.value.forEach(msg => {
      if (msg.sender !== 'user' && !currentReadIds.includes(msg.id)) {
        currentReadIds.push(msg.id)
        updated = true
      }
    })
    if (updated) {
      readChatIds.value = currentReadIds
      localStorage.setItem('read_chat_ids', JSON.stringify(currentReadIds))
    }
  }
}

const fetchChatMessages = async () => {
  loadingChat.value = true
  try {
    const response = await xacThucApi.getChatMessages()
    allMessages.value = response.data
    markCurrentChatAsRead()
    
    // Set initial visible window to the most recent 10 messages
    if (allMessages.value.length > 10) {
      visibleStartIdx.value = allMessages.value.length - 10
    } else {
      visibleStartIdx.value = 0
    }
    scrollToBottom()
  } catch (error) {
    console.error('Lỗi khi lấy tin nhắn chat:', error)
  } finally {
    loadingChat.value = false
  }
}

const fetchChatMessagesBackground = async () => {
  try {
    const response = await xacThucApi.getChatMessages()
    const newMessages = response.data || []
    if (newMessages.length !== allMessages.value.length) {
      allMessages.value = newMessages
      markCurrentChatAsRead()
      if (allMessages.value.length > 10) {
        visibleStartIdx.value = allMessages.value.length - 10
      } else {
        visibleStartIdx.value = 0
      }
      scrollToBottom()
    }
  } catch (error) {
    console.error('Lỗi khi cập nhật tin nhắn nền:', error)
  }
}

let chatIntervalId = null

const startChatPolling = () => {
  stopChatPolling()
  chatIntervalId = setInterval(() => {
    if (activeTab.value === 'chat') {
      fetchChatMessagesBackground()
    }
  }, 10000)
}

const stopChatPolling = () => {
  if (chatIntervalId) {
    clearInterval(chatIntervalId)
    chatIntervalId = null
  }
}

const sendMessage = async () => {
  const textVal = newMsgText.value.trim()
  if (!textVal) return

  newMsgText.value = ''
  try {
    const response = await xacThucApi.sendChatMessage(textVal)
    allMessages.value.push(response.data)
    
    // Shift window to show the newly sent message at the end
    if (allMessages.value.length > 10) {
      visibleStartIdx.value = allMessages.value.length - 10
    } else {
      visibleStartIdx.value = 0
    }
    scrollToBottom()
  } catch (error) {
    console.error('Lỗi khi gửi tin nhắn:', error)
    notification.error('Không thể gửi tin nhắn. Vui lòng thử lại.')
  }
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    notification.show('Đã sao chép mã giảm giá thành công!', 'success')
  }).catch((err) => {
    console.error('Lỗi khi sao chép:', err)
    notification.error('Không thể sao chép. Vui lòng tự bôi đen và sao chép.')
  })
}

const submittingSupport = ref(false)
const supportForm = ref({
  subject: '',
  serial: '',
  message: ''
})
const supportImages = ref([])
const supportImageInput = ref(null)

const triggerSupportImageSelect = () => {
  if (supportImageInput.value) {
    supportImageInput.value.click()
  }
}

const handleSupportImagesChange = (event) => {
  const files = Array.from(event.target.files)
  if (supportImages.value.length + files.length > 5) {
    notification.error('Bạn chỉ có thể đính kèm tối đa 5 hình ảnh!')
    return
  }

  files.forEach(file => {
    if (!file.type.startsWith('image/')) {
      notification.error('Chỉ hỗ trợ đính kèm file hình ảnh!')
      return
    }
    if (file.size > 10 * 1024 * 1024) {
      notification.error(`File ${file.name} vượt quá dung lượng tối đa 10MB!`)
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      supportImages.value.push({
        file: file,
        preview: e.target.result
      })
    }
    reader.readAsDataURL(file)
  })
  
  event.target.value = ''
}

const removeSupportImage = (index) => {
  supportImages.value.splice(index, 1)
}

const submitSupport = async () => {
  if (!supportForm.value.subject || !supportForm.value.message) return

  submittingSupport.value = true
  try {
    const formData = new FormData()
    formData.append('subject', supportForm.value.subject)
    formData.append('serial', supportForm.value.serial || '')
    formData.append('message', supportForm.value.message)
    
    supportImages.value.forEach(img => {
      formData.append('images', img.file)
    })

    await xacThucApi.sendSupportTicket(formData)
    
    notification.show("Gửi yêu cầu hỗ trợ thành công! Đội ngũ Peach sẽ kiểm tra và phản hồi sớm nhất.", "success")
    
    // Reset form
    supportForm.value = {
      subject: '',
      serial: '',
      message: ''
    }
    supportImages.value = []
  } catch (error) {
    console.error('Lỗi khi gửi hỗ trợ:', error)
    notification.error(error.response?.data?.detail || "Không thể gửi yêu cầu hỗ trợ. Vui lòng thử lại sau.")
  } finally {
    submittingSupport.value = false
  }
}

const fetchUserProfile = async () => {
  try {
    const response = await xacThucApi.getMe()
    user.value = response.data
    // Đồng bộ lại vào localStorage
    localStorage.setItem('user_profile', JSON.stringify(response.data))
    fetchBusinessRequestStatus()
  } catch (error) {
    console.error('Lỗi khi lấy thông tin cá nhân:', error)
    // Lỗi 401 được xử lý bởi axios interceptor
  }
}

const validatePhone = (e) => {
  // Chỉ cho phép nhập số
  const val = e.target.value.replace(/\D/g, '')
  user.value.so_dien_thoai = val.slice(0, 10)
}

const triggerAvatarUpload = () => {
  avatarInput.value.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    notification.error('Vui lòng chỉ chọn file hình ảnh')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    notification.error('Dung lượng ảnh không được vượt quá 5MB')
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await xacThucApi.uploadAvatar(formData)
    
    if (response.data.url) {
      user.value.hinh_anh = response.data.url
      notification.show('Đã cập nhật ảnh đại diện thành công', 'success')
      fetchUserProfile()
    }
  } catch (error) {
    console.error('Lỗi khi upload ảnh:', error)
    notification.error('Không thể tải ảnh lên. Vui lòng thử lại.')
  }
}

const removeAvatar = async () => {
  if (!confirm('Bạn có chắc chắn muốn xóa ảnh đại diện này?')) return

  try {
    await xacThucApi.deleteAvatar()
    user.value.hinh_anh = null
    notification.show('Đã xóa ảnh đại diện', 'success')
    fetchUserProfile()
  } catch (error) {
    console.error('Lỗi khi xóa ảnh:', error)
    notification.error('Không thể xóa ảnh. Vui lòng thử lại.')
  }
}

// Hàm định dạng ngày tháng
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('vi-VN', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
}

const formatLoginTime = (isoString) => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleString('vi-VN', {
    hour: '2-digit',
    minute: '2-digit',
    day: '2-digit',
    month: 'numeric',
    year: 'numeric'
  })
}

const formatPrice = (p) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

// Hàm xác định hạng thành viên
const getMembershipRank = (user) => {
  if (!user) return 'Chưa có hạng'
  if (user.vai_tro === 'admin') return 'Premium Admin'
  
  const points = user.diem_tich_luy || 0
  if (loyaltyLevels.value && loyaltyLevels.value.length > 0) {
    const sorted = [...loyaltyLevels.value].sort((a, b) => b.diem_toi_thieu - a.diem_toi_thieu)
    for (const level of sorted) {
      if (points >= level.diem_toi_thieu) {
        return level.ten_hang
      }
    }
    return 'Chưa có hạng'
  }
  
  if (points >= 5000) return 'Kim cương'
  if (points >= 1000) return 'Vàng'
  if (points >= 0) return 'Bạc'
  return 'Chưa có hạng'
}

// Hàm lấy class CSS cho từng hạng
const getRankClass = (user) => {
  if (!user) return 'no-rank'
  if (user.vai_tro === 'admin') return 'premium'
  
  const rank = getMembershipRank(user).toLowerCase()
  if (rank.includes('kim') || rank.includes('diamond')) return 'diamond'
  if (rank.includes('vàng') || rank.includes('gold')) return 'gold'
  if (rank.includes('bạc') || rank.includes('silver')) return 'silver'
  return 'no-rank'
}

const showLoyaltyDetailsModal = ref(false)

const getRankBg = (user) => {
  if (!user) return 'linear-gradient(135deg, #a6a6a6 0%, #8e8e93 100%)'
  if (user.vai_tro === 'admin') return 'linear-gradient(135deg, #8556d6 0%, #5856d6 100%)'
  
  const rank = getMembershipRank(user).toLowerCase()
  if (rank.includes('kim') || rank.includes('diamond')) {
    return 'linear-gradient(135deg, #5ac8fa 0%, #007aff 100%)'
  }
  if (rank.includes('vàng') || rank.includes('gold')) {
    return 'linear-gradient(135deg, #ffcc00 0%, #ff9500 100%)'
  }
  if (rank.includes('bạc') || rank.includes('silver')) {
    return 'linear-gradient(135deg, #a6a6a6 0%, #8e8e93 100%)'
  }
  return 'linear-gradient(135deg, #cfd8dc 0%, #90a4ae 100%)'
}

const getRankDiscount = (user) => {
  if (!user) return 0
  const points = user.diem_tich_luy || 0
  if (loyaltyLevels.value && loyaltyLevels.value.length > 0) {
    const sorted = [...loyaltyLevels.value].sort((a, b) => b.diem_toi_thieu - a.diem_toi_thieu)
    for (const level of sorted) {
      if (points >= level.diem_toi_thieu) {
        return level.phan_tram_giam
      }
    }
    return 0
  }
  if (points >= 5000) return 10
  if (points >= 1000) return 5
  return 0
}

const getRankBenefits = (user) => {
  if (!user) return ['Tích điểm mua sắm', 'Hỗ trợ tiêu chuẩn', 'Đổi trả hàng trong 30 ngày']
  const rank = getMembershipRank(user).toLowerCase()
  if (rank === 'chưa có hạng') {
    return ['Tích lũy điểm khi mua sắm (10,000đ = 1 điểm)', 'Hỗ trợ tư vấn mua hàng', 'Nhận hạng Bạc khi đủ điểm tối thiểu']
  }
  const points = user.diem_tich_luy || 0
  if (loyaltyLevels.value && loyaltyLevels.value.length > 0) {
    const sorted = [...loyaltyLevels.value].sort((a, b) => b.diem_toi_thieu - a.diem_toi_thieu)
    for (const level of sorted) {
      if (points >= level.diem_toi_thieu) {
        if (!level.uu_dai_rieng) return []
        if (Array.isArray(level.uu_dai_rieng)) return level.uu_dai_rieng
        if (typeof level.uu_dai_rieng === 'string') {
          return level.uu_dai_rieng.split(';').filter(x => x && x.trim())
        }
        return []
      }
    }
  }
  if (points >= 5000) {
    return ['Tích điểm mua sắm', 'Đặc quyền Hỗ trợ VIP 24/7', 'Miễn phí vận chuyển mọi đơn hàng', 'Đổi trả hàng trong 30 ngày', 'Trải nghiệm sớm sản phẩm mới']
  }
  if (points >= 1000) {
    return ['Tích điểm mua sắm', 'Hỗ trợ ưu tiên', 'Đổi trả hàng trong 30 ngày']
  }
  return ['Tích điểm mua sắm', 'Hỗ trợ tiêu chuẩn', 'Đổi trả hàng trong 30 ngày']
}

const getNextRankInfo = (user) => {
  if (!user) return null
  const currentPoints = user.diem_tich_luy || 0
  
  let tiers = []
  if (loyaltyLevels.value && loyaltyLevels.value.length > 0) {
    tiers = [...loyaltyLevels.value].sort((a, b) => a.diem_toi_thieu - b.diem_toi_thieu)
  } else {
    tiers = [
      { ten_hang: 'Bạc', diem_toi_thieu: 0 },
      { ten_hang: 'Vàng', diem_toi_thieu: 1000 },
      { ten_hang: 'Kim cương', diem_toi_thieu: 5000 }
    ]
  }
  
  // Find the next tier
  const nextTier = tiers.find(t => t.diem_toi_thieu > currentPoints)
  if (!nextTier) return null // Already highest rank
  
  const targetPoints = nextTier.diem_toi_thieu
  const pointsNeeded = targetPoints - currentPoints
  const percent = Math.min(100, Math.max(0, (currentPoints / targetPoints) * 100))
  
  return {
    nextRankName: nextTier.ten_hang,
    targetPoints,
    pointsNeeded,
    percent: Math.round(percent)
  }
}

// Hàm xử lý URL hình ảnh
const getImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}${url}`
}

const getStatusLabel = (status) => {
  const map = {
    'cho_duyet': 'Chờ duyệt',
    'da_duyet': 'Đã duyệt',
    'dang_giao': 'Đang giao',
    'hoan_thanh': 'Hoàn thành',
    'da_giao': 'Đã giao hàng',
    'da_huy': 'Đã hủy'
  }
  return map[status] || status
}

const getStatusClass = (status) => {
  const map = {
    'cho_duyet': 'processing',
    'da_duyet': 'processing',
    'dang_giao': 'shipping',
    'hoan_thanh': 'delivered',
    'da_giao': 'delivered',
    'da_huy': 'cancelled'
  }
  return map[status] || ''
}

onMounted(() => {
  // Lấy tab từ query parameter nếu có
  if (route.query.tab) {
    activeTab.value = route.query.tab
  }
  
  fetchUserProfile()
  fetchLoyaltyLevels()

  // Tải đồng thời tất cả dữ liệu để hiển thị huy hiệu thông báo đỏ ngay lập tức
  fetchVouchers()
  fetchWishlist()
  fetchChatMessages()
  fetchUserNotifications()

  startChatPolling()

  if (activeTab.value === 'orders' || route.query.tab === 'orders') {
    fetchOrders()
  }
  if (activeTab.value === 'devices' || route.query.tab === 'devices') {
    fetchLoginHistory()
  }
})

onUnmounted(() => {
  stopChatPolling()
})

// Theo dõi thay đổi của activeTab để fetch dữ liệu tương ứng
watch(activeTab, (newTab) => {
  if (newTab === 'orders') {
    fetchOrders()
  } else if (newTab === 'vouchers') {
    fetchVouchers()
  } else if (newTab === 'wishlist') {
    fetchWishlist()
  } else if (newTab === 'devices') {
    fetchLoginHistory()
  } else if (newTab === 'chat') {
    fetchChatMessages()
    markCurrentChatAsRead()
  } else if (newTab === 'notifications') {
    fetchUserNotifications()
  }
})

const saveProfile = async () => {
  saving.value = true
  try {
    const response = await xacThucApi.updateProfile({
      ho_ten: user.value.ho_ten,
      so_dien_thoai: user.value.so_dien_thoai,
      dia_chi: user.value.dia_chi
    })
    
    user.value = response.data
    localStorage.setItem('user_profile', JSON.stringify(response.data))
    notification.show("Đã lưu thông tin tài khoản thành công", "success")
  } catch (error) {
    console.error('Lỗi khi lưu hồ sơ:', error)
    notification.error(error.response?.data?.detail || "Không thể lưu thông tin. Vui lòng thử lại.")
  } finally {
    saving.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('access_token')
  router.push('/login')
}
</script>

<style scoped>
.account-page {
  background-color: #ffffff;
  padding: 120px 20px 80px;
  color: #1d1d1f;
}

.account-container {
  max-width: 980px;
  margin: 0 auto;
}

/* Header Area */
.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 40px;
  border-bottom: 1px solid #d2d2d7;
  margin-bottom: 40px;
}

.profile-summary {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
}

.avatar-img-container {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  position: relative;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 50%;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.remove-avatar-btn {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #ff3b30;
  color: white;
  border: 2px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 100;
  opacity: 0;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.avatar-wrapper:hover .remove-avatar-btn {
  opacity: 1;
}

.remove-avatar-btn:hover {
  background: #ff3b30;
  transform: scale(1.1);
}

.avatar-circle {
  width: 80px;
  height: 80px;
  background: #f5f5f7;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 600;
  color: #86868b;
  position: relative;
}

.hidden-input {
  display: none;
}

.user-name { font-size: 32px; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
.user-email { font-size: 17px; color: #86868b; margin: 4px 0 0; }

.status-label { display: block; font-size: 12px; color: #86868b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.status-value { font-size: 19px; font-weight: 600; }
.status-value.gold { color: #b8860b; }
.status-value.silver { color: #8e8e93; }
.status-value.diamond { color: #007aff; }
.status-value.premium { color: #5856d6; }
.status-value.no-rank { color: #86868b; }

/* Layout */
.content-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 60px;
  flex: 1;
  min-height: 0; /* Quan trọng để overflow hoạt động */
}

/* Navigation */
.account-nav { 
  display: flex; 
  flex-direction: column; 
  gap: 12px; 
  padding-bottom: 40px;
  overflow-y: auto; /* Sidebar cũng có thể cuộn nếu quá dài */
}

.nav-link {
  background: none;
  border: none;
  padding: 8px 0;
  font-size: 16px;
  font-weight: 500;
  color: #424245;
  text-align: left;
  cursor: pointer;
  transition: color 0.2s;
}

.nav-link:hover { color: #007aff; }
.nav-link.active { color: #007aff; font-weight: 600; }
.nav-link.logout { color: #ff3b30; margin-top: 20px; }

.nav-divider { height: 1px; background: #d2d2d7; margin: 10px 0; }

/* Content Sections */
.group-title { font-size: 24px; font-weight: 600; margin-bottom: 30px; }

.settings-group { margin-bottom: 60px; }

/* Table Style Layout */
.settings-table {
  width: 100%;
  border-top: 1px solid #d2d2d7;
  display: flex;
  flex-direction: column;
}

.table-row {
  display: flex;
  padding: 24px 0;
  border-bottom: 0.5px solid #d2d2d7;
  align-items: flex-start; /* Căn lề trên để đồng bộ khi có textarea */
}

.table-label {
  width: 240px;
  font-size: 14px;
  font-weight: 500;
  color: #86868b;
  flex-shrink: 0;
  padding-top: 4px; /* Cân bằng với dòng đầu của input */
}

.table-value {
  flex: 1;
  min-width: 0;
}

.input-wrapper input, .input-wrapper textarea {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 16px;
  color: #1d1d1f;
  padding: 0;
  font-family: inherit;
}

.input-wrapper input:focus, .input-wrapper textarea:focus { outline: none; }
.input-wrapper textarea { height: 100px; resize: none; line-height: 1.6; }

.value-text { font-size: 16px; color: #1d1d1f; }

/* Khối nút chức năng Sidebar - Hình chữ nhật vừa khít */
.sidebar-action-block {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #d2d2d7;
  width: 100%; /* Đảm bảo rộng bằng khít với Sidebar */
}

.action-btn-item {
  width: 100%;
  padding: 14px;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.action-btn-item.save {
  background: #0071e3;
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.action-btn-item.save:hover {
  background: #0077ed;
}

.action-btn-item.logout {
  background: #ffffff;
  color: #ff3b30;
}

.action-btn-item.logout:hover {
  background: #fff5f5;
}

.action-btn-item:disabled {
  background: #f5f5f7;
  color: #86868b;
  cursor: not-allowed;
}

/* Voucher Grid */
/* Voucher List & Profile Scroll Container with Apple Smooth Scrollbar */
.voucher-list,
.profile-scroll-container {
  max-height: 430px; 
  overflow-y: auto;
  padding: 5px 15px 5px 0;
  background: transparent;
  border: none;
}

/* Thanh cuộn siêu mảnh và tinh tế kiểu Apple cho Voucher & Profile */
.voucher-list::-webkit-scrollbar,
.profile-scroll-container::-webkit-scrollbar {
  width: 5px;
}

.voucher-list::-webkit-scrollbar-track,
.profile-scroll-container::-webkit-scrollbar-track {
  background: transparent;
}

.voucher-list::-webkit-scrollbar-thumb,
.profile-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  transition: all 0.3s;
}

.voucher-list:hover::-webkit-scrollbar-thumb,
.profile-scroll-container:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
}

/* Security Scroll Container with Apple Smooth Scrollbar */
.security-scroll-container {
  max-height: 520px; 
  overflow-y: auto;
  padding: 5px 15px 5px 0;
  background: transparent;
  border: none;
}

.security-scroll-container::-webkit-scrollbar {
  width: 5px;
}

.security-scroll-container::-webkit-scrollbar-track {
  background: transparent;
}

.security-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  transition: all 0.3s;
}

.security-scroll-container:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
}

.voucher-grid { display: grid; grid-template-columns: 1fr; gap: 20px; }
.voucher-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: #f5f5f7;
  border-radius: 18px;
}

.v-tag { font-size: 11px; font-weight: 700; background: #007aff; color: white; padding: 4px 10px; border-radius: 10px; }
.v-info h3 { font-size: 18px; margin: 10px 0 4px; }
.v-info p { font-size: 13px; color: #86868b; margin: 0; }

.v-use {
  background: white;
  border: 1px solid #d2d2d7;
  padding: 8px 18px;
  border-radius: 15px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

/* Order History Styles */
.order-list {
  display: flex;
  flex-direction: column;
  gap: 25px;
  max-height: 600px; 
  overflow-y: auto;
  padding: 5px 15px 5px 0;
  background: transparent; /* Bỏ nền xám */
  border: none; /* Bỏ viền khung */
}

/* Thanh cuộn siêu mảnh và tinh tế kiểu Apple */
.order-list::-webkit-scrollbar {
  width: 5px;
}

.order-list::-webkit-scrollbar-track {
  background: transparent;
}

.order-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  transition: all 0.3s;
}

.order-list:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
}

.order-item {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e5e5ea;
  overflow: hidden;
  flex-shrink: 0; /* QUAN TRỌNG: Ngăn đơn hàng bị bóp bẹp khi danh sách dài */
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #f5f5f7;
  border-bottom: 1px solid #d2d2d7;
}

.order-info-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-id { font-weight: 600; font-size: 15px; }
.order-date { font-size: 13px; color: #86868b; }

.order-status {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
}

.order-status.delivered { background: #e3f9e5; color: #1e7e34; }
.order-status.processing { background: #fff4e5; color: #b05d22; }
.order-status.shipping { background: #e5f1ff; color: #007aff; }
.order-status.cancelled { background: #fff5f5; color: #ff3b30; }

.order-status-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cancel-btn-mini {
  background: white;
  border: 1px solid #d2d2d7;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: #ff3b30;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn-mini:hover {
  background: #fff5f5;
  border-color: #ff3b30;
}

.order-products { 
  padding: 10px 24px; 
}

.product-mini {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px 0;
  border-bottom: 0.5px solid #f5f5f7;
}

.product-mini:last-child {
  border-bottom: none;
}

.mini-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.mini-details h4 { font-size: 15px; margin: 0 0 4px; font-weight: 500; }
.mini-details p { font-size: 13px; color: #86868b; margin: 0; }
.mini-price { margin-left: auto; font-weight: 600; font-size: 15px; }

.order-footer {
  display: flex;
  justify-content: space-between;
  padding: 16px 24px;
  border-top: 0.5px solid #d2d2d7;
  align-items: center;
}

.total-label { font-size: 14px; color: #86868b; }
.total-amount { font-size: 18px; font-weight: 700; color: #1d1d1f; }

/* Mobile Navigation Trigger & Inline Expandable Panel */
.mobile-nav-trigger-wrapper {
  display: none; /* Ẩn mặc định trên desktop */
  margin-bottom: 24px;
}

.mobile-nav-trigger-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 16px 20px;
  background: #f5f5f7;
  border: 1px solid #e5e5e7;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  color: #007aff;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.mobile-nav-trigger-btn:hover {
  background: #e8e8ed;
}

.chevron-icon {
  width: 16px;
  height: 16px;
  color: #007aff;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.chevron-icon.rotate {
  transform: rotate(180deg);
}

/* Inline Expandable Menu Panel */
.mobile-menu-inline-panel {
  margin-top: 10px;
  background: #ffffff;
  border: 1px solid #e5e5e7;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  animation: slideDown 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.inline-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px 12px;
  border-bottom: 1px solid #f5f5f7;
  margin-bottom: 8px;
}

.inline-panel-header span {
  font-size: 13px;
  font-weight: 600;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.inline-close-btn {
  background: #f5f5f7;
  color: #86868b;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.inline-close-btn:hover {
  background: #e8e8ed;
  color: #1d1d1f;
}

.mobile-account-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 380px;
  overflow-y: auto;
  padding-right: 4px;
}

/* Custom Scrollbar for Inline Mobile Menu */
.mobile-account-nav::-webkit-scrollbar {
  width: 4px;
}

.mobile-account-nav::-webkit-scrollbar-track {
  background: transparent;
}

.mobile-account-nav::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.mobile-nav-link {
  background: none;
  border: none;
  padding: 10px 12px;
  font-size: 15px;
  font-weight: 500;
  color: #1d1d1f;
  text-align: left;
  cursor: pointer;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.15s;
}

.mobile-nav-link:hover {
  background: #f5f5f7;
  color: #007aff;
}

.mobile-nav-link.active {
  background: #f0f7ff;
  color: #007aff;
  font-weight: 600;
}

.mobile-nav-link.logout {
  color: #ff3b30;
  margin-top: 14px;
  border-top: 0.5px solid #f5f5f7;
  border-radius: 0;
  padding-top: 14px;
}

.mobile-nav-link.logout:hover {
  background: transparent;
  color: #d72c21;
}

.checkmark-icon {
  width: 14px;
  height: 14px;
  color: #007aff;
}

.mobile-sidebar-action-block {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #d2d2d7;
}

.mobile-action-btn {
  width: 100%;
  padding: 10px;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.mobile-action-btn.save {
  background: #0071e3;
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-action-btn.save:hover {
  background: #0077ed;
}

.mobile-action-btn.logout {
  background: #ffffff;
  color: #ff3b30;
}

.mobile-action-btn.logout:hover {
  background: #fff5f5;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 850px) {
  .account-page { padding-top: 80px; }
  .account-header { 
    flex-direction: column; 
    align-items: center; 
    text-align: center;
    gap: 24px; 
    padding-bottom: 32px;
  }
  .profile-summary { 
    flex-direction: column; 
    gap: 16px; 
  }
  .avatar-img-container, .avatar-circle {
    width: 100px;
    height: 100px;
  }
  .user-name { font-size: 24px; }
  .membership-status {
    border-top: 1px solid #f5f5f7;
    padding-top: 16px;
    width: 100%;
  }
  .content-layout { grid-template-columns: 1fr; gap: 40px; }
  .table-row { flex-direction: column; gap: 10px; }
  .table-label { width: 100%; }

  .account-nav {
    display: none; /* Ẩn sidebar truyền thống trên mobile */
  }
  .mobile-nav-trigger-wrapper {
    display: block; /* Hiện nút kích hoạt menu hamburger */
  }
}

/* Wishlist Tab Styles */
.wishlist-container {
  max-height: 430px; 
  overflow-y: auto;
  padding: 5px 15px 5px 0;
  background: transparent;
  border: none;
}

.wishlist-container::-webkit-scrollbar {
  width: 5px;
}

.wishlist-container::-webkit-scrollbar-track {
  background: transparent;
}

.wishlist-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  transition: all 0.3s;
}

.wishlist-container:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
}

.wishlist-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.wishlist-item {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #ffffff;
  border: 1px solid #e5e5e7;
  border-radius: 14px;
  padding: 12px 16px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.wishlist-item:hover {
  border-color: rgba(0, 122, 255, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.wishlist-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
  background: #f5f5f7;
  border-radius: 8px;
  padding: 4px;
}

.wishlist-details {
  flex: 1;
}

.wishlist-name {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 4px 0;
}

.wishlist-price {
  font-size: 14px;
  font-weight: 500;
  color: #86868b;
  margin: 0;
}

.wishlist-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.wishlist-btn-view {
  background: #007aff;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
}

.wishlist-btn-view:hover {
  background: #0066cc;
}

.wishlist-btn-delete {
  background: #f5f5f7;
  color: #86868b;
  border: none;
  border-radius: 10px;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.wishlist-btn-delete:hover {
  background: #fff0f0;
  color: #ff3b30;
}

.trash-icon {
  width: 16px;
  height: 16px;
}

/* Apple Switch Toggle */
.apple-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 28px;
}

.apple-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.apple-switch .slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e5e5ea;
  transition: .3s;
  border-radius: 34px;
}

.apple-switch .slider:before {
  position: absolute;
  content: "";
  height: 24px;
  width: 24px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

.apple-switch input:checked + .slider {
  background-color: #34c759;
}

.apple-switch input:checked + .slider:before {
  transform: translateX(22px);
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

.modal-icon-container.red {
  background: #fff0f0;
  border: 2px solid #ff3b30;
  color: #ff3b30;
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

.modal-input-group label {
  font-size: 12px;
  font-weight: 600;
  color: #86868b;
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
  background: #86868b;
  opacity: 0.5;
  cursor: not-allowed;
}

/* Login History (Devices) Tab Styles */
.devices-scroll-container {
  max-height: 430px; 
  overflow-y: auto;
  padding: 5px 15px 5px 0;
  background: transparent;
  border: none;
}

.devices-scroll-container::-webkit-scrollbar {
  width: 5px;
}

.devices-scroll-container::-webkit-scrollbar-track {
  background: transparent;
}

.devices-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  transition: all 0.3s;
}

.devices-scroll-container:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
}

.device-list-grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.device-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: #ffffff;
  border: 1px solid #e5e5e7;
  border-radius: 16px;
  padding: 16px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.device-item:hover {
  border-color: rgba(0, 122, 255, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.device-item.active {
  border-color: rgba(52, 199, 89, 0.3);
  background: rgba(52, 199, 89, 0.01);
}

.device-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #f5f5f7;
  color: #86868b;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.device-icon-wrapper.active {
  background: rgba(52, 199, 89, 0.1);
  color: #34c759;
}

.device-icon {
  width: 22px;
  height: 22px;
}

.device-info {
  flex: 1;
}

.device-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}

.device-name {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
}

.device-badge-active {
  font-size: 11px;
  font-weight: 700;
  color: #34c759;
  background: rgba(52, 199, 89, 0.1);
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.device-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.device-details span {
  font-size: 13px;
  color: #515154;
  line-height: 1.4;
  text-align: left;
}

.device-details strong {
  color: #1d1d1f;
  font-weight: 500;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleUp {
  from { transform: scale(0.85); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Chat với Admin Styles */
.chat-messages-container::-webkit-scrollbar {
  width: 5px;
}

.chat-messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.chat-messages-container:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.18);
}

.typing-dot {
  width: 6px;
  height: 6px;
  background-color: #86868b;
  border-radius: 50%;
  animation: typingBounce 1.4s infinite ease-in-out both;
}

@keyframes typingBounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>
