import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', 
  headers: {
    'Content-Type': 'application/json',
  },
});


api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    if (token && token !== 'null' && token !== 'undefined') {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);


api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.error("Phiên đăng nhập hết hạn hoặc không hợp lệ. Đang chuyển hướng...");
      
      // Xóa token cũ
      localStorage.removeItem('access_token');
      localStorage.removeItem('token');
      localStorage.removeItem('user_profile');

      // Chuyển hướng về login (tránh redirect loop)
      if (!window.location.pathname.includes('/login')) {
        // Lưu lại trang hiện tại để quay lại sau khi login
        localStorage.setItem('redirect_after_login', window.location.pathname);
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const xacThucApi = {
  dangKy(data) {
    return api.post('/xac-thuc/dang-ky', data);
  },
  dangNhap(data) {
    return api.post('/xac-thuc/dang-nhap', data);
  },
  getMe() {
    return api.get('/xac-thuc/me');
  },
  uploadAvatar(formData) {
    return api.post('/xac-thuc/upload-avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  deleteAvatar() {
    return api.delete('/xac-thuc/delete-avatar');
  },
  updateProfile(data) {
    return api.put('/xac-thuc/update-profile', data);
  },
  doiMatKhau(data) {
    return api.put('/xac-thuc/doi-mat-khau', data);
  },
  caiDatPin(data) {
    return api.post('/xac-thuc/cai-dat-pin', data);
  },
  togglePin(data) {
    return api.post('/xac-thuc/toggle-pin', data);
  },
  getLoginHistory() {
    return api.get('/xac-thuc/lich-su-dang-nhap');
  },
  getChatMessages() {
    return api.get('/xac-thuc/tin-nhan-chat');
  },
  sendChatMessage(text) {
    return api.post('/xac-thuc/tin-nhan-chat', { text });
  },
  sendSupportTicket(formData) {
    return api.post('/xac-thuc/support/ticket', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  dangKyDoanhNghiep(data) {
    return api.post('/xac-thuc/dang-ky-doanh-nghiep', data);
  },
  getTrangThaiDoanhNghiep() {
    return api.get('/xac-thuc/trang-thai-doanh-nghiep');
  },
  getNotifications() {
    return api.get('/xac-thuc/notifications');
  }
};

export const sanPhamApi = {
  getAll() {
    return api.get('/san-pham/');
  },
  getByCategory(category) {
    return api.get(`/san-pham/danh-muc/${category}`);
  },
  getById(id) {
    return api.get(`/san-pham/${id}`);
  }
};

export const gioHangApi = {
  getCart() {
    return api.get('/gio-hang/');
  },
  addToCart(data) {
    return api.post('/gio-hang/them', data);
  },
  updateQuantity(itemId, data) {
    return api.put(`/gio-hang/cap-nhat/${itemId}`, data);
  },
  removeItem(itemId) {
    return api.delete(`/gio-hang/xoa/${itemId}`);
  }
};

export const donHangApi = {
  taoDonHang(data) {
    return api.post('/don-hang/tao', data);
  },
  getOrders() {
    return api.get('/don-hang/user/my-orders');
  },
  updateStatus(orderId, data) {
    return api.put(`/don-hang/cap-nhat-trang-thai/${orderId}`, data);
  }
}

export const voucherApi = {
  getAll() {
    return api.get('/vouchers/');
  },
  getUserVouchers() {
    return api.get('/vouchers/user/all');
  },
  checkVoucher(maVoucher, tongBill) {
    return api.post('/vouchers/check-voucher', { ma_voucher: maVoucher, tong_bill: tongBill });
  }
};

export const shippingApi = {
  getDonVi() {
    return api.get('/shipping/don-vi');
  },
  tinhPhiShip(maDonVi, tongBill) {
    return api.post('/shipping/tinh-phi', { ma_don_vi: maDonVi, tong_bill: tongBill });
  }
};

export const paymentApi = {
  getDoiTac() {
    return api.get('/payment/doi-tac');
  }
};

export const yeuThichApi = {
  getWishlist() {
    return api.get('/yeu-thich/');
  },
  toggleWishlist(productId) {
    return api.post(`/yeu-thich/toggle/${productId}`);
  },
  checkWishlist(productId) {
    return api.get(`/yeu-thich/check/${productId}`);
  }
};

export default api;

