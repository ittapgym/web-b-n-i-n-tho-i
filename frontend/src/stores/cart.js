import { defineStore } from 'pinia';
import { gioHangApi, voucherApi, shippingApi, paymentApi } from '../services/api';

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
    count: (state) => {
      return state.items.reduce((sum, item) => sum + item.so_luong, 0);
    },
    tongTienHang: (state) => {
      return state.items.reduce((sum, item) => sum + (item.san_pham?.gia || 0) * item.so_luong, 0);
    },
    total: (state) => {
      // tong_thanh_toan_cuoi = tong_tien_hang - giam_gia_voucher + phi_ship
      const giamGia = state.appliedVoucher?.so_tien_giam || 0;
      const tongHang = state.items.reduce((sum, item) => sum + (item.san_pham?.gia || 0) * item.so_luong, 0);
      return tongHang - giamGia + state.phiShip;
    }
  },
  actions: {
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
    
    setItems(items) {
      this.items = items;
    },
    
    clearCart() {
      this.items = [];
    },

    // ---- Shipping Methods ----
    async fetchShippingMethods() {
      try {
        const res = await shippingApi.getDonVi();
        this.shippingMethods = res.data;
      } catch (error) {
        console.error("Lỗi khi tải phương thức vận chuyển:", error);
        this.shippingMethods = [];
      }
    },

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
    async fetchPaymentMethods() {
      try {
        const res = await paymentApi.getDoiTac();
        this.paymentMethods = res.data;
      } catch (error) {
        console.error("Lỗi khi tải phương thức thanh toán:", error);
        this.paymentMethods = [];
      }
    },

    setPaymentMethod(maPhuongThuc) {
      if (this.selectedPaymentMethod === maPhuongThuc) {
        this.selectedPaymentMethod = null;
        return;
      }
      this.selectedPaymentMethod = maPhuongThuc;
    },

    // ---- Voucher ----
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

    removeVoucher() {
      this.appliedVoucher = null;
      this.voucherError = null;
    },

    // ---- Checkout helpers ----
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
