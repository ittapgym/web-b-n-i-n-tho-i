import { defineStore } from 'pinia';
import { gioHangApi, voucherApi, shippingApi, paymentApi } from '../services/api';

/**
 * Pinia Store quản lý trạng thái giỏ hàng toàn cục của ứng dụng Web Frontend.
 * Đồng bộ hóa giỏ hàng của người dùng, tính toán chi phí vận chuyển, áp dụng voucher giảm giá
 * và cung cấp dữ liệu thanh toán (Checkout).
 */
export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    loading: false,
    // Shipping & Payment state
    selectedShipMethod: null,
    selectedPaymentMethod: null,
    phiShip: 0,
    shippingMethods: [],
    paymentMethods: [],
    // Voucher state
    appliedVoucher: null, // { ma_voucher, so_tien_giam, loai_giam_gia, ... }
    voucherLoading: false,
    voucherError: null,
    // Checkout loading
    checkoutLoading: false
  }),
  getters: {
    /**
     * Tính tổng số lượng tất cả các sản phẩm đang có trong giỏ hàng.
     * 
     * @param {Object} state - Trạng thái store hiện tại.
     * @returns {number} Tổng số lượng sản phẩm.
     */
    count: (state) => {
      return state.items.reduce((sum, item) => sum + item.so_luong, 0);
    },
    /**
     * Tính tổng tiền hàng thuần túy (chưa cộng phí vận chuyển, chưa trừ voucher giảm giá).
     * 
     * @param {Object} state - Trạng thái store hiện tại.
     * @returns {number} Tổng tiền hàng.
     */
    tongTienHang: (state) => {
      return state.items.reduce((sum, item) => sum + (item.san_pham?.gia || 0) * item.so_luong, 0);
    },
    /**
     * Tính tổng tiền thanh toán cuối cùng của đơn hàng.
     * Công thức: Tổng thanh toán = Tổng tiền hàng - Số tiền giảm giá voucher + Phí vận chuyển.
     * 
     * @param {Object} state - Trạng thái store hiện tại.
     * @returns {number} Tổng thanh toán cuối cùng.
     */
    total: (state) => {
      // tong_thanh_toan_cuoi = tong_tien_hang - giam_gia_voucher + phi_ship
      const giamGia = state.appliedVoucher?.so_tien_giam || 0;
      const tongHang = state.items.reduce((sum, item) => sum + (item.san_pham?.gia || 0) * item.so_luong, 0);
      return tongHang - giamGia + state.phiShip;
    }
  },
  actions: {
    /**
     * Gọi API tải giỏ hàng của người dùng đang đăng nhập từ máy chủ.
     * Nếu không có token đăng nhập hợp lệ, giỏ hàng sẽ được reset về rỗng.
     */
    async fetchCart() {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');
      if (!token || token === 'null' || token === 'undefined') {
        this.items = [];
        return;
      }
      
      this.loading = true;
      try {
        const res = await gioHangApi.getCart();
        this.items = res.data;
      } catch (error) {
        console.error("Lỗi khi tải giỏ hàng trong store:", error);
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * Thiết lập danh sách các sản phẩm trong giỏ hàng trực tiếp.
     * 
     * @param {Array} items - Danh sách sản phẩm mới.
     */
    setItems(items) {
      this.items = items;
    },
    
    /**
     * Xóa sạch các sản phẩm trong giỏ hàng ở Client.
     */
    clearCart() {
      this.items = [];
    },

    // ---- Shipping Methods ----
    /**
     * Tải danh sách các phương thức và đơn vị vận chuyển có sẵn từ API.
     */
    async fetchShippingMethods() {
      try {
        const res = await shippingApi.getDonVi();
        this.shippingMethods = res.data;
      } catch (error) {
        console.error("Lỗi khi tải phương thức vận chuyển:", error);
        this.shippingMethods = [];
      }
    },

    /**
     * Chọn đơn vị vận chuyển và tự động tính toán phí vận chuyển dựa trên tổng giá trị giỏ hàng.
     * Nếu chọn lại đúng đơn vị vận chuyển đang chọn, hệ thống sẽ bỏ chọn và đặt phí ship về 0.
     * 
     * @param {string} maDonVi - Mã định danh đơn vị vận chuyển.
     */
    async setShipMethod(maDonVi) {
      // Reset if same method selected
      if (this.selectedShipMethod === maDonVi) {
        this.selectedShipMethod = null;
        this.phiShip = 0;
        return;
      }
      this.selectedShipMethod = maDonVi;
      // Calculate shipping fee
      const tongHang = this.items.reduce((sum, item) => sum + (item.san_pham?.gia || 0) * item.so_luong, 0);
      try {
        const res = await shippingApi.tinhPhiShip(maDonVi, tongHang);
        this.phiShip = res.data.phi_ship;
      } catch (error) {
        console.error("Lỗi khi tính phí ship:", error);
        this.phiShip = 0;
      }
    },

    // ---- Payment Methods ----
    /**
     * Tải danh sách các đối tác và phương thức thanh toán có sẵn từ API.
     */
    async fetchPaymentMethods() {
      try {
        const res = await paymentApi.getDoiTac();
        this.paymentMethods = res.data;
      } catch (error) {
        console.error("Lỗi khi tải phương thức thanh toán:", error);
        this.paymentMethods = [];
      }
    },

    /**
     * Chọn phương thức thanh toán cho đơn hàng.
     * 
     * @param {string} maPhuongThuc - Mã định danh phương thức thanh toán (ví dụ: 'chuyen_khoan', 'cod').
     */
    setPaymentMethod(maPhuongThuc) {
      if (this.selectedPaymentMethod === maPhuongThuc) {
        this.selectedPaymentMethod = null;
        return;
      }
      this.selectedPaymentMethod = maPhuongThuc;
    },

    // ---- Voucher ----
    /**
     * Áp dụng mã voucher giảm giá vào giỏ hàng hiện tại.
     * Gửi yêu cầu kiểm tra tính hợp lệ của voucher và số tiền giảm giá tối đa dựa trên tổng tiền hàng.
     * 
     * @param {string} maVoucher - Mã code của voucher.
     */
    async applyVoucherCode(maVoucher) {
      if (!maVoucher || maVoucher.trim() === '') {
        this.voucherError = 'Vui lòng nhập mã giảm giá';
        return;
      }
      this.voucherLoading = true;
      this.voucherError = null;
      const tongHang = this.items.reduce((sum, item) => sum + (item.san_pham?.gia || 0) * item.so_luong, 0);
      try {
        const res = await voucherApi.checkVoucher(maVoucher, tongHang);
        if (res.data.hop_le) {
          this.appliedVoucher = {
            ma_voucher: res.data.ma_voucher,
            so_tien_giam: res.data.so_tien_giam,
            loai_giam_gia: res.data.loai_giam_gia,
            gia_tri_giam: res.data.gia_tri_giam,
            giam_toi_da: res.data.giam_toi_da
          };
          this.voucherError = null;
        } else {
          this.appliedVoucher = null;
          this.voucherError = res.data.loi || 'Mã giảm giá không hợp lệ';
        }
      } catch (error) {
        this.appliedVoucher = null;
        this.voucherError = 'Lỗi khi kiểm tra mã giảm giá';
        console.error("Lỗi khi áp dụng voucher:", error);
      } finally {
        this.voucherLoading = false;
      }
    },

    /**
     * Hủy bỏ voucher đang áp dụng khỏi giỏ hàng.
     */
    removeVoucher() {
      this.appliedVoucher = null;
      this.voucherError = null;
    },

    // ---- Checkout helpers ----
    /**
     * Dọn dẹp toàn bộ giỏ hàng, đơn vị vận chuyển, phương thức thanh toán và voucher sau khi đã đặt hàng thành công.
     */
    clearCartAfterOrder() {
      this.items = [];
      this.selectedShipMethod = null;
      this.selectedPaymentMethod = null;
      this.phiShip = 0;
      this.appliedVoucher = null;
      this.voucherError = null;
    }
  }
});
