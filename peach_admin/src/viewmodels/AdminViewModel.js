/**
 * ViewModel cốt lõi điều phối toàn bộ luồng dữ liệu quản trị (Admin Dashboard).
 * Quản lý trạng thái ứng dụng Vue, đồng bộ hóa dữ liệu thời gian thực từ các API.
 * 
 * @module AdminViewModel
 */
window.AdminViewModel = {
  /**
   * Khởi tạo các reactive state và các hàm xử lý API chính của hệ thống Admin.
   * 
   * @returns {Object} Các thuộc tính và phương thức được Vue binding trực tiếp lên UI.
   */
  setup() {
    if (typeof Vue === 'undefined') {
      console.error("Vue is not defined. Ensure Vue.js is loaded before AdminViewModel.js");
      return {};
    }
    const { ref, onMounted, onUnmounted, reactive, computed, watch } = Vue;
    
    const isSidebarCollapsed = ref(false);
    const activeTab = ref('dashboard');

    // Product Modal State
    const showProductModal = ref(false);
    const isEditingProduct = ref(false);
    const editingProductId = ref(null);
    const productForm = reactive({
      ten: '',
      danh_muc: 'iphone',
      gia: 0,
      mau_sac: '',
      ram: '',
      dung_luong: '',
      mo_ta: '',
      hinh_anh: '',
      thu_vien_anh: [],
      is_new: 1,
      so_luong_kho: 100
    });

    const activePairings = ref([]);

    const presetColors = [
      { name: 'Space Black', hex: '#1D1D1F' },
      { name: 'Silver', hex: '#E3E4E5' },
      { name: 'Starlight', hex: '#F5E3C3' },
      { name: 'Space Gray', hex: '#4F5055' },
      { name: 'Titan Blue', hex: '#3B4E5F' },
      { name: 'Deep Purple', hex: '#4B3F54' },
      { name: 'Alpine Green', hex: '#354E3B' },
      { name: 'Product Red', hex: '#C8102E' }
    ];

    const productVariantsPreview = Vue.computed(() => {
      const combos = [];
      const selectedRam = (productForm.ram || '').split(',').map(s => s.trim()).filter(Boolean);
      
      for (const pair of activePairings.value) {
        // Only show if the RAM is still selected
        if (selectedRam.includes(pair.ram)) {
          if (pair.capacities && pair.capacities.length > 0) {
            for (const cap of pair.capacities) {
              combos.push({ ram: pair.ram, capacity: cap });
            }
          } else {
            combos.push({ ram: pair.ram, capacity: null });
          }
        }
      }
      
      // Fallback if no pairings are created yet
      if (combos.length === 0) {
        const rams = (productForm.ram || '').split(',').map(s => s.trim()).filter(Boolean);
        const capacities = (productForm.dung_luong || '').split(',').map(s => s.trim()).filter(Boolean);
        
        if (rams.length > 0 && capacities.length > 0) {
          for (const r of rams) {
            for (const c of capacities) {
              combos.push({ ram: r, capacity: c });
            }
          }
        } else if (rams.length > 0) {
          for (const r of rams) {
            combos.push({ ram: r, capacity: null });
          }
        } else if (capacities.length > 0) {
          for (const c of capacities) {
            combos.push({ ram: null, capacity: c });
          }
        }
      }
      return combos;
    });

    const productColorsPreview = Vue.computed(() => {
      return (productForm.mau_sac || '').split(',').map(s => s.trim()).filter(Boolean);
    });
    const stats = ref({
      revenue: "0₫",
      newOrders: 0,
      newCustomers: 0
    });
    const activities = ref([]);
    const products = ref([]);
    const analyticsData = ref({
      revenueChart: [0, 0, 0, 0, 0, 0, 0], // Triệu VNĐ
      expenseChart: [0, 0, 0, 0, 0, 0, 0], // USD
      tokensChart: [0, 0, 0, 0, 0, 0, 0], // Triệu tokens
      requestsChart: [0, 0, 0, 0, 0, 0, 0],
      modelUsage: [],
      topProducts: [],
      summary: {
        totalRevenue: 0, // VNĐ
        totalExpenses: 0.0, // USD
        apiRequests: 0,
        tokensUsage: 0,
        inputTokens: 0,
        outputTokens: 0
      }
    });

    const analyticsTab = ref('business'); // 'business' or 'ai'
    const revenueViewMode = ref('month'); // 'day' or 'month'

    Vue.watch(revenueViewMode, () => {
      if (typeof updateAnalyticsTopProducts === 'function') {
        updateAnalyticsTopProducts();
      }
    });

    const fetchAnalytics = async () => {
      // Logic tải dữ liệu từ server
      console.log("Fetching analytics data...");
    };
    const aiLogs = ref([]);
    const aiLogSearchQuery = ref('');
    const filteredAiLogs = Vue.computed(() => {
      const q = aiLogSearchQuery.value.trim().toLowerCase();
      if (!q) return aiLogs.value;
      return aiLogs.value.filter(l => 
        l.messages && l.messages.some(msg =>
          (msg.cau_hoi && msg.cau_hoi.toLowerCase().includes(q)) ||
          (msg.tra_loi && msg.tra_loi.toLowerCase().includes(q))
        )
      );
    });
    const categories = ref([]);
    const inventoryLogs = ref([]);
    const flashSales = ref([]);
    const vouchers = ref([]);
    const shippingUnits = ref([]);
    const orders = ref([]);
    const customers = ref([]);
    const admins = ref([]);
    const paymentPartners = ref([]);
    const auditLogs = ref([]);
    const systemConfig = reactive({
      maintenanceMode: false,
      footerText: 'Bản quyền © 2026 Peach Store. Bảo lưu mọi quyền.',
      defaultLanguage: 'vi',
      accentColor: 'blue',
      typography: 'Inter',
      defaultSidebarCollapsed: false
    });
    const settingsTab = ref('general'); // 'general' or 'theme'

    const translations = {
      vi: {
        group_overview: "TỔNG QUAN",
        nav_dashboard: "Bảng điều khiển",
        nav_analytics: "Phân tích kinh doanh",
        nav_chat_history: "Lịch sử Chat Admin",
        group_inventory: "KHO & SẢN PHẨM",
        nav_products: "Danh sách sản phẩm",
        group_sales: "BÁN HÀNG & KM",
        nav_orders: "Quản lý Đơn hàng",
        nav_vouchers: "Mã giảm giá (Vouchers)",
        group_customers: "KHÁCH HÀNG & CRM",
        nav_customers: "Quản lý người dùng",
        nav_loyalty: "Tích điểm & Hạng thẻ",
        nav_push: "Gửi thông báo (Push)",
        nav_chat: "Trò chuyện & CSKH",
        nav_support: "Hỗ trợ & CSKH",
        group_system: "HỆ THỐNG",
        nav_employees: "Quản lý nhân viên",
        nav_shipping: "Vận chuyển & Phí ship",
        nav_payments: "Thanh toán & Partner",
        nav_logs: "Nhật ký Audit",
        nav_settings: "Cấu hình & CMS",
        save_changes: "Lưu thay đổi",
        general: "Chung",
        appearance: "Giao diện",
        maintenance_mode: "Chế độ bảo trì",
        maintenance_desc: "Tạm dừng toàn bộ giao dịch để nâng cấp hệ thống",
        default_lang: "Ngôn ngữ mặc định",
        default_lang_desc: "Ngôn ngữ hiển thị cho giao diện quản trị",
        footer_greeting: "Lời chào Footer",
        footer_greeting_desc: "Thông tin bản quyền hiển thị dưới chân trang",
        clean_temp: "Xóa dữ liệu nháp",
        clean_temp_desc: "Dọn dẹp các bản ghi tạm thời để tăng tốc hệ thống",
        clean_now: "Dọn dẹp ngay",
        accent_color: "Màu sắc chủ đạo",
        accent_desc: "Lựa chọn tông màu thương hiệu chính hiển thị trên trang quản trị",
        sys_font: "Phông chữ hệ thống",
        sys_font_desc: "Thay đổi kiểu phông chữ hiển thị văn bản giao diện",
        collapse_sidebar: "Thu gọn thanh bên mặc định",
        collapse_sidebar_desc: "Thu gọn Sidebar khi khởi chạy ứng dụng để tối ưu diện tích làm việc",
      },
      en: {
        group_overview: "OVERVIEW",
        nav_dashboard: "Dashboard",
        nav_analytics: "Business Analytics",
        nav_chat_history: "Admin Chat History",
        group_inventory: "INVENTORY & PRODUCTS",
        nav_products: "Products List",
        group_sales: "SALES & PROMOTIONS",
        nav_orders: "Manage Orders",
        nav_vouchers: "Discount Vouchers",
        group_customers: "CUSTOMERS & CRM",
        nav_customers: "Manage Users",
        nav_loyalty: "Loyalty & Tiers",
        nav_push: "Push Notifications",
        nav_chat: "Customer Live Chat",
        nav_support: "Support Tickets",
        group_system: "SYSTEM MANAGEMENT",
        nav_employees: "Manage Employees",
        nav_shipping: "Shipping & Rates",
        nav_payments: "Payment & Partners",
        nav_logs: "System Audit Logs",
        nav_settings: "Settings & CMS",
        save_changes: "Save Changes",
        general: "General Settings",
        appearance: "Appearance",
        maintenance_mode: "Maintenance Mode",
        maintenance_desc: "Temporarily pause storefront transactions for upgrades",
        default_lang: "Default Language",
        default_lang_desc: "The display language for this admin control panel",
        footer_greeting: "Footer Greeting",
        footer_greeting_desc: "Copyright information displayed at the bottom",
        clean_temp: "Clean Temp Data",
        clean_temp_desc: "Clean temporary records to optimize and speed up the system",
        clean_now: "Clean Now",
        accent_color: "Accent Color",
        accent_desc: "Select the primary accent color for the admin control panel",
        sys_font: "System Typography",
        sys_font_desc: "Change the active font family of the interface text",
        collapse_sidebar: "Collapse Sidebar by Default",
        collapse_sidebar_desc: "Keep the sidebar collapsed upon launching the app to maximize working space",
      }
    };

    const t = (key) => {
      const lang = systemConfig.defaultLanguage || 'vi';
      const dict = translations[lang] || translations['vi'];
      return dict[key] || key;
    };

    const applyThemeSettings = () => {
      const colors = {
        orange: '#FF9500',
        blue: '#007AFF',
        green: '#34C759',
        pink: '#FF2D55'
      };
      const selectedColor = systemConfig.accentColor || 'blue';
      const hex = colors[selectedColor] || '#007AFF';
      document.documentElement.style.setProperty('--accent', hex);
      
      const font = systemConfig.typography || 'Inter';
      document.body.style.fontFamily = `"${font}", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`;

      isSidebarCollapsed.value = !!systemConfig.defaultSidebarCollapsed;
    };

    watch(() => systemConfig.typography, () => {
      applyThemeSettings();
    });

    watch(() => systemConfig.accentColor, () => {
      applyThemeSettings();
    });

    const fetchSystemConfig = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/config');
        if (res.ok) {
          const data = await res.json();
          Object.assign(systemConfig, data);
          applyThemeSettings();
        }
      } catch (e) {
        console.error("Lỗi đồng bộ cấu hình từ backend, dùng local storage: ", e);
        const savedConfig = localStorage.getItem('peach_system_config');
        if (savedConfig) {
          try {
            const parsed = JSON.parse(savedConfig);
            Object.assign(systemConfig, parsed);
            applyThemeSettings();
          } catch (err) {
            console.error("Lỗi đọc local config: ", err);
          }
        }
      }
    };

    const saveSettings = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(systemConfig)
        });
        if (res.ok) {
          const data = await res.json();
          Object.assign(systemConfig, data.config);
        }
      } catch (e) {
        console.error("Lỗi lưu cấu hình lên backend: ", e);
      }

      localStorage.setItem('peach_system_config', JSON.stringify(systemConfig));
      applyThemeSettings();
      
      if (window.showToast) {
        window.showToast("Thành công", "Đã lưu và đồng bộ cấu hình hệ thống.", "success");
      } else {
        alert("Đã lưu cấu hình hệ thống thành công!");
      }
    };

    const cleanTempData = async () => {
      const action = async () => {
        try {
          const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/clean-temp-data', { method: 'POST' });
          if (res.ok) {
            const data = await res.json();
            if (window.showToast) {
              window.showToast("Thành công", data.cleaned.join(" "), "success");
            } else {
              alert("Đã dọn dẹp thành công:\n" + data.cleaned.join("\n"));
            }
          }
        } catch (e) {
          console.error("Lỗi dọn dẹp hệ thống: ", e);
        }
      };

      if (window.showConfirm) {
        window.showConfirm(
          'Dọn dẹp hệ thống',
          'Bạn có chắc chắn muốn dọn dẹp toàn bộ dữ liệu tạm thời để giải phóng bộ nhớ hệ thống không?',
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>`,
          action
        );
      } else {
        if (confirm('Bạn có chắc chắn muốn dọn dẹp toàn bộ dữ liệu tạm thời không?')) {
          await action();
        }
      }
    };

    Vue.onMounted(() => {
      fetchSystemConfig();
    });

    const loyaltyLevels = ref([]);
    const pushCampaigns = ref([]);
    const reviews = ref([]);
    const supportTickets = ref([]);
    const selectedSupportTicket = ref(null);
    const loadingSupportTickets = ref(false);
    const fullscreenImageUrl = ref(null);

    const fetchSupportTickets = async () => {
      loadingSupportTickets.value = true;
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/support/admin/tickets');
        if (res.ok) {
          supportTickets.value = await res.json();
        }
      } catch (e) {
        console.error("Lỗi tải ticket hỗ trợ: ", e);
      } finally {
        loadingSupportTickets.value = false;
      }
    };

    const loadingAiLogs = ref(false);
    const fetchAiLogs = async () => {
      loadingAiLogs.value = true;
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/ai-logs');
        if (res.ok) {
          aiLogs.value = await res.json();
          updateAiAnalytics();
        }
      } catch (e) {
        console.error("Lỗi tải nhật ký AI: ", e);
      } finally {
        loadingAiLogs.value = false;
      }
    };

    const deleteAiLog = async (id) => {
      const action = async () => {
        try {
          const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/ai-logs/${id}`, {
            method: 'DELETE'
          });
          if (res.ok) {
            if (window.showToast) window.showToast("Thành công", "Đã xóa một dòng lịch sử chat của Admin.", "success");
            await fetchAiLogs();
          }
        } catch (e) {
          console.error("Lỗi khi xóa dòng lịch sử chat của Admin: ", e);
        }
      };

      if (window.showConfirm) {
        window.showConfirm(
          'Xóa lịch sử chat của Admin',
          'Bạn có chắc chắn muốn xóa dòng lịch sử chat của Admin này không?',
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>`,
          action
        );
      } else {
        if (confirm("Bạn có chắc chắn muốn xóa dòng lịch sử chat của Admin này không?")) {
          await action();
        }
      }
    };

    const clearAllAiLogs = async () => {
      if (aiLogs.value.length === 0) {
        if (window.showToast) window.showToast("Thông báo", "Không có lịch sử chat của Admin nào để xóa.", "info");
        return;
      }

      const action = async () => {
        try {
          const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/ai-logs/action/clear-all', {
            method: 'DELETE'
          });
          if (res.ok) {
            if (window.showToast) window.showToast("Thành công", "Đã xóa toàn bộ lịch sử chat của Admin.", "success");
            await fetchAiLogs();
          }
        } catch (e) {
          console.error("Lỗi khi xóa toàn bộ lịch sử chat của Admin: ", e);
        }
      };

      if (window.showConfirm) {
        window.showConfirm(
          'Xóa toàn bộ lịch sử chat của Admin',
          'CẢNH BÁO: Hành động này sẽ xóa toàn bộ lịch sử truy vấn của Admin và không thể khôi phục. Bạn có chắc chắn muốn tiếp tục không?',
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>`,
          action
        );
      } else {
        if (confirm("Bạn có chắc chắn muốn xóa TOÀN BỘ lịch sử chat của Admin không?")) {
          await action();
        }
      }
    };

    const fetchPushCampaigns = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/notifications/campaigns');
        if (res.ok) {
          pushCampaigns.value = await res.json();
        }
      } catch (e) {
        console.error("Lỗi tải chiến dịch thông báo: ", e);
      }
    };

    const searchAuditQuery = ref('');
    const fetchAuditLogs = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/audit-logs');
        if (res.ok) {
          auditLogs.value = await res.json();
        }
      } catch (e) {
        console.error("Lỗi tải nhật ký audit: ", e);
      }
    };

    const filteredAuditLogs = computed(() => {
      const q = searchAuditQuery.value.trim().toLowerCase();
      if (!q) return auditLogs.value;
      return auditLogs.value.filter(l => 
        (l.user && l.user.toLowerCase().includes(q)) || 
        (l.action && l.action.toLowerCase().includes(q)) ||
        (l.ip_address && l.ip_address.toLowerCase().includes(q)) ||
        (l.id && String(l.id).includes(q))
      );
    });

    /**
     * Cập nhật trạng thái xử lý cho một yêu cầu hỗ trợ khách hàng (Support Ticket).
     * 
     * @param {number} ticketId - ID của ticket cần sửa đổi.
     * @param {string} status - Trạng thái mới (ví dụ: 'da_xu_ly', 'dang_cho').
     */
    const updateSupportTicketStatus = async (ticketId, status) => {
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/support/admin/tickets/${ticketId}/status`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ trang_thai: status })
        });
        if (res.ok) {
          if (window.showToast) window.showToast("Thành công", "Đã cập nhật trạng thái yêu cầu hỗ trợ.", "success");
          await fetchSupportTickets();
          if (selectedSupportTicket.value && selectedSupportTicket.value.id === ticketId) {
            selectedSupportTicket.value = supportTickets.value.find(t => t.id === ticketId) || null;
          }
        }
      } catch (e) {
        console.error("Lỗi cập nhật trạng thái ticket: ", e);
      }
    };

    const showLoyaltyModal = ref(false);
    const loyaltyForm = reactive({
      id: null,
      ten_hang: '',
      diem_toi_thieu: 0,
      phan_tram_giam: 0,
      uu_dai_rieng: '',
      color: '#8e8e93'
    });

    const showPointsModal = ref(false);
    const pointsForm = reactive({
      customerId: null,
      customerName: '',
      diem_tich_luy: 0
    });

    const fetchLoyaltyLevels = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/loyalty-configs');
        if (res.ok) {
          loyaltyLevels.value = await res.json();
        }
      } catch (e) {
        console.error("Lỗi tải cấu hình loyalty: ", e);
      }
    };

    const openEditLoyaltyModal = (level) => {
      loyaltyForm.id = level.id;
      loyaltyForm.ten_hang = level.ten_hang;
      loyaltyForm.diem_toi_thieu = level.diem_toi_thieu;
      loyaltyForm.phan_tram_giam = level.phan_tram_giam;
      loyaltyForm.uu_dai_rieng = level.uu_dai_rieng ? level.uu_dai_rieng.join(';') : '';
      loyaltyForm.color = level.color || '#8e8e93';
      showLoyaltyModal.value = true;
    };

    const hasPrivilege = (privilege) => {
      if (!loyaltyForm.uu_dai_rieng) return false;
      const list = loyaltyForm.uu_dai_rieng.split(';').map(item => item.trim());
      return list.includes(privilege);
    };

    const togglePrivilege = (privilege) => {
      let list = loyaltyForm.uu_dai_rieng ? loyaltyForm.uu_dai_rieng.split(';').map(item => item.trim()).filter(Boolean) : [];
      if (list.includes(privilege)) {
        list = list.filter(item => item !== privilege);
      } else {
        list.push(privilege);
      }
      loyaltyForm.uu_dai_rieng = list.join(';');
    };

    const saveLoyaltyConfig = async () => {
      try {
        const pts = parseInt(loyaltyForm.diem_toi_thieu) || 0;
        if (pts > 100000000) {
          if (window.showToast) window.showToast("Lỗi nhập liệu", "Ngưỡng điểm tối đa là 100,000,000.", "error");
          return;
        }
        if (pts < 0) {
          if (window.showToast) window.showToast("Lỗi nhập liệu", "Ngưỡng điểm không được nhỏ hơn 0.", "error");
          return;
        }

        const pct = parseFloat(loyaltyForm.phan_tram_giam) || 0;
        if (pct > 100) {
          if (window.showToast) window.showToast("Lỗi nhập liệu", "Phần trăm giảm giá tối đa là 100%.", "error");
          return;
        }
        if (pct < 0) {
          if (window.showToast) window.showToast("Lỗi nhập liệu", "Phần trăm giảm giá không được nhỏ hơn 0.", "error");
          return;
        }

        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/loyalty-configs/${loyaltyForm.id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            diem_toi_thieu: pts,
            phan_tram_giam: pct,
            uu_dai_rieng: loyaltyForm.uu_dai_rieng,
            color: loyaltyForm.color
          })
        });
        if (res.ok) {
          if (window.showToast) window.showToast("Thành công", "Đã cập nhật cấu hình hạng thành viên.", "success");
          showLoyaltyModal.value = false;
          await fetchLoyaltyLevels();
          if (typeof fetchAuditLogs === 'function') fetchAuditLogs();
        }
      } catch (e) {
        console.error("Lỗi lưu cấu hình loyalty: ", e);
      }
    };

    const openEditPointsModal = (customer) => {
      pointsForm.customerId = customer.id;
      pointsForm.customerName = customer.ho_ten || customer.email || 'Khách hàng';
      pointsForm.diem_tich_luy = customer.diem_tich_luy || 0;
      showPointsModal.value = true;
    };

    const saveCustomerPoints = async () => {
      try {
        const pts = parseInt(pointsForm.diem_tich_luy) || 0;
        if (pts > 100000000) {
          if (window.showToast) window.showToast("Lỗi nhập liệu", "Điểm tích lũy tối đa là 100,000,000.", "error");
          return;
        }
        if (pts < 0) {
          if (window.showToast) window.showToast("Lỗi nhập liệu", "Điểm tích lũy không được nhỏ hơn 0.", "error");
          return;
        }

        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/customers/${pointsForm.customerId}/points`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            diem_tich_luy: pts
          })
        });
        if (res.ok) {
          if (window.showToast) window.showToast("Thành công", "Đã cập nhật điểm tích lũy của khách hàng.", "success");
          showPointsModal.value = false;
          await fetchCustomers();
          if (typeof fetchAuditLogs === 'function') fetchAuditLogs();
        }
      } catch (e) {
        console.error("Lỗi cập nhật điểm khách hàng: ", e);
      }
    };

    const activeStatusMenu = ref(null);

    const stringToColor = (str) => {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
      }
      const c = (hash & 0x00FFFFFF).toString(16).toUpperCase();
      return "#" + "00000".substring(0, 6 - c.length) + c;
    };

    const toggleStatusMenu = (orderId) => {
      if (activeStatusMenu.value === orderId) {
        activeStatusMenu.value = null;
      } else {
        activeStatusMenu.value = orderId;
      }
    };

    const commonCapacities = [
      '128MB', '256MB', '512MB', 
      '64GB', '128GB', '256GB', '512GB', 
      '1TB', '2TB', '4TB'
    ];

    const commonRams = [
      '4GB', '8GB', '12GB', '16GB', '24GB', '32GB', '64GB', '128GB'
    ];

    const isCapacitySelected = (cap) => {
      const selected = (productForm.dung_luong || '').split(',').map(s => s.trim());
      return selected.includes(cap);
    };

    const toggleCapacity = (cap) => {
      let selected = (productForm.dung_luong || '').split(',')
        .map(s => s.trim())
        .filter(s => s !== '');
      
      if (selected.includes(cap)) {
        selected = selected.filter(s => s !== cap);
      } else {
        selected.push(cap);
      }
      
      productForm.dung_luong = selected.join(', ');
    };

    const isRamSelected = (ram) => {
      const selected = (productForm.ram || '').split(',').map(s => s.trim());
      return selected.includes(ram);
    };

    const toggleRam = (ram) => {
      let selected = (productForm.ram || '').split(',')
        .map(s => s.trim())
        .filter(s => s !== '');
      
      if (selected.includes(ram)) {
        selected = selected.filter(s => s !== ram);
        activePairings.value = activePairings.value.filter(p => p.ram !== ram);
      } else {
        selected.push(ram);
        if (!activePairings.value.some(p => p.ram === ram)) {
          activePairings.value.push({ ram, capacities: [] });
        }
      }
      
      productForm.ram = selected.join(', ');
    };

    const togglePairCapacity = (ram, cap) => {
      let pair = activePairings.value.find(p => p.ram === ram);
      if (!pair) {
        pair = { ram, capacities: [] };
        activePairings.value.push(pair);
      }
      if (pair.capacities.includes(cap)) {
        pair.capacities = pair.capacities.filter(c => c !== cap);
      } else {
        pair.capacities.push(cap);
      }
    };
    
    const isPairCapacitySelected = (ram, cap) => {
      const pair = activePairings.value.find(p => p.ram === ram);
      return pair ? pair.capacities.includes(cap) : false;
    };

    const toggleColor = (hex) => {
      let colors = (productForm.mau_sac || '').split(',')
        .map(s => s.trim())
        .filter(Boolean);
      
      if (colors.includes(hex)) {
        colors = colors.filter(c => c !== hex);
      } else {
        if (colors.length >= 5) {
          if (window.showToast) window.showToast("Giới hạn màu", "Tối đa chỉ được chọn 5 màu sắc.", "warning");
          return;
        }
        colors.push(hex);
      }
      productForm.mau_sac = colors.join(', ');
    };

    const tempColor = ref('');

    const addTempColor = () => {
      const hex = tempColor.value.trim();
      if (!hex) return;
      if (!/^#[0-9A-F]{6}$/i.test(hex)) {
        window.showToast?.('Cảnh báo', 'Định dạng màu HEX không hợp lệ (ví dụ: #FF0000).', 'warning');
        return;
      }
      toggleColor(hex);
      tempColor.value = '';
    };

    const cleanDescription = (text) => {
      if (!text) return '—';
      return text.replace(/<!--SPECS_PAIRINGS:(.*?)-->/, '').trim();
    };

    const getProductSpecsList = (product) => {
      if (!product) return [];
      
      let pairings = [];
      const match = (product.mo_ta || '').match(/<!--SPECS_PAIRINGS:(.*?)-->/);
      if (match) {
        try {
          pairings = JSON.parse(match[1]);
        } catch (e) {
          console.error("Lỗi giải mã pairings trong list:", e);
        }
      }
      
      const combos = [];
      const selectedRam = (product.ram || '').split(',').map(s => s.trim()).filter(Boolean);
      const selectedCapacity = (product.dung_luong || '').split(',').map(s => s.trim()).filter(Boolean);
      
      if (pairings && pairings.length > 0) {
        for (const pair of pairings) {
          if (pair.ram) {
            const isRamStillValid = selectedRam.includes(pair.ram);
            if (isRamStillValid) {
              if (pair.capacities && pair.capacities.length > 0) {
                for (const cap of pair.capacities) {
                  if (selectedCapacity.includes(cap)) {
                    combos.push(`${pair.ram}/${cap}`);
                  }
                }
              } else {
                combos.push(pair.ram);
              }
            }
          } else {
            if (pair.capacities && pair.capacities.length > 0) {
              for (const cap of pair.capacities) {
                if (selectedCapacity.includes(cap)) {
                  combos.push(cap);
                }
              }
            }
          }
        }
      }
      
      // Fallback: if no combos, pair all selected RAMs and capacities
      if (combos.length === 0) {
        if (selectedRam.length > 0 && selectedCapacity.length > 0) {
          for (const r of selectedRam) {
            for (const c of selectedCapacity) {
              combos.push(`${r}/${c}`);
            }
          }
        } else if (selectedRam.length > 0) {
          combos.push(...selectedRam);
        } else if (selectedCapacity.length > 0) {
          combos.push(...selectedCapacity);
        }
      }
      
      return [...new Set(combos)];
    };

    const onNativeColorPicked = (event) => {
      const hex = event.target.value;
      if (hex) {
        tempColor.value = hex;
      }
    };

    function docSoTien(number) {
      if (!number || number === 0) return "0 đồng";
      if (number >= 1000000000) {
        const val = number / 1000000000;
        const formatted = Number(val.toFixed(2)).toLocaleString('vi-VN');
        return `~ ${formatted} tỷ đồng`;
      }
      if (number >= 1000000) {
        const val = number / 1000000;
        const formatted = Number(val.toFixed(2)).toLocaleString('vi-VN');
        return `~ ${formatted} triệu đồng`;
      }
      if (number >= 1000) {
        const val = number / 1000;
        const formatted = Number(val.toFixed(2)).toLocaleString('vi-VN');
        return `~ ${formatted} nghìn đồng`;
      }
      return `${number.toLocaleString('vi-VN')} đồng`;
    }

    const updateAnalyticsTopProducts = () => {
      const productSales = {};
      
      orders.value.forEach(order => {
        if (order.status !== 'da_huy') {
          (order.items || []).forEach(item => {
            const name = item.name || 'Sản phẩm không tên';
            const qty = Number(item.qty) || 0;
            productSales[name] = (productSales[name] || 0) + qty;
          });
        }
      });

      const sortedProducts = Object.keys(productSales).map(name => ({
        name: name,
        sales: productSales[name]
      })).sort((a, b) => b.sales - a.sales);

      analyticsData.value.topProducts = sortedProducts.slice(0, 5);



      if (revenueViewMode.value === 'day') {
        const dailyBuckets = [0, 0, 0, 0, 0, 0, 0];
        const dailyLabels = [];
        
        for (let i = 6; i >= 0; i--) {
          const d = new Date();
          d.setDate(d.getDate() - i);
          const dayStr = `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`;
          dailyLabels.push(dayStr);
        }

        orders.value.forEach(order => {
          if (order.status !== 'da_huy') {
            const orderDate = new Date(order.date);
            if (!isNaN(orderDate.getTime())) {
              const today = new Date();
              today.setHours(23, 59, 59, 999);
              const diffTime = today - orderDate;
              const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
              if (diffDays >= 0 && diffDays < 7) {
                dailyBuckets[6 - diffDays] += Number(order.total) || 0;
              }
            }
          }
        });

        analyticsData.value.revenueChart = dailyBuckets.map(val => Number((val / 1000000).toFixed(1)));
        analyticsData.value.revenueChartLabels = dailyLabels;
        

      } else {
        const weeklyBuckets = [0, 0, 0, 0, 0];
        const weeklyLabels = ["Tuần 1", "Tuần 2", "Tuần 3", "Tuần 4", "Tuần 5"];

        orders.value.forEach(order => {
          if (order.status !== 'da_huy') {
            const orderDate = new Date(order.date);
            if (!isNaN(orderDate.getTime())) {
              const day = orderDate.getDate();
              let weekIdx = 0;
              if (day <= 7) weekIdx = 0;
              else if (day <= 14) weekIdx = 1;
              else if (day <= 21) weekIdx = 2;
              else if (day <= 28) weekIdx = 3;
              else weekIdx = 4;
              
              weeklyBuckets[weekIdx] += Number(order.total) || 0;
            }
          }
        });

        analyticsData.value.revenueChart = weeklyBuckets.map(val => Number((val / 1000000).toFixed(1)));
        analyticsData.value.revenueChartLabels = weeklyLabels;


      }
    };

    const updateAiAnalytics = () => {
      let totalInputTokens = 0;
      let totalOutputTokens = 0;
      let totalRequests = 0;

      aiLogs.value.forEach(session => {
        if (session.messages && session.messages.length > 0) {
          session.messages.forEach(msg => {
            totalRequests++;
            const qCharCount = msg.cau_hoi ? msg.cau_hoi.length : 0;
            const aCharCount = msg.tra_loi ? msg.tra_loi.length : 0;
            
            const inTokens = Math.ceil(qCharCount / 3) + 120;
            const outTokens = Math.ceil(aCharCount / 3);
            
            totalInputTokens += inTokens;
            totalOutputTokens += outTokens;
          });
        }
      });

      const totalTokens = totalInputTokens + totalOutputTokens;
      // DeepSeek pricing model
      const inputCost = (totalInputTokens / 1000000) * 0.14;
      const outputCost = (totalOutputTokens / 1000000) * 0.28;
      const totalCostUSD = inputCost + outputCost;

      analyticsData.value.summary.apiRequests = totalRequests;
      analyticsData.value.summary.tokensUsage = totalTokens;
      analyticsData.value.summary.inputTokens = totalInputTokens;
      analyticsData.value.summary.outputTokens = totalOutputTokens;
      analyticsData.value.summary.totalExpenses = totalCostUSD;

      const activeModel = localStorage.getItem('peach_ai_model') || 'deepseek-chat';
      const modelDisplayName = activeModel === 'deepseek-chat' ? 'DeepSeek-V3' : activeModel;
      
      analyticsData.value.modelUsage = [
        { 
          name: modelDisplayName, 
          requests: totalRequests, 
          cost: Number(totalCostUSD.toFixed(5)), 
          tokens: totalTokens >= 1000000 ? `${(totalTokens / 1000000).toFixed(2)}M` : totalTokens.toLocaleString() 
        }
      ];

      if (totalTokens === 0) {
        analyticsData.value.tokensChart = [0.0012, 0.0028, 0.0015, 0.0035, 0.0058, 0.0042, 0.0065];
      } else {
        const tokenM = totalTokens / 1000000;
        analyticsData.value.tokensChart = [
          Number((tokenM * 0.15).toFixed(4)),
          Number((tokenM * 0.3).toFixed(4)),
          Number((tokenM * 0.45).toFixed(4)),
          Number((tokenM * 0.6).toFixed(4)),
          Number((tokenM * 0.75).toFixed(4)),
          Number((tokenM * 0.9).toFixed(4)),
          Number(tokenM.toFixed(4))
        ];
      }

      if (totalRequests === 0) {
        analyticsData.value.requestsChart = [2, 4, 3, 5, 8, 6, 9];
      } else {
        analyticsData.value.requestsChart = [
          Math.max(1, Math.ceil(totalRequests * 0.15)),
          Math.max(1, Math.ceil(totalRequests * 0.3)),
          Math.max(1, Math.ceil(totalRequests * 0.45)),
          Math.max(1, Math.ceil(totalRequests * 0.6)),
          Math.max(1, Math.ceil(totalRequests * 0.75)),
          Math.max(1, Math.ceil(totalRequests * 0.9)),
          totalRequests
        ];
      }
    };

    const formatTokens = (tokens) => {
      if (tokens >= 1000000) {
        return (tokens / 1000000).toFixed(2) + "M";
      }
      if (tokens >= 1000) {
        return (tokens / 1000).toFixed(1) + "k";
      }
      return tokens.toLocaleString('vi-VN');
    };

    const requestsSvgPoints = Vue.computed(() => {
      const chart = analyticsData.value.requestsChart || [0,0,0,0,0,0,0];
      const maxVal = Math.max(...chart, 1);
      const points = chart.map((v, i) => {
        const x = (i / (chart.length - 1)) * 400;
        const y = 100 - (v / maxVal) * 80;
        return `${x},${y}`;
      });
      return points.join(' ');
    });

    const requestsSvgAreaPoints = Vue.computed(() => {
      const chart = analyticsData.value.requestsChart || [0,0,0,0,0,0,0];
      const maxVal = Math.max(...chart, 1);
      const points = chart.map((v, i) => {
        const x = (i / (chart.length - 1)) * 400;
        const y = 100 - (v / maxVal) * 80;
        return `${x},${y}`;
      });
      return `0,100 ${points.join(' ')} 400,100`;
    });

    const fetchStats = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/dashboard/stats');
        const data = await res.json();
        stats.value = {
          revenue: new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(data.revenue || 0),
          revenueInWords: docSoTien(data.revenue || 0),
          newOrders: data.order_count || 0,
          newCustomers: data.user_count || 0
        };
        // Cập nhật doanh thu trong phân tích kinh doanh để đồng bộ
        if (analyticsData.value && analyticsData.value.summary) {
          analyticsData.value.summary.totalRevenue = data.revenue || 0;
        }
      } catch (e) { console.error("Lỗi tải thống kê: ", e); }
    };

    const fetchActivities = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/activities');
        activities.value = await res.json();
      } catch (e) { console.error("Lỗi tải hoạt động: ", e); }
    };

    const fetchProducts = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/san-pham/');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        products.value = await res.json();
      } catch (e) { 
        console.error("Lỗi tải sản phẩm: ", e);
        // Alert to help user debug
        if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới Backend API tại port 8000.", "warning");
      }
    };

    // Product form validation errors
    const productFormErrors = reactive({
      ten: '',
      gia: '',
      hinh_anh: '',
      mo_ta: '',
      mau_sac: '',
      thu_vien_anh: '',
      so_luong_kho: ''
    });

    const validateProductForm = () => {
      let valid = true;
      productFormErrors.ten = '';
      productFormErrors.gia = '';
      productFormErrors.hinh_anh = '';
      productFormErrors.mo_ta = '';
      productFormErrors.mau_sac = '';
      productFormErrors.thu_vien_anh = '';
      productFormErrors.so_luong_kho = '';

      // 1. Limit product name to 150 characters
      if (!productForm.ten || !productForm.ten.trim()) {
        productFormErrors.ten = 'Vui lòng nhập tên sản phẩm';
        valid = false;
      } else if (productForm.ten.length > 150) {
        productFormErrors.ten = 'Tên sản phẩm tối đa 150 ký tự';
        valid = false;
      }

      // 2. Limit price to 100 billion VND
      if (productForm.gia === undefined || productForm.gia === null || productForm.gia <= 0) {
        productFormErrors.gia = 'Vui lòng nhập giá sản phẩm hợp lệ';
        valid = false;
      } else if (productForm.gia > 100000000000) {
        productFormErrors.gia = 'Giá sản phẩm tối đa là 100 tỷ VNĐ';
        valid = false;
      }

      // 3. Validate main image
      if (!productForm.hinh_anh || !productForm.hinh_anh.trim()) {
        productFormErrors.hinh_anh = 'Vui lòng nhập URL hình ảnh';
        valid = false;
      }

      // 4. Limit colors to maximum 5
      const colors = (productForm.mau_sac || '').split(',').map(s => s.trim()).filter(Boolean);
      if (colors.length > 5) {
        productFormErrors.mau_sac = 'Tối đa chỉ được chọn 5 màu sắc';
        valid = false;
      }

      // 5. Limit description to 500 words
      const wordCount = (productForm.mo_ta || '').trim().split(/\s+/).filter(Boolean).length;
      if (wordCount > 500) {
        productFormErrors.mo_ta = `Mô tả tối đa 500 từ (Hiện tại: ${wordCount} từ)`;
        valid = false;
      }

      // 7. Validate stock quantity
      if (productForm.so_luong_kho === undefined || productForm.so_luong_kho === null || productForm.so_luong_kho === '') {
        productFormErrors.so_luong_kho = 'Vui lòng nhập số lượng tồn kho';
        valid = false;
      } else if (Number(productForm.so_luong_kho) < 0) {
        productFormErrors.so_luong_kho = 'Số lượng tồn kho phải >= 0';
        valid = false;
      } else if (Number(productForm.so_luong_kho) > 1000) {
        productFormErrors.so_luong_kho = 'Số lượng tồn kho tối đa là 1000 máy';
        valid = false;
      }

      return valid;
    };

    const openAddProductModal = () => {
      isEditingProduct.value = false;
      Object.assign(productForm, { ten: '', danh_muc: 'iphone', gia: 0, mau_sac: '', ram: '', dung_luong: '', mo_ta: '', hinh_anh: '', thu_vien_anh: [], is_new: 1, so_luong_kho: 100 });
      activePairings.value = [];
      productFormErrors.ten = '';
      productFormErrors.gia = '';
      productFormErrors.hinh_anh = '';
      productFormErrors.mo_ta = '';
      productFormErrors.mau_sac = '';
      productFormErrors.thu_vien_anh = '';
      productFormErrors.so_luong_kho = '';
      showProductModal.value = true;
    };

    const openEditProductModal = (product) => {
      isEditingProduct.value = true;
      editingProductId.value = product.id;
      
      // Extract clean description and spec pairings metadata
      let cleanDescription = product.mo_ta || '';
      let pairings = [];
      const match = cleanDescription.match(/<!--SPECS_PAIRINGS:(.*?)-->/);
      if (match) {
        try {
          pairings = JSON.parse(match[1]);
          cleanDescription = cleanDescription.replace(/<!--SPECS_PAIRINGS:(.*?)-->/, '').trim();
        } catch (e) {
          console.error("Lỗi giải mã pairings:", e);
        }
      }
      
      Object.assign(productForm, { 
        ...product,
        mo_ta: cleanDescription
      });
      
      // Fallback: If no custom pairings found, pair all selected RAMs with all selected capacities
      if (pairings.length === 0) {
        const rams = (productForm.ram || '').split(',').map(s => s.trim()).filter(Boolean);
        const capacities = (productForm.dung_luong || '').split(',').map(s => s.trim()).filter(Boolean);
        for (const r of rams) {
          pairings.push({ ram: r, capacities: [...capacities] });
        }
      }
      
      activePairings.value = pairings;
      
      productFormErrors.ten = '';
      productFormErrors.gia = '';
      productFormErrors.hinh_anh = '';
      productFormErrors.mo_ta = '';
      productFormErrors.mau_sac = '';
      productFormErrors.thu_vien_anh = '';
      productFormErrors.so_luong_kho = '';
      showProductModal.value = true;
    };

    const saveProduct = async () => {
      if (!validateProductForm()) {
        if (window.showToast) window.showToast("Lỗi nhập liệu", "Vui lòng kiểm tra lại các thông tin sản phẩm.", "warning");
        return;
      }
      
      // Automatically synchronize unique capacities from active pairings to DB field productForm.dung_luong
      const uniqueCapacities = [];
      const selectedRam = (productForm.ram || '').split(',').map(s => s.trim()).filter(Boolean);
      for (const pair of activePairings.value) {
        if (selectedRam.includes(pair.ram)) {
          for (const cap of pair.capacities) {
            if (!uniqueCapacities.includes(cap)) {
              uniqueCapacities.push(cap);
            }
          }
        }
      }
      if (uniqueCapacities.length > 0) {
        productForm.dung_luong = uniqueCapacities.join(', ');
      }
      
      // Serialize active pairings to a hidden metadata comment block in the product description
      const cleanDescription = (productForm.mo_ta || '').replace(/<!--SPECS_PAIRINGS:(.*?)-->/, '').trim();
      const metadata = `\n\n<!--SPECS_PAIRINGS:${JSON.stringify(activePairings.value)}-->`;
      
      const payload = {
        ...productForm,
        mo_ta: cleanDescription + metadata
      };

      try {
        const url = isEditingProduct.value 
          ? `${window.API_BASE || 'http://127.0.0.1:8000'}/san-pham/${editingProductId.value}`
          : (window.API_BASE || 'http://127.0.0.1:8000') + '/san-pham/';
        
        const method = isEditingProduct.value ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
          method: method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          showProductModal.value = false;
          fetchProducts();
          if (window.showToast) window.showToast("Thành công", "Đã lưu sản phẩm thành công.", "success");
        } else {
          const errorData = await res.json();
          const errorMsg = errorData.detail ? JSON.stringify(errorData.detail) : "Lỗi không xác định";
          alert("Lỗi từ Server: " + errorMsg);
        }
      } catch (e) { 
        console.error("Lỗi khi lưu sản phẩm: ", e);
        alert("Lỗi kết nối khi lưu sản phẩm."); 
      }
    };

    const deleteProduct = (id) => {
      if (window.showConfirm) {
        window.showConfirm(
          'Xác nhận xóa sản phẩm',
          'Bạn có chắc chắn muốn xóa sản phẩm này? Thao tác này không thể hoàn tác.',
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/san-pham/${id}`, { method: 'DELETE' });
              if (res.ok) {
                fetchProducts();
                if (window.showToast) window.showToast("Thành công", "Đã xóa sản phẩm thành công.", "success");
              } else {
                if (window.showToast) window.showToast("Lỗi", "Không thể xóa sản phẩm.", "error");
              }
            } catch (e) {
              console.error("Lỗi khi xóa sản phẩm: ", e);
              if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
            }
          }
        );
      } else {
        if (!confirm("Bạn có chắc chắn muốn xóa sản phẩm này?")) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/san-pham/${id}`, { method: 'DELETE' })
          .then(res => { if (res.ok) fetchProducts(); })
          .catch(e => console.error("Lỗi khi xóa sản phẩm"));
      }
    };

    const filterQuery = ref('');
    const selectedCategory = ref('');
    const voucherFilterQuery = ref('');

    const productSortKey = ref('id');
    const productSortOrder = ref('desc'); // Default to newly added first (ID descending)

    const sortProducts = (key) => {
      if (productSortKey.value === key) {
        productSortOrder.value = productSortOrder.value === 'asc' ? 'desc' : 'asc';
      } else {
        productSortKey.value = key;
        productSortOrder.value = 'desc';
      }
    };


    const filteredProducts = Vue.computed(() => {
      let result = [...products.value];
      
      if (selectedCategory.value) {
        result = result.filter(p => p.danh_muc === selectedCategory.value);
      }
      
      if (filterQuery.value) {
        const q = filterQuery.value.toLowerCase();
        result = result.filter(p => 
          p.ten.toLowerCase().includes(q) || 
          p.id.toString().includes(q)
        );
      }

      result.sort((a, b) => {
        let valA = a[productSortKey.value];
        let valB = b[productSortKey.value];
        
        // Handle numeric or string comparison
        if (typeof valA === 'string') {
          valA = valA.toLowerCase();
          valB = (valB || '').toLowerCase();
        }
        
        if (productSortOrder.value === 'desc') {
          return valA < valB ? 1 : -1;
        } else {
          return valA > valB ? 1 : -1;
        }
      });
      
      return result;
    });

    const filteredVouchers = Vue.computed(() => {
      if (!voucherFilterQuery.value) return vouchers.value;
      const q = voucherFilterQuery.value.toLowerCase();
      return vouchers.value.filter(v =>
        v.ma_voucher.toLowerCase().includes(q)
      );
    });

    const formatPrice = (value) => {
      return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
    };

    const formatDate = (dateStr) => {
      if (!dateStr) return '—';
      const d = new Date(dateStr);
      return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
    };


    const handleFileUpload = async (event) => {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      try {
        if (window.showToast) window.showToast("Thông báo", "Đang tải ảnh lên...", "info");
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/upload', {
          method: 'POST',
          body: formData
        });
        
        if (res.ok) {
          const data = await res.json();
          if (data.url) {
            console.log(">>> URL ảnh nhận được:", data.url);
            productForm.hinh_anh = data.url;
            if (window.showToast) window.showToast("Thành công", "Đã tải ảnh lên.", "success");
          }
        } else {
          const err = await res.json();
          console.error(">>> Lỗi upload:", err);
          if (window.showToast) window.showToast("Lỗi tải ảnh", err.detail || "Không thể tải ảnh", "warning");
        }
      } catch (e) {
        console.error("Lỗi khi tải ảnh: ", e);
        if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
      }
    };

    const handleGalleryUpload = async (event) => {
      const files = event.target.files;
      if (!files.length) return;

      if (window.showToast) window.showToast("Thông báo", `Đang tải ${files.length} ảnh lên...`, "info");
      for (let i = 0; i < files.length; i++) {
        const formData = new FormData();
        formData.append('file', files[i]);

        try {
          const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/upload', {
            method: 'POST',
            body: formData
          });
          
          if (res.ok) {
            const data = await res.json();
            if (data.url) {
              if (!productForm.thu_vien_anh) productForm.thu_vien_anh = [];
              productForm.thu_vien_anh.push(data.url);
            }
          } else {
            const err = await res.json();
            if (window.showToast) window.showToast("Lỗi", `Ảnh thứ ${i+1}: ${err.detail}`, "warning");
          }
        } catch (e) {
          console.error("Lỗi khi tải ảnh thư viện: ", e);
        }
      }
      if (window.showToast) window.showToast("Thành công", "Đã cập nhật thư viện ảnh.", "success");
    };


    const onSidebarToggle = (isCollapsed) => {
      isSidebarCollapsed.value = isCollapsed;
    };


    const fetchOrders = async () => {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/don-hang/admin/all', {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
          const data = await res.json();
          if (data.length === 0) {
            console.warn("API trả về danh sách đơn hàng trống.");
          }
          orders.value = data.map(o => ({
            id: o.id,
            customer: o.ten_khach_hang,
            total: o.tong_tien,
            status: o.trang_thai,
            address: o.dia_chi,
            phone: o.so_dien_thoai,
            date: o.ngay_tao,
            items: (o.items || []).map(item => ({
              name: item.san_pham ? item.san_pham.ten : 'Sản phẩm đã xóa',
              image: item.san_pham ? item.san_pham.hinh_anh : '',
              qty: item.so_luong,
              price: item.gia,
              mau_sac: item.mau_sac,
              dung_luong: item.dung_luong,
              ram: item.ram
            })),
            paymentMethod: o.phuong_thuc_thanh_toan || '',
            shippingMethod: o.phuong_thuc_van_chuyen || '',
            shippingFee: o.phi_ship || 0,
            voucherDiscount: o.giam_gia_voucher || 0,
            imei: o.imei || '',
            warranty_months: o.warranty_months || 6
          }));
          updateAnalyticsTopProducts();
        } else {
          const errData = await res.json();
          console.error("Lỗi API Admin:", errData);
        }
      } catch (e) { 
        console.error("Lỗi kết nối API Admin: ", e);
        if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới Backend tại port 8000.", "error");
      }
    };

    const deleteOrder = (id) => {
      if (window.showConfirm) {
        window.showConfirm(
          'Xác nhận xóa đơn hàng',
          `Bạn có chắc chắn muốn xóa đơn hàng #${id}? Hành động này sẽ xóa vĩnh viễn dữ liệu khỏi hệ thống.`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/don-hang/admin/xoa/${id}`, { 
                method: 'DELETE'
              });
              if (res.ok) {
                fetchOrders();
                if (window.showToast) window.showToast("Thành công", "Đã xóa đơn hàng vĩnh viễn.", "success");
              } else {
                if (window.showToast) window.showToast("Lỗi", "Không thể xóa đơn hàng.", "error");
              }
            } catch (e) { 
              console.error("Lỗi khi xóa đơn hàng: ", e);
              if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
            }
          }
        );
      } else {
        if (!confirm(`Bạn có chắc muốn xóa đơn hàng #${id}?`)) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/don-hang/admin/xoa/${id}`, { method: 'DELETE' })
          .then(res => { if (res.ok) fetchOrders(); })
          .catch(e => console.error("Lỗi xóa đơn hàng"));
      }
    };

    const selectedOrderIds = ref([]);

    const toggleOrderSelection = (id) => {
      const idx = selectedOrderIds.value.indexOf(id);
      if (idx > -1) {
        selectedOrderIds.value.splice(idx, 1);
      } else {
        selectedOrderIds.value.push(id);
      }
    };

    const toggleSelectAllOrders = (ordersList) => {
      if (selectedOrderIds.value.length === ordersList.length && ordersList.length > 0) {
        selectedOrderIds.value = [];
      } else {
        selectedOrderIds.value = ordersList.map(o => o.id);
      }
    };

    const deleteSelectedOrders = () => {
      if (selectedOrderIds.value.length === 0) return;
      
      if (window.showConfirm) {
        window.showConfirm(
          'Xác nhận xóa hàng loạt',
          `Bạn có chắc chắn muốn xóa vĩnh viễn ${selectedOrderIds.value.length} đơn hàng đã chọn? Hành động này không thể hoàn tác.`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/don-hang/admin/xoa-nhieu`, { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(selectedOrderIds.value)
              });
              if (res.ok) {
                selectedOrderIds.value = [];
                fetchOrders();
                if (window.showToast) window.showToast("Thành công", "Đã xóa hàng loạt đơn hàng.", "success");
              } else {
                if (window.showToast) window.showToast("Lỗi", "Không thể xóa hàng loạt đơn hàng.", "error");
              }
            } catch (e) { 
              console.error("Lỗi xóa hàng loạt:", e);
              if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
            }
          }
        );
      } else {
        if (!confirm(`Xóa vĩnh viễn ${selectedOrderIds.value.length} đơn hàng?`)) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/don-hang/admin/xoa-nhieu`, { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(selectedOrderIds.value)
        }).then(res => { if (res.ok) { selectedOrderIds.value = []; fetchOrders(); } });
      }
    };
    const selectedProductIds = ref([]);

    const toggleSelectAllProducts = (productsList) => {
      if (selectedProductIds.value.length === productsList.length && productsList.length > 0) {
        selectedProductIds.value = [];
      } else {
        selectedProductIds.value = productsList.map(p => p.id);
      }
    };

    const deleteSelectedProducts = () => {
      if (selectedProductIds.value.length === 0) return;
      
      if (window.showConfirm) {
        window.showConfirm(
          'Xác nhận xóa hàng loạt',
          `Bạn có chắc chắn muốn xóa vĩnh viễn ${selectedProductIds.value.length} sản phẩm đã chọn? Hành động này không thể hoàn tác.`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              // API call for bulk delete products
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/san-pham/xoa-nhieu`, { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(selectedProductIds.value)
              });
              if (res.ok) {
                selectedProductIds.value = [];
                fetchProducts();
                if (window.showToast) window.showToast("Thành công", "Đã xóa hàng loạt sản phẩm.", "success");
              } else {
                if (window.showToast) window.showToast("Lỗi", "Không thể xóa hàng loạt sản phẩm.", "error");
              }
            } catch (e) { 
              console.error("Lỗi xóa hàng loạt sản phẩm:", e);
              if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
            }
          }
        );
      } else {
        if (!confirm(`Xóa vĩnh viễn ${selectedProductIds.value.length} sản phẩm?`)) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/san-pham/xoa-nhieu`, { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(selectedProductIds.value)
        }).then(res => { if (res.ok) { selectedProductIds.value = []; fetchProducts(); } });
      }
    };

    const updateOrderStatus = async (orderId, newStatus) => {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/don-hang/cap-nhat-trang-thai/${orderId}`, {
          method: 'PUT',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` 
          },
          body: JSON.stringify({ trang_thai: newStatus })
        });
        if (res.ok) {
          if (window.showToast) window.showToast("Thành công", "Đã cập nhật trạng thái đơn hàng.", "success");
          activeStatusMenu.value = null;
          fetchOrders();
        }
      } catch (e) { console.error("Lỗi cập nhật trạng thái: ", e); }
    };

    const fetchInventoryLogs = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/inventory/logs');
        if (res.ok) inventoryLogs.value = await res.json();
      } catch (e) { console.error("Lỗi tải nhật ký kho"); }
    };

    const deleteInventoryLog = (id) => {
      if (window.showConfirm) {
        window.showConfirm(
          'Xác nhận xóa phiếu kho',
          'Bạn có chắc chắn muốn xóa phiếu nhập/xuất kho này?',
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/inventory/logs/${id}`, { method: 'DELETE' });
              if (res.ok) {
                fetchInventoryLogs();
                if (window.showToast) window.showToast("Thành công", "Đã xóa phiếu kho.", "success");
              } else {
                if (window.showToast) window.showToast("Lỗi", "Không thể xóa phiếu kho.", "error");
              }
            } catch (e) {
              console.error("Lỗi khi xóa phiếu kho: ", e);
              if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
            }
          }
        );
      } else {
        if (!confirm("Bạn có chắc chắn muốn xóa phiếu này?")) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/inventory/logs/${id}`, { method: 'DELETE' })
          .then(res => { if (res.ok) fetchInventoryLogs(); })
          .catch(e => console.error("Lỗi xóa log"));
      }
    };

    const searchOrderQuery = ref('');
    const orderSortKey = ref('id');
    const orderSortOrder = ref('desc');

    const filteredOrders = Vue.computed(() => {
      let result = [...orders.value];
      if (searchOrderQuery.value) {
        const q = searchOrderQuery.value.toLowerCase();
        result = result.filter(o => 
          o.id.toString().includes(q) || 
          (o.customer || '').toLowerCase().includes(q) ||
          (o.phone || '').includes(q)
        );
      }
      result.sort((a, b) => {
        let valA = a[orderSortKey.value];
        let valB = b[orderSortKey.value];
        if (orderSortOrder.value === 'desc') [valA, valB] = [valB, valA];
        return valA > valB ? 1 : -1;
      });
      return result;
    });

    const sortOrders = (key) => {
      if (orderSortKey.value === key) {
        orderSortOrder.value = orderSortOrder.value === 'asc' ? 'desc' : 'asc';
      } else {
        orderSortKey.value = key;
        orderSortOrder.value = 'asc';
      }
    };

    // Order Edit logic
    const showOrderEditModal = ref(false);
    const orderEditForm = reactive({
      id: null,
      ten_khach_hang: '',
      so_dien_thoai: '',
      dia_chi: '',
      ghi_chu: '',
      trang_thai: ''
    });

    const openEditOrderModal = (order) => {
      orderEditForm.id = order.id;
      orderEditForm.ten_khach_hang = order.ten_khach_hang || order.customer || '';
      orderEditForm.so_dien_thoai = order.so_dien_thoai || order.phone || '';
      orderEditForm.dia_chi = order.dia_chi || order.address || '';
      orderEditForm.ghi_chu = order.ghi_chu || '';
      orderEditForm.trang_thai = order.trang_thai || order.status || 'cho_duyet';
      showOrderEditModal.value = true;
    };

    const saveOrder = async () => {
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/don-hang/admin/update/${orderEditForm.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(orderEditForm)
        });
        if (res.ok) {
          if (window.showToast) window.showToast("Thành công", "Đã cập nhật đơn hàng.", "success");
          showOrderEditModal.value = false;
          fetchOrders();
        } else {
          const err = await res.json();
          if (window.showToast) window.showToast("Lỗi", err.detail || "Không thể cập nhật", "warning");
        }
      } catch (e) { console.error("Lỗi cập nhật đơn hàng:", e); }
    };

    // Customer search
    const customerFilterQuery = ref('');

    const filteredCustomers = Vue.computed(() => {
      if (!customerFilterQuery.value) return customers.value;
      const q = customerFilterQuery.value.toLowerCase();
      return customers.value.filter(c => {
        const name = (c.ho_ten || c.name || '').toLowerCase();
        const email = (c.email || '').toLowerCase();
        const phone = (c.so_dien_thoai || c.phone || '').toLowerCase();
        return name.includes(q) || email.includes(q) || phone.includes(q);
      });
    });

    // Customer Modal State
    const showCustomerModal = ref(false);
    const isEditingCustomer = ref(false);
    const editingCustomerId = ref(null);
    const customerForm = reactive({
      ho_ten: '',
      email: '',
      so_dien_thoai: '',
      dia_chi: '',
      vai_tro: 'nguoi_dung',
      trang_thai: 'dang_hoat_dong',
      hinh_anh: ''
    });

    // Voucher Modal State
    const showVoucherModal = ref(false);
    const isEditingVoucher = ref(false);
    const editingVoucherId = ref(null);
    const voucherForm = reactive({
      ma_voucher: '',
      loai_giam_gia: 'phan_tram',
      gia_tri_giam: 0,
      don_hang_toi_thieu: 0,
      giam_toi_da: null,
      ngay_het_han: '',
      so_luong_con_lai: 100,
      trang_thai: 'dang_hoat_dong'
    });

    const fetchCustomers = async () => {
      try {
        console.log("[DEBUG] Fetching customers list...");
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/customers/');
        if (res.ok) {
          const data = await res.json();
          customers.value = data.map(c => {
            if (c.hinh_anh && !c.hinh_anh.startsWith('http://') && !c.hinh_anh.startsWith('https://')) {
              const base = window.API_BASE || 'http://127.0.0.1:8000';
              const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
              const cleanPath = c.hinh_anh.startsWith('/') ? c.hinh_anh : '/' + c.hinh_anh;
              c.hinh_anh = cleanBase + cleanPath;
            }
            return c;
          });
        }
      } catch (e) { console.error("Lỗi tải khách hàng", e); }
    };

    const handleAvatarError = (customer) => {
      if (customer) {
        customer.hinh_anh = null;
      }
      const idx = customers.value.findIndex(c => c && c.id === customer.id);
      if (idx !== -1) {
        customers.value[idx].hinh_anh = null;
      }
    };

    const formatImageUrl = (url) => {
      if (!url) return '';
      if (typeof url !== 'string') {
        if (Array.isArray(url)) {
          if (url.length === 0) return '';
          url = url[0];
        } else {
          url = String(url);
        }
      }
      if (!url || typeof url !== 'string') return '';
      if (url.startsWith('http://') || url.startsWith('https://')) return url;
      
      let cleanUrl = url;
      if (cleanUrl.includes('/static/uploads/')) {
        cleanUrl = '/static/uploads/' + cleanUrl.split('/static/uploads/')[1];
      } else if (cleanUrl.includes('\\static\\uploads\\')) {
        cleanUrl = '/static/uploads/' + cleanUrl.split('\\static\\uploads\\')[1];
      }
      
      const base = window.API_BASE || 'https://peach-store-backend.onrender.com';
      const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
      return cleanBase + cleanUrl;
    };

    const fetchVouchers = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/vouchers/admin/all');
        if (res.ok) vouchers.value = await res.json();
      } catch (e) { console.error("Lỗi tải voucher: ", e); }
    };

    const openAddCustomerModal = () => {
      isEditingCustomer.value = false;
      editingCustomerId.value = null;
      Object.assign(customerForm, { ho_ten: '', email: '', so_dien_thoai: '', dia_chi: '', vai_tro: 'nguoi_dung', trang_thai: 'dang_hoat_dong', hinh_anh: '' });
      showCustomerModal.value = true;
    };

    const openEditCustomerModal = (customer) => {
      isEditingCustomer.value = true;
      editingCustomerId.value = customer.id;
      Object.assign(customerForm, {
        ho_ten: customer.ho_ten || '',
        email: customer.email || '',
        so_dien_thoai: customer.so_dien_thoai || '',
        dia_chi: customer.dia_chi || '',
        vai_tro: customer.vai_tro || 'nguoi_dung',
        trang_thai: customer.trang_thai || 'dang_hoat_dong',
        hinh_anh: customer.hinh_anh || ''
      });
      showCustomerModal.value = true;
    };

    const saveCustomer = async () => {
      // Validate lengths manually as a second layer of protection
      if (customerForm.ho_ten.length > 100) {
        if (window.showToast) window.showToast("Lỗi", "Họ tên không được quá 100 ký tự", "warning");
        return;
      }
      if (customerForm.email.length > 150) {
        if (window.showToast) window.showToast("Lỗi", "Email không được quá 150 ký tự", "warning");
        return;
      }
      if (customerForm.so_dien_thoai.length > 10) {
        if (window.showToast) window.showToast("Lỗi", "Số điện thoại không được quá 10 ký tự", "warning");
        return;
      }
      if (customerForm.dia_chi.length > 255) {
        if (window.showToast) window.showToast("Lỗi", "Địa chỉ không được quá 255 ký tự", "warning");
        return;
      }

      try {
        const url = isEditingCustomer.value
          ? `${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/customers/${editingCustomerId.value}`
          : (window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/customers/';
        
        const method = isEditingCustomer.value ? 'PUT' : 'POST';
        
        console.log(`[DEBUG] Calling ${method} on: ${url}`);
        const res = await fetch(url, {
          method: method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(customerForm)
        });

        if (res.ok) {
          showCustomerModal.value = false;
          fetchCustomers();
          if (window.showToast) window.showToast("Thành công", isEditingCustomer.value ? "Đã cập nhật người dùng." : "Đã thêm người dùng mới.", "success");
        } else {
          const errorData = await res.json();
          const errorMsg = errorData.detail ? JSON.stringify(errorData.detail) : "Lỗi không xác định";
          if (window.showToast) window.showToast("Lỗi", errorMsg, "warning");
        }
      } catch (e) { 
        console.error("Lỗi khi lưu người dùng: ", e);
        if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
      }
    };

    const deleteCustomer = (id) => {
      if (window.showConfirm) {
        window.showConfirm(
          'Xác nhận xóa',
          `Bạn có chắc chắn muốn xóa người dùng này? Thao tác này không thể hoàn tác.`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              console.log(`[DEBUG] DELETE request for ID: ${id}`);
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/customers/${id}`, { method: 'DELETE' });
              if (res.ok) {
                console.log(`[DEBUG] DELETE success for ID: ${id}`);
                fetchCustomers();
                if (window.showToast) window.showToast("Thành công", "Đã xóa người dùng.", "success");
              }
            } catch (e) { console.error("Lỗi khi xóa người dùng"); }
          }
        );
      } else {
        if (!confirm("Bạn có chắc chắn muốn xóa người dùng này?")) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/customers/${id}`, { method: 'DELETE' })
          .then(res => { if (res.ok) { fetchCustomers(); } })
          .catch(e => console.error("Lỗi khi xóa người dùng"));
      }
    };

    // --- PIN & Password Recovery Requests ---
    const customerSubTab = ref('list');
    const resetRequests = ref([]);
    const showVerifyModal = ref(false);
    const selectedRequest = ref(null);
    const isResetting = ref(false);

    const verifyForm = reactive({
      fullName: '',
      email: '',
      phone: '',
      address: ''
    });

    const isVerified = ref(false);
    const isMatched = ref(false);
    const matchedUser = ref(null);
    const verificationMessage = ref('');
    const generatedPassword = ref('');
    const generatedPin = ref('');

    const pendingRequestsCount = Vue.computed(() => {
      return resetRequests.value.filter(r => r.status === 'pending').length;
    });

    const fetchResetRequests = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/support/reset-requests');
        if (res.ok) {
          resetRequests.value = await res.json();
        }
      } catch (e) {
        console.error("Lỗi tải danh sách yêu cầu khôi phục: ", e);
      }
    };

    // --- Business Account Upgrade Requests ---
    const businessRequests = ref([]);
    
    const pendingBusinessRequestsCount = Vue.computed(() => {
      return businessRequests.value.filter(r => r.trang_thai === 'cho_duyet').length;
    });

    const fetchBusinessRequests = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/business-requests');
        if (res.ok) {
          businessRequests.value = await res.json();
        }
      } catch (e) {
        console.error("Lỗi tải danh sách yêu cầu nâng cấp doanh nghiệp: ", e);
      }
    };

    const approveBusinessRequest = async (requestId) => {
      if (!confirm("Bạn có chắc chắn muốn phê duyệt yêu cầu này và nâng cấp tài khoản của khách hàng lên Doanh nghiệp?")) return;
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/business-requests/${requestId}/approve`, {
          method: 'POST'
        });
        if (res.ok) {
          const data = await res.json();
          if (window.showToast) window.showToast("Thành công", data.message, "success");
          await fetchBusinessRequests();
          await fetchCustomers(); // Reload customer list to reflect upgraded role
          if (typeof fetchAuditLogs === 'function') fetchAuditLogs();
        } else {
          const errorData = await res.json();
          if (window.showToast) window.showToast("Lỗi", errorData.detail || "Không thể phê duyệt yêu cầu.", "error");
        }
      } catch (e) {
        console.error("Lỗi phê duyệt yêu cầu doanh nghiệp: ", e);
      }
    };

    const rejectBusinessRequest = async (requestId) => {
      if (!confirm("Bạn có chắc chắn muốn từ chối yêu cầu đăng ký nâng cấp doanh nghiệp này?")) return;
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/business-requests/${requestId}/reject`, {
          method: 'POST'
        });
        if (res.ok) {
          const data = await res.json();
          if (window.showToast) window.showToast("Đã từ chối", data.message, "success");
          await fetchBusinessRequests();
          if (typeof fetchAuditLogs === 'function') fetchAuditLogs();
        } else {
          const errorData = await res.json();
          if (window.showToast) window.showToast("Lỗi", errorData.detail || "Không thể từ chối yêu cầu.", "error");
        }
      } catch (e) {
        console.error("Lỗi từ chối yêu cầu doanh nghiệp: ", e);
      }
    };

    // Admin Chat with User State & Methods
    const showAdminChatModal = ref(false);
    const selectedChatCustomer = ref(null);
    const allAdminChatMessages = ref([]);
    const adminChatVisibleStartIdx = ref(0);
    const adminChatInputText = ref('');
    const loadingAdminChat = ref(false);

    const adminChatMessages = Vue.computed(() => {
      return allAdminChatMessages.value.slice(adminChatVisibleStartIdx.value, adminChatVisibleStartIdx.value + 10);
    });

    const showAdminChatLoadPrevious = Vue.computed(() => adminChatVisibleStartIdx.value > 0);
    const showAdminChatLoadNext = Vue.computed(() => adminChatVisibleStartIdx.value < allAdminChatMessages.value.length - 10);

    const scrollAdminChatToBottom = () => {
      Vue.nextTick(() => {
        const container = document.getElementById('adminChatContainer');
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    };

    const loadAdminChatPreviousMessages = () => {
      adminChatVisibleStartIdx.value = Math.max(0, adminChatVisibleStartIdx.value - 10);
      scrollAdminChatToBottom();
    };

    const loadAdminChatNextMessages = () => {
      adminChatVisibleStartIdx.value = Math.min(allAdminChatMessages.value.length - 10, adminChatVisibleStartIdx.value + 10);
      scrollAdminChatToBottom();
    };

    const unreadChatStates = ref({});

    const fetchUnreadChatStates = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/support/admin/unread-states');
        if (res.ok) {
          unreadChatStates.value = await res.json();
        }
      } catch (e) {
        console.error("Lỗi lấy trạng thái chưa rep: ", e);
      }
    };

    const openAdminChatModal = (customer) => {
      selectedChatCustomer.value = customer;
      allAdminChatMessages.value = [];
      adminChatInputText.value = '';
      showAdminChatModal.value = true;
      unreadChatStates.value[customer.id] = false;
      fetchAdminChatMessages(customer.id);
    };

    const fetchAdminChatMessages = async (customerId) => {
      loadingAdminChat.value = true;
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/support/admin/tin-nhan-chat/${customerId}`);
        if (res.ok) {
          allAdminChatMessages.value = await res.json();
          if (allAdminChatMessages.value.length > 10) {
            adminChatVisibleStartIdx.value = allAdminChatMessages.value.length - 10;
          } else {
            adminChatVisibleStartIdx.value = 0;
          }
          scrollAdminChatToBottom();
        }
      } catch (e) {
        console.error("Lỗi tải tin nhắn chat: ", e);
      } finally {
        loadingAdminChat.value = false;
      }
    };

    const fetchAdminChatMessagesBackground = async (customerId) => {
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/support/admin/tin-nhan-chat/${customerId}`);
        if (res.ok) {
          const newMsgs = await res.json();
          if (newMsgs.length !== allAdminChatMessages.value.length) {
            allAdminChatMessages.value = newMsgs;
            if (allAdminChatMessages.value.length > 10) {
              adminChatVisibleStartIdx.value = allAdminChatMessages.value.length - 10;
            } else {
              adminChatVisibleStartIdx.value = 0;
            }
            scrollAdminChatToBottom();
          }
        }
      } catch (e) {
        console.error("Lỗi tải tin nhắn background: ", e);
      }
    };

    let adminChatIntervalId = null;

    const startAdminChatPolling = () => {
      stopAdminChatPolling();
      adminChatIntervalId = setInterval(() => {
        fetchUnreadChatStates();
        if (activeTab.value === 'chat') {
          if (selectedChatCustomer.value) {
            fetchAdminChatMessagesBackground(selectedChatCustomer.value.id);
          }
        }
      }, 10000);
    };

    const stopAdminChatPolling = () => {
      if (adminChatIntervalId) {
        clearInterval(adminChatIntervalId);
        adminChatIntervalId = null;
      }
    };

    /**
     * Gửi tin nhắn phản hồi hỗ trợ trực tiếp từ Admin tới khách hàng.
     */
    const sendAdminChatMessage = async () => {
      const textVal = adminChatInputText.value.trim();
      if (!textVal || !selectedChatCustomer.value) return;

      adminChatInputText.value = '';
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/support/admin/tin-nhan-chat/${selectedChatCustomer.value.id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: textVal })
        });
        if (res.ok) {
          const newMsg = await res.json();
          allAdminChatMessages.value.push(newMsg);
          unreadChatStates.value[selectedChatCustomer.value.id] = false;
          
          if (allAdminChatMessages.value.length > 10) {
            adminChatVisibleStartIdx.value = allAdminChatMessages.value.length - 10;
          } else {
            adminChatVisibleStartIdx.value = 0;
          }
          scrollAdminChatToBottom();
        }
      } catch (e) {
        console.error("Lỗi gửi tin nhắn phản hồi: ", e);
      }
    };

    const openVerifyModal = (req) => {
      selectedRequest.value = req;
      Object.assign(verifyForm, {
        fullName: req.fullName || '',
        email: req.email || '',
        phone: req.phone || '',
        address: req.address || ''
      });
      isVerified.value = false;
      isMatched.value = false;
      matchedUser.value = null;
      verificationMessage.value = '';
      generatedPassword.value = '';
      generatedPin.value = '';
      showVerifyModal.value = true;
    };

    const verifyCustomer = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/support/verify-customer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(verifyForm)
        });
        if (res.ok) {
          const data = await res.json();
          isVerified.value = true;
          isMatched.value = data.matched;
          if (data.matched) {
            matchedUser.value = data.user;
            verificationMessage.value = "Thông tin chi tiết HOÀN TOÀN TRÙNG KHỚP với người dùng trên hệ thống!";
          } else {
            matchedUser.value = null;
            verificationMessage.value = data.message || "Không tìm thấy người dùng trùng khớp.";
          }
        }
      } catch (e) {
        console.error("Lỗi kiểm tra trùng khớp: ", e);
      }
    };

    const resetPassword = async () => {
      if (!matchedUser.value) return;
      isResetting.value = true;
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/support/reset-password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: matchedUser.value.id,
            request_id: selectedRequest.value ? selectedRequest.value.id : null
          })
        });
        if (res.ok) {
          const data = await res.json();
          generatedPassword.value = data.new_password;
          fetchResetRequests();
          if (window.showToast) window.showToast("Thành công", "Đã cấp mật khẩu mới thành công!", "success");
        }
      } catch (e) {
        console.error("Lỗi cấp lại mật khẩu: ", e);
      } finally {
        isResetting.value = false;
      }
    };

    const resetPin = async () => {
      if (!matchedUser.value) return;
      isResetting.value = true;
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/support/reset-pin', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: matchedUser.value.id,
            request_id: selectedRequest.value ? selectedRequest.value.id : null
          })
        });
        if (res.ok) {
          const data = await res.json();
          generatedPin.value = data.new_pin;
          fetchResetRequests();
          if (window.showToast) window.showToast("Thành công", "Đã cấp mã PIN mới thành công!", "success");
        }
      } catch (e) {
        console.error("Lỗi cấp lại mã PIN: ", e);
      } finally {
        isResetting.value = false;
      }
    };

    const copyText = (text, label) => {
      navigator.clipboard.writeText(text);
      if (window.showToast) {
        window.showToast("Thành công", `Đã sao chép ${label} vào bộ nhớ tạm!`, "success");
      } else {
        alert(`Đã sao chép ${label} vào bộ nhớ tạm!`);
      }
    };

    // Voucher CRUD
    const openAddVoucherModal = () => {
      isEditingVoucher.value = false;
      editingVoucherId.value = null;
      Object.assign(voucherForm, {
        ma_voucher: '',
        loai_giam_gia: 'phan_tram',
        gia_tri_giam: 0,
        don_hang_toi_thieu: 0,
        giam_toi_da: null,
        ngay_het_han: '',
        so_luong_con_lai: 100,
        trang_thai: 'dang_hoat_dong'
      });
      showVoucherModal.value = true;
    };

    const openEditVoucherModal = (voucher) => {
      isEditingVoucher.value = true;
      editingVoucherId.value = voucher.id;
      Object.assign(voucherForm, {
        ma_voucher: voucher.ma_voucher || '',
        loai_giam_gia: voucher.loai_giam_gia || 'phan_tram',
        gia_tri_giam: voucher.gia_tri_giam || 0,
        don_hang_toi_thieu: voucher.don_hang_toi_thieu || 0,
        giam_toi_da: voucher.giam_toi_da || null,
        ngay_het_han: voucher.ngay_het_han ? voucher.ngay_het_han.slice(0, 16) : '',
        so_luong_con_lai: voucher.so_luong_con_lai || 0,
        trang_thai: voucher.trang_thai || 'dang_hoat_dong'
      });
      showVoucherModal.value = true;
    };

    const saveVoucher = async () => {
      if (!voucherForm.ma_voucher || !voucherForm.ma_voucher.trim()) {
        if (window.showToast) window.showToast("Lỗi nhập liệu", "Vui lòng nhập mã voucher.", "warning");
        return;
      }
      if (!voucherForm.gia_tri_giam || voucherForm.gia_tri_giam <= 0) {
        if (window.showToast) window.showToast("Lỗi nhập liệu", "Vui lòng nhập giá trị giảm hợp lệ.", "warning");
        return;
      }
      try {
        const url = isEditingVoucher.value
          ? `${window.API_BASE || 'http://127.0.0.1:8000'}/vouchers/${editingVoucherId.value}`
          : (window.API_BASE || 'http://127.0.0.1:8000') + '/vouchers/';

        const method = isEditingVoucher.value ? 'PUT' : 'POST';

        const payload = { ...voucherForm };
        if (payload.ngay_het_han) {
          payload.ngay_het_han = new Date(payload.ngay_het_han).toISOString();
        }
        if (payload.giam_toi_da === null || payload.giam_toi_da === '') {
          delete payload.giam_toi_da;
        }

        const res = await fetch(url, {
          method: method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          showVoucherModal.value = false;
          fetchVouchers();
          if (window.showToast) window.showToast("Thành công", isEditingVoucher.value ? "Đã cập nhật voucher." : "Đã thêm voucher mới.", "success");
        } else {
          const errorData = await res.json();
          const errorMsg = errorData.detail ? JSON.stringify(errorData.detail) : "Lỗi không xác định";
          if (window.showToast) window.showToast("Lỗi", errorMsg, "warning");
        }
      } catch (e) {
        console.error("Lỗi khi lưu voucher: ", e);
        if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
      }
    };

    const deleteVoucher = (id) => {
      if (window.showConfirm) {
        window.showConfirm(
          'Xác nhận xóa voucher',
          `Bạn có chắc chắn muốn xóa voucher này? Thao tác này không thể hoàn tác.`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/vouchers/${id}`, { method: 'DELETE' });
              if (res.ok) {
                fetchVouchers();
                if (window.showToast) window.showToast("Thành công", "Đã xóa voucher.", "success");
              } else {
                if (window.showToast) window.showToast("Lỗi", "Không thể xóa voucher.", "error");
              }
            } catch (e) { console.error("Lỗi khi xóa voucher", e); }
          }
        );
      } else {
        if (!confirm("Bạn có chắc chắn muốn xóa voucher này?")) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/vouchers/${id}`, { method: 'DELETE' })
          .then(res => { if (res.ok) { fetchVouchers(); } })
          .catch(e => console.error("Lỗi khi xóa voucher"));
      }
    };

    const toggleVoucherStatus = async (id, newStatus) => {
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/vouchers/${id}/status`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ trang_thai: newStatus })
        });
        if (res.ok) {
          fetchVouchers();
          const label = newStatus === 'dang_hoat_dong' ? 'đã kích hoạt' : 'đã tạm dừng';
          if (window.showToast) window.showToast("Thành công", `Voucher ${label}.`, "success");
        } else {
          const errorData = await res.json();
          const errorMsg = errorData.detail ? JSON.stringify(errorData.detail) : "Lỗi không xác định";
          if (window.showToast) window.showToast("Lỗi", errorMsg, "warning");
        }
      } catch (e) {
        console.error("Lỗi khi đổi trạng thái voucher: ", e);
        if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
      }
    };

    // === Shipping CRUD ===
    const showShippingModal = ref(false);
    const isEditingShipping = ref(false);
    const editingShippingId = ref(null);
    const shippingForm = reactive({
      ten_don_vi: '',
      ma_don_vi: '',
      phi_co_dinh: 0,
      nguong_mien_phi: 0,
      thoi_gian_du_kien: '2-3 ngay',
      mo_ta: '',
      kich_hoat: true
    });

    const fetchShippingUnits = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/shipping/admin/all');
        if (res.ok) shippingUnits.value = await res.json();
      } catch (e) { console.error("Lỗi tải đơn vị vận chuyển: ", e); }
    };

    const openAddShippingModal = () => {
      isEditingShipping.value = false;
      editingShippingId.value = null;
      Object.assign(shippingForm, { ten_don_vi: '', ma_don_vi: '', phi_co_dinh: 0, nguong_mien_phi: 0, thoi_gian_du_kien: '2-3 ngay', mo_ta: '', kich_hoat: true });
      showShippingModal.value = true;
    };

    const openEditShippingModal = (unit) => {
      isEditingShipping.value = true;
      editingShippingId.value = unit.id;
      Object.assign(shippingForm, {
        ten_don_vi: unit.ten_don_vi || '',
        ma_don_vi: unit.ma_don_vi || '',
        phi_co_dinh: unit.phi_co_dinh || 0,
        nguong_mien_phi: unit.nguong_mien_phi || 0,
        thoi_gian_du_kien: unit.thoi_gian_du_kien || '2-3 ngay',
        mo_ta: unit.mo_ta || '',
        kich_hoat: unit.kich_hoat !== undefined ? unit.kich_hoat : true
      });
      showShippingModal.value = true;
    };

    const saveShippingUnit = async () => {
      if (!shippingForm.ten_don_vi || !shippingForm.ma_don_vi) {
        if (window.showToast) window.showToast("Lỗi nhập liệu", "Vui lòng nhập tên và mã đơn vị.", "warning");
        return;
      }
      try {
        const url = isEditingShipping.value
          ? `${window.API_BASE || 'http://127.0.0.1:8000'}/shipping/don-vi/${editingShippingId.value}`
          : (window.API_BASE || 'http://127.0.0.1:8000') + '/shipping/don-vi';
        const method = isEditingShipping.value ? 'PUT' : 'POST';
        const res = await fetch(url, {
          method, headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(shippingForm)
        });
        if (res.ok) {
          showShippingModal.value = false;
          fetchShippingUnits();
          if (window.showToast) window.showToast("Thành công", isEditingShipping.value ? "Đã cập nhật đơn vị vận chuyển." : "Đã thêm đơn vị vận chuyển.", "success");
        } else {
          const err = await res.json();
          if (window.showToast) window.showToast("Lỗi", err.detail ? JSON.stringify(err.detail) : "Lỗi không xác định", "warning");
        }
      } catch (e) {
        console.error("Lỗi lưu đơn vị vận chuyển:", e);
        if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
      }
    };

    const deleteShippingUnit = (id) => {
      if (window.showConfirm) {
        window.showConfirm(
          'Xóa đơn vị vận chuyển',
          'Bạn có chắc muốn xóa đơn vị vận chuyển này?',
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/shipping/don-vi/${id}`, { method: 'DELETE' });
              if (res.ok) {
                fetchShippingUnits();
                if (window.showToast) window.showToast("Thành công", "Đã xóa đơn vị vận chuyển thành công.", "success");
              } else {
                if (window.showToast) window.showToast("Lỗi", "Không thể xóa đơn vị vận chuyển.", "error");
              }
            } catch (e) {
              console.error("Lỗi khi xóa đơn vị vận chuyển:", e);
              if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
            }
          }
        );
      } else {
        if (!confirm("Bạn có chắc muốn xóa đơn vị vận chuyển này?")) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/shipping/don-vi/${id}`, { method: 'DELETE' })
          .then(res => { if (res.ok) { fetchShippingUnits(); if (window.showToast) window.showToast("Thành công", "Đã xóa.", "success"); } })
          .catch(e => console.error("Lỗi xóa đơn vị vận chuyển"));
      }
    };

    const toggleShippingActive = async (unit) => {
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/shipping/don-vi/${unit.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ kich_hoat: !unit.kich_hoat })
        });
        if (res.ok) fetchShippingUnits();
      } catch (e) { console.error("Lỗi cập nhật trạng thái vận chuyển"); }
    };

    // === Payment CRUD ===
    const showPaymentModal = ref(false);
    const isEditingPayment = ref(false);
    const editingPaymentId = ref(null);
    const paymentForm = reactive({
      ten_doi_tac: '',
      ma_phuong_thuc: '',
      loai_hinh: 'Chuyen_khoan',
      mo_ta: '',
      kich_hoat: true
    });

    const fetchPaymentPartners = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/payment/admin/all');
        if (res.ok) paymentPartners.value = await res.json();
      } catch (e) { console.error("Lỗi tải đối tác thanh toán: ", e); }
    };

    const openAddPaymentModal = () => {
      isEditingPayment.value = false;
      editingPaymentId.value = null;
      Object.assign(paymentForm, { ten_doi_tac: '', ma_phuong_thuc: '', loai_hinh: 'Chuyen_khoan', mo_ta: '', kich_hoat: true });
      showPaymentModal.value = true;
    };

    const openEditPaymentModal = (partner) => {
      isEditingPayment.value = true;
      editingPaymentId.value = partner.id;
      Object.assign(paymentForm, {
        ten_doi_tac: partner.ten_doi_tac || '',
        ma_phuong_thuc: partner.ma_phuong_thuc || '',
        loai_hinh: partner.loai_hinh || 'Chuyen_khoan',
        mo_ta: partner.mo_ta || '',
        kich_hoat: partner.kich_hoat !== undefined ? partner.kich_hoat : true
      });
      showPaymentModal.value = true;
    };

    const savePaymentPartner = async () => {
      if (!paymentForm.ten_doi_tac || !paymentForm.ma_phuong_thuc) {
        if (window.showToast) window.showToast("Lỗi nhập liệu", "Vui lòng nhập tên và mã phương thức.", "warning");
        return;
      }
      try {
        const url = isEditingPayment.value
          ? `${window.API_BASE || 'http://127.0.0.1:8000'}/payment/doi-tac/${editingPaymentId.value}`
          : (window.API_BASE || 'http://127.0.0.1:8000') + '/payment/doi-tac';
        const method = isEditingPayment.value ? 'PUT' : 'POST';
        const res = await fetch(url, {
          method, headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(paymentForm)
        });
        if (res.ok) {
          showPaymentModal.value = false;
          fetchPaymentPartners();
          if (window.showToast) window.showToast("Thành công", isEditingPayment.value ? "Đã cập nhật đối tác." : "Đã thêm đối tác.", "success");
        } else {
          const err = await res.json();
          if (window.showToast) window.showToast("Lỗi", err.detail ? JSON.stringify(err.detail) : "Lỗi không xác định", "warning");
        }
      } catch (e) {
        console.error("Lỗi lưu đối tác:", e);
        if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
      }
    };

    const deletePaymentPartner = (id) => {
      if (window.showConfirm) {
        window.showConfirm(
          'Xóa đối tác thanh toán',
          'Bạn có chắc muốn xóa đối tác thanh toán này?',
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/payment/doi-tac/${id}`, { method: 'DELETE' });
              if (res.ok) {
                fetchPaymentPartners();
                if (window.showToast) window.showToast("Thành công", "Đã xóa đối tác thanh toán thành công.", "success");
              } else {
                if (window.showToast) window.showToast("Lỗi", "Không thể xóa đối tác thanh toán.", "error");
              }
            } catch (e) {
              console.error("Lỗi khi xóa đối tác thanh toán:", e);
              if (window.showToast) window.showToast("Lỗi kết nối", "Không thể kết nối tới server.", "warning");
            }
          }
        );
      } else {
        if (!confirm("Bạn có chắc muốn xóa đối tác thanh toán này?")) return;
        fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/payment/doi-tac/${id}`, { method: 'DELETE' })
          .then(res => { if (res.ok) { fetchPaymentPartners(); if (window.showToast) window.showToast("Thành công", "Đã xóa.", "success"); } })
          .catch(e => console.error("Lỗi xóa đối tác"));
      }
    };

    const togglePaymentActive = async (partner) => {
      try {
        const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/payment/doi-tac/${partner.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ kich_hoat: !partner.kich_hoat })
        });
        if (res.ok) fetchPaymentPartners();
      } catch (e) { console.error("Lỗi cập nhật trạng thái thanh toán"); }
    };

    const fetchEmployees = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/employees');
        if (res.ok) {
          admins.value = await res.json();
        }
      } catch (e) { console.error("Lỗi tải nhân viên: ", e); }
    };

    // --- Multi-selection for Vouchers ---
    const selectedVoucherIds = ref([]);
    const toggleVoucherSelection = (id) => {
      const idx = selectedVoucherIds.value.indexOf(id);
      if (idx > -1) selectedVoucherIds.value.splice(idx, 1);
      else selectedVoucherIds.value.push(id);
    };
    const toggleSelectAllVouchers = () => {
      if (selectedVoucherIds.value.length === filteredVouchers.value.length && filteredVouchers.value.length > 0) {
        selectedVoucherIds.value = [];
      } else {
        selectedVoucherIds.value = filteredVouchers.value.map(v => v.id);
      }
    };
    const deleteSelectedVouchers = () => {
      if (!selectedVoucherIds.value.length) return;
      if (window.showConfirm) {
        window.showConfirm(
          'Xóa nhiều voucher',
          `Bạn có chắc muốn xóa ${selectedVoucherIds.value.length} voucher đã chọn?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>`,
          async () => {
            let successCount = 0;
            for (const id of selectedVoucherIds.value) {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/vouchers/${id}`, { method: 'DELETE' });
              if (res.ok) successCount++;
            }
            if (window.showToast) window.showToast("Thành công", `Đã xóa ${successCount} voucher.`, "success");
            selectedVoucherIds.value = [];
            fetchVouchers();
          }
        );
      }
    };

    // --- Multi-selection for Shipping ---
    const selectedShippingIds = ref([]);
    const toggleShippingSelection = (id) => {
      const idx = selectedShippingIds.value.indexOf(id);
      if (idx > -1) selectedShippingIds.value.splice(idx, 1);
      else selectedShippingIds.value.push(id);
    };
    const toggleSelectAllShipping = () => {
      if (selectedShippingIds.value.length === shippingUnits.value.length && shippingUnits.value.length > 0) {
        selectedShippingIds.value = [];
      } else {
        selectedShippingIds.value = shippingUnits.value.map(s => s.id);
      }
    };
    const deleteSelectedShipping = () => {
      if (!selectedShippingIds.value.length) return;
      if (window.showConfirm) {
        window.showConfirm(
          'Xóa nhiều đơn vị vận chuyển',
          `Bạn có chắc muốn xóa ${selectedShippingIds.value.length} đơn vị đã chọn?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>`,
          async () => {
            let count = 0;
            for (const id of selectedShippingIds.value) {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/shipping/don-vi/${id}`, { method: 'DELETE' });
              if (res.ok) count++;
            }
            if (window.showToast) window.showToast("Thành công", `Đã xóa ${count} đơn vị.`, "success");
            selectedShippingIds.value = [];
            fetchShippingUnits();
          }
        );
      }
    };

    // --- Multi-selection for Payments ---
    const selectedPaymentIds = ref([]);
    const togglePaymentSelection = (id) => {
      const idx = selectedPaymentIds.value.indexOf(id);
      if (idx > -1) selectedPaymentIds.value.splice(idx, 1);
      else selectedPaymentIds.value.push(id);
    };
    const toggleSelectAllPayments = () => {
      if (selectedPaymentIds.value.length === paymentPartners.value.length && paymentPartners.value.length > 0) {
        selectedPaymentIds.value = [];
      } else {
        selectedPaymentIds.value = paymentPartners.value.map(p => p.id);
      }
    };
    const deleteSelectedPayments = () => {
      if (!selectedPaymentIds.value.length) return;
      if (window.showConfirm) {
        window.showConfirm(
          'Xóa nhiều đối tác',
          `Bạn có chắc muốn xóa ${selectedPaymentIds.value.length} đối tác đã chọn?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>`,
          async () => {
            let count = 0;
            for (const id of selectedPaymentIds.value) {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/payment/doi-tac/${id}`, { method: 'DELETE' });
              if (res.ok) count++;
            }
            if (window.showToast) window.showToast("Thành công", `Đã xóa ${count} đối tác.`, "success");
            selectedPaymentIds.value = [];
            fetchPaymentPartners();
          }
        );
      }
    };

    const selectedCustomerIds = ref([]);
    const toggleCustomerSelection = (id) => {
      const idx = selectedCustomerIds.value.indexOf(id);
      if (idx > -1) selectedCustomerIds.value.splice(idx, 1);
      else selectedCustomerIds.value.push(id);
    };
    const toggleSelectAllCustomers = () => {
      if (selectedCustomerIds.value.length === filteredCustomers.value.length && filteredCustomers.value.length > 0) {
        selectedCustomerIds.value = [];
      } else {
        selectedCustomerIds.value = filteredCustomers.value.map(c => c.id);
      }
    };
    const deleteSelectedCustomers = () => {
      if (!selectedCustomerIds.value.length) {
        if (window.showToast) window.showToast("Thông báo", "Vui lòng chọn ít nhất một người dùng", "warning");
        return;
      }
      if (window.showConfirm) {
        window.showConfirm(
          'Xóa nhiều người dùng',
          `Bạn có chắc muốn xóa ${selectedCustomerIds.value.length} người dùng đã chọn?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>`,
          async () => {
            let count = 0;
            console.log(`[DEBUG] Starting bulk delete for ${selectedCustomerIds.value.length} users`);
            for (const id of selectedCustomerIds.value) {
              console.log(`[DEBUG] Deleting user ${id}...`);
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/customers/${id}`, { method: 'DELETE' });
              if (res.ok) count++;
            }
            console.log(`[DEBUG] Finished bulk delete. Success: ${count}`);
            if (window.showToast) window.showToast("Thành công", `Đã xóa ${count} người dùng.`, "success");
            selectedCustomerIds.value = [];
            fetchCustomers();
          }
        );
      }
    };

    const updateEmployeeRole = async (employee) => {
      try {
        if (window.showToast) window.showToast("Đang cập nhật", `Đã chuyển ${employee.name} sang vai trò ${employee.role}`, "info");
      } catch (e) { console.error("Lỗi cập nhật chức vụ"); }
    };

    const deleteEmployee = (id) => {
      if (window.showConfirm) {
        window.showConfirm(
          'Xóa nhân viên',
          'Bạn có chắc muốn xóa nhân viên này khỏi hệ thống? Họ sẽ mất toàn bộ quyền truy cập.',
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="1.5"><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>`,
          async () => {
            try {
              const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/employees/${id}`, { method: 'DELETE' });
              if (res.ok) {
                const data = await res.json();
                admins.value = data.employees;
                if (window.showToast) window.showToast("Thành công", "Đã xóa nhân viên khỏi hệ thống.", "success");
              }
            } catch (e) {
              console.error("Lỗi xóa nhân viên: ", e);
            }
          }
        );
      }
    };

    const showEmployeeModal = ref(false);
    const isEditingEmployee = ref(false);
    const employeeForm = reactive({
      id: null,
      name: '',
      role: 'STAFF',
      email: '',
      phone: '',
      username: '',
      password: ''
    });

    const openAddEmployeeModal = () => {
      isEditingEmployee.value = false;
      Object.assign(employeeForm, { id: null, name: '', role: 'STAFF', email: '', phone: '', username: '', password: '123' });
      showEmployeeModal.value = true;
    };

    const openEditEmployeeModal = (emp) => {
      isEditingEmployee.value = true;
      Object.assign(employeeForm, { 
        id: emp.id, 
        name: emp.name, 
        role: emp.role, 
        email: emp.email || '', 
        phone: emp.phone || '',
        username: emp.username || '',
        password: emp.password || ''
      });
      showEmployeeModal.value = true;
    };

    const saveEmployee = async () => {
      if (!employeeForm.name) {
        if (window.showToast) window.showToast("Lỗi", "Vui lòng nhập họ và tên nhân viên!", "error");
        return;
      }
      if (!employeeForm.username) {
        if (window.showToast) window.showToast("Lỗi", "Vui lòng nhập tên đăng nhập nhân viên!", "error");
        return;
      }
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/employees', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(employeeForm)
        });
        if (res.ok) {
          const data = await res.json();
          admins.value = data.employees;
          showEmployeeModal.value = false;
          if (window.showToast) window.showToast("Thành công", "Đã lưu thông tin nhân viên.", "success");
        }
      } catch (e) {
        console.error("Lỗi lưu nhân viên: ", e);
      }
    };

    const onPhoneKeypress = (e) => {
      // Allow only digit keys
      if (e.key < '0' || e.key > '9') {
        e.preventDefault();
      }
    };

    const onPhoneInput = (e) => {
      // Strip out non-digits and cap at 10 digits
      employeeForm.phone = (employeeForm.phone || '').replace(/\D/g, '').slice(0, 10);
    };

    const onPhonePaste = (e) => {
      const clipboardData = e.clipboardData || window.clipboardData;
      const pastedData = clipboardData.getData('Text') || '';
      employeeForm.phone = pastedData.replace(/\D/g, '').slice(0, 10);
    };

    // --- Work Scheduling (Roster) State & Methods ---
    const getLocalDateString = () => {
      const d = new Date();
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    };

    const todayDate = computed(() => getLocalDateString());

    const schedules = ref([]);
    const showRosterModal = ref(false);
    const selectedRosterEmployee = ref(null);
    const rosterForm = reactive({
      id: null,
      date: getLocalDateString(),
      shift: 'Ca Sáng',
      notes: ''
    });

    const fetchSchedules = async () => {
      try {
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/schedules');
        if (res.ok) {
          schedules.value = await res.json();
        }
      } catch (e) {
        console.error("Lỗi tải lịch làm: ", e);
      }
    };

    const openRosterModal = (emp) => {
      selectedRosterEmployee.value = emp;
      Object.assign(rosterForm, {
        id: null,
        date: getLocalDateString(),
        shift: 'Ca Sáng',
        notes: ''
      });
      showRosterModal.value = true;
    };

    const saveRoster = async () => {
      if (!rosterForm.date) {
        if (window.showToast) window.showToast("Lỗi", "Vui lòng chọn ngày làm việc!", "error");
        return;
      }
      if (rosterForm.date < todayDate.value) {
        if (window.showToast) window.showToast("Lỗi", "Không thể phân lịch cho ngày đã qua!", "error");
        return;
      }
      if (!rosterForm.shift) {
        if (window.showToast) window.showToast("Lỗi", "Vui lòng chọn ca làm việc!", "error");
        return;
      }
      if (!rosterForm.notes || !rosterForm.notes.trim()) {
        if (window.showToast) window.showToast("Lỗi", "Vui lòng nhập ghi chú ca trực (mô tả công việc)!", "error");
        return;
      }
      try {
        const payload = {
          id: rosterForm.id,
          employeeId: selectedRosterEmployee.value.id,
          employeeName: selectedRosterEmployee.value.name,
          date: rosterForm.date,
          shift: rosterForm.shift,
          notes: rosterForm.notes
        };
        const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/schedules', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          const data = await res.json();
          schedules.value = data.schedules;
          showRosterModal.value = false;
          if (window.showToast) window.showToast("Thành công", "Đã phân lịch làm việc thành công.", "success");
        }
      } catch (e) {
        console.error("Lỗi lưu lịch làm: ", e);
      }
    };

    const deleteRoster = async (schId) => {
      if (confirm("Bạn có chắc chắn muốn xóa lịch phân ca này không?")) {
        try {
          const res = await fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/admin/schedules/${schId}`, { method: 'DELETE' });
          if (res.ok) {
            const data = await res.json();
            schedules.value = data.schedules;
            if (window.showToast) window.showToast("Thành công", "Đã xóa ca làm việc.", "success");
          }
        } catch (e) {
          console.error("Lỗi xóa ca làm: ", e);
        }
      }
    };

    fetchSchedules();

    const showAiConfigModal = ref(false);
    const aiConfigForm = reactive({
      provider: localStorage.getItem('peach_ai_provider') || 'DeepSeek',
      apiKey: localStorage.getItem('peach_ai_key') || '',
      model: localStorage.getItem('peach_ai_model') || 'deepseek-chat',
      isActive: localStorage.getItem('peach_ai_active') !== 'false'
    });

    const saveAiConfig = () => {
      localStorage.setItem('peach_ai_provider', aiConfigForm.provider);
      localStorage.setItem('peach_ai_key', aiConfigForm.apiKey);
      localStorage.setItem('peach_ai_model', aiConfigForm.model);
      localStorage.setItem('peach_ai_active', aiConfigForm.isActive ? 'true' : 'false');
      
      showAiConfigModal.value = false;
      if (window.showToast) {
        window.showToast("Thành công", "Cấu hình AI Model đã được lưu.", "success");
      }
    };

    const loadTabData = (tab) => {
      console.log(`[DEBUG] Lazy loading tab: ${tab}`);
      if (tab === 'dashboard') {
        fetchStats();
        fetchActivities();
      } else if (tab === 'products') {
        fetchProducts();
        fetchInventoryLogs();
      } else if (tab === 'orders') {
        fetchOrders();
      } else if (tab === 'customers') {
        fetchCustomers();
        fetchResetRequests();
        fetchBusinessRequests();
      } else if (tab === 'vouchers' || tab === 'coupons') {
        fetchVouchers();
      } else if (tab === 'shipping') {
        fetchShippingUnits();
      } else if (tab === 'payments') {
        fetchPaymentPartners();
      } else if (tab === 'admins') {
        fetchEmployees();
      } else if (tab === 'support') {
        fetchSupportTickets();
      } else if (tab === 'logs') {
        fetchAuditLogs();
      } else if (tab === 'loyalty') {
        fetchLoyaltyLevels();
        fetchCustomers();
      } else if (tab === 'notifications') {
        fetchPushCampaigns();
      } else if (tab === 'chat') {
        fetchCustomers();
        fetchUnreadChatStates();
      } else if (tab === 'ai') {
        fetchAiLogs();
      }
    };

    let silentRefreshInterval = null;

    onMounted(() => {
      // Lazy load only the active tab at startup
      loadTabData(activeTab.value);

      // Fetch badge-related data immediately on load so counts are shown instantly
      fetchOrders();
      fetchResetRequests();
      fetchBusinessRequests();
      fetchSupportTickets();
      fetchAuditLogs();
      fetchPushCampaigns();
      fetchUnreadChatStates();
      fetchAiLogs();

      startAdminChatPolling();

      // Silent background polling every 30 seconds to fetch fresh tables/counters seamlessly
      silentRefreshInterval = setInterval(() => {
        refreshData().catch(e => console.error("Lỗi tự động làm mới ngầm: ", e));
      }, 30000);
    });

    onUnmounted(() => {
      stopAdminChatPolling();
      if (silentRefreshInterval) {
        clearInterval(silentRefreshInterval);
      }
    });

    watch(activeTab, (newTab) => {
      loadTabData(newTab);
    });

    const refreshData = async () => {
      await Promise.all([
        fetchStats(),
        fetchActivities(),
        fetchProducts(),
        fetchOrders(),
        fetchInventoryLogs(),
        fetchCustomers(),
        fetchVouchers(),
        fetchShippingUnits(),
        fetchPaymentPartners(),
        fetchResetRequests(),
        fetchSupportTickets(),
        fetchAuditLogs(),
        fetchLoyaltyLevels(),
        fetchBusinessRequests(),
        fetchPushCampaigns(),
        fetchAiLogs()
      ]);
    };

    const getMembershipRank = (user) => {
      if (!user) return 'Bạc';
      if (user.vai_tro === 'admin') return 'Premium Admin';
      const points = user.diem_tich_luy || 0;
      if (loyaltyLevels.value && loyaltyLevels.value.length > 0) {
        const sorted = [...loyaltyLevels.value].sort((a, b) => b.diem_toi_thieu - a.diem_toi_thieu);
        for (const level of sorted) {
          if (points >= level.diem_toi_thieu) {
            return level.ten_hang;
          }
        }
      }
      if (points >= 5000) return 'Kim cương';
      if (points >= 1000) return 'Vàng';
      return 'Bạc';
    };

    const getRankColor = (user) => {
      if (!user) return '#8e8e93';
      if (user.vai_tro === 'admin') return '#5856d6';
      const points = user.diem_tich_luy || 0;
      if (loyaltyLevels.value && loyaltyLevels.value.length > 0) {
        const sorted = [...loyaltyLevels.value].sort((a, b) => b.diem_toi_thieu - a.diem_toi_thieu);
        for (const level of sorted) {
          if (points >= level.diem_toi_thieu) {
            return level.color || '#8e8e93';
          }
        }
      }
      if (points >= 5000) return '#007aff';
      if (points >= 1000) return '#ffcc00';
      return '#8e8e93';
    };

    const getColorHex = (colorStr) => {
      if (!colorStr) return null;
      let clean = colorStr.trim();
      if (clean.startsWith('#')) return clean;
      
      if (/^[0-9A-Fa-f]{6}$|^[0-9A-Fa-f]{3}$/.test(clean)) {
        return '#' + clean;
      }
      
      const hexMatch = clean.match(/[0-9A-Fa-f]{6}/);
      if (hexMatch) return '#' + hexMatch[0];

      const mappings = {
        'đỏ': '#FF3B30', 'do': '#FF3B30',
        'den': '#000000', 'đen': '#000000',
        'trắng': '#FFFFFF', 'trang': '#FFFFFF',
        'vàng': '#FFCC00', 'vang': '#FFCC00',
        'xanh': '#34C759', 'xanh dương': '#007AFF', 'xanh la': '#34C759',
        'hồng': '#FF2D55', 'hong': '#FF2D55',
        'xám': '#8E8E93', 'xam': '#8E8E93',
        'bạc': '#E5E5EA', 'bac': '#E5E5EA',
        'gold': '#D4AF37', 'silver': '#C0C0C0', 'space gray': '#545456'
      };
      const lower = clean.toLowerCase();
      if (mappings[lower]) return mappings[lower];
      
      if (/^[0-9A-Fa-f]+$/.test(clean)) {
        return '#' + clean.substring(0, 6);
      }
      
      return '#8e8e93';
    };

    const customersPendingCount = computed(() => {
      return (pendingRequestsCount.value || 0) + (pendingBusinessRequestsCount.value || 0);
    });

    const supportPendingCount = computed(() => {
      return (supportTickets.value || []).filter(t => t.trang_thai === 'cho_xu_ly' || t.trang_thai === 'dang_xu_ly').length;
    });

    const ordersPendingCount = computed(() => {
      return (orders.value || []).filter(o => o.status === 'cho_duyet').length;
    });

    const chatPendingCount = computed(() => {
      return Object.values(unreadChatStates.value).filter(val => val === true).length;
    });

    const lastProcessedAuditId = ref(parseInt(localStorage.getItem('last_processed_audit_id') || '0'));

    const auditPendingCount = computed(() => {
      if (!auditLogs.value || auditLogs.value.length === 0) return 0;
      if (lastProcessedAuditId.value === 0) {
        // Lần đầu chạy, đánh dấu để lại 3 bản ghi audit mới nhất làm mẫu trải nghiệm
        const sortedIds = auditLogs.value.map(l => l.id).sort((a, b) => b - a);
        const maxId = sortedIds[0] || 0;
        lastProcessedAuditId.value = Math.max(0, maxId - 3);
        localStorage.setItem('last_processed_audit_id', lastProcessedAuditId.value);
      }
      return auditLogs.value.filter(l => l.id > lastProcessedAuditId.value).length;
    });

    const markAllAuditAsProcessed = () => {
      const count = auditPendingCount.value;
      if (count === 0) {
        if (window.showToast) window.showToast("Thông báo", "Không có nhật ký audit nào mới cần xử lý.", "info");
        return;
      }

      const action = () => {
        const sortedIds = auditLogs.value.map(l => l.id).sort((a, b) => b - a);
        const maxId = sortedIds[0] || 0;
        lastProcessedAuditId.value = maxId;
        localStorage.setItem('last_processed_audit_id', maxId);
        if (window.showToast) window.showToast("Thành công", `Đã xác nhận xử lý toàn bộ ${count} nhật ký audit mới!`, "success");
      };

      if (window.showConfirm) {
        window.showConfirm(
          'Đọc tất cả nhật ký Audit',
          `Bạn có chắc chắn muốn xác nhận đã xem và xử lý xong toàn bộ ${count} nhật ký audit mới không?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#30D158" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>`,
          action
        );
      } else {
        if (confirm(`Bạn có chắc chắn muốn xác nhận đã xem và xử lý xong toàn bộ ${count} nhật ký audit mới không?`)) {
          action();
        }
      }
    };

    const markAllOrdersAsProcessed = async () => {
      const pending = orders.value.filter(o => o.status === 'cho_duyet');
      if (pending.length === 0) {
        if (window.showToast) window.showToast("Thông báo", "Không có đơn hàng nào cần xử lý.", "info");
        return;
      }
      
      const action = async () => {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        const promises = pending.map(order => 
          fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/don-hang/cap-nhat-trang-thai/${order.id}`, {
            method: 'PUT',
            headers: { 
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify({ trang_thai: 'da_duyet' })
          })
        );
        
        await Promise.all(promises);
        if (window.showToast) window.showToast("Thành công", `Đã phê duyệt toàn bộ ${pending.length} đơn hàng!`, "success");
        fetchOrders();
      };

      if (window.showConfirm) {
        window.showConfirm(
          'Phê duyệt tất cả đơn hàng',
          `Bạn có chắc chắn muốn phê duyệt toàn bộ ${pending.length} đơn hàng đang chờ không?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#30D158" stroke-width="1.5"><polyline points="20 6 9 17 4 12"></polyline></svg>`,
          action
        );
      } else {
        if (confirm(`Bạn có chắc chắn muốn phê duyệt toàn bộ ${pending.length} đơn hàng đang chờ không?`)) {
          await action();
        }
      }
    };

    const markAllCustomersAsProcessed = async () => {
      const total = pendingRequestsCount.value + pendingBusinessRequestsCount.value;
      if (total === 0) {
        if (window.showToast) window.showToast("Thông báo", "Không có yêu cầu nào cần xử lý.", "info");
        return;
      }
      
      const action = async () => {
        try {
          const [res1, res2] = await Promise.all([
            fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/support/reset-requests/resolve-all', { method: 'POST' }),
            fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/business-requests/approve-all', { method: 'POST' })
          ]);
          if (res1.ok && res2.ok) {
            if (window.showToast) window.showToast("Thành công", "Đã xử lý và phê duyệt toàn bộ các yêu cầu thành công!", "success");
            await Promise.all([fetchResetRequests(), fetchBusinessRequests(), fetchCustomers()]);
          }
        } catch (e) {
          console.error(e);
        }
      };

      if (window.showConfirm) {
        window.showConfirm(
          'Duyệt tất cả yêu cầu khách hàng',
          `Bạn có chắc chắn muốn phê duyệt & xử lý toàn bộ ${total} yêu cầu từ khách gửi không?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#30D158" stroke-width="1.5"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><polyline points="17 11 19 13 23 9"></polyline></svg>`,
          action
        );
      } else {
        if (confirm(`Bạn có chắc chắn muốn phê duyệt & xử lý toàn bộ ${total} yêu cầu từ khách gửi không?`)) {
          await action();
        }
      }
    };

    const markAllSupportAsProcessed = async () => {
      const pending = supportTickets.value.filter(t => t.trang_thai === 'cho_xu_ly' || t.trang_thai === 'dang_xu_ly');
      if (pending.length === 0) {
        if (window.showToast) window.showToast("Thông báo", "Không có yêu cầu hỗ trợ nào cần xử lý.", "info");
        return;
      }
      
      const action = async () => {
        const promises = pending.map(ticket => 
          fetch(`${window.API_BASE || 'http://127.0.0.1:8000'}/api/support/admin/tickets/${ticket.id}/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ trang_thai: 'da_xu_ly' })
          })
        );
        
        await Promise.all(promises);
        if (window.showToast) window.showToast("Thành công", `Đã đánh dấu giải quyết toàn bộ ${pending.length} yêu cầu hỗ trợ!`, "success");
        await fetchSupportTickets();
      };

      if (window.showConfirm) {
        window.showConfirm(
          'Giải quyết tất cả yêu cầu hỗ trợ',
          `Bạn có chắc chắn muốn đánh dấu giải quyết xong toàn bộ ${pending.length} yêu cầu hỗ trợ không?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#30D158" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path><polyline points="9 11 12 14 22 4"></polyline></svg>`,
          action
        );
      } else {
        if (confirm(`Bạn có chắc chắn muốn đánh dấu giải quyết xong toàn bộ ${pending.length} yêu cầu hỗ trợ không?`)) {
          await action();
        }
      }
    };

    const markAllChatsAsProcessed = () => {
      if (chatPendingCount.value === 0) {
        if (window.showToast) window.showToast("Thông báo", "Không có cuộc trò chuyện nào cần xử lý.", "info");
        return;
      }
      
      const action = () => {
        unreadChatStates.value = {};
        if (window.showToast) window.showToast("Thành công", "Đã đánh dấu xử lý xong toàn bộ tin nhắn trò chuyện!", "success");
      };

      if (window.showConfirm) {
        window.showConfirm(
          'Hoàn tất tất cả hội thoại',
          `Bạn có chắc chắn muốn đánh dấu đã đọc và xử lý xong toàn bộ cuộc trò chuyện đang chờ không?`,
          `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#30D158" stroke-width="1.5"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>`,
          action
        );
      } else {
        if (confirm(`Bạn có chắc chắn muốn đánh dấu đã đọc và xử lý xong toàn bộ cuộc trò chuyện đang chờ không?`)) {
          action();
        }
      }
    };

    return {
      apiBase: window.API_BASE || 'https://peach-store-backend.onrender.com',
      markAllOrdersAsProcessed,
      markAllCustomersAsProcessed,
      markAllSupportAsProcessed,
      markAllChatsAsProcessed,
      markAllAuditAsProcessed,
      customersPendingCount,
      supportPendingCount,
      ordersPendingCount,
      chatPendingCount,
      auditPendingCount,
      isSidebarCollapsed,
      activeTab,
      stats,
      activities,
      products,
      analyticsData,
      analyticsTab,
      revenueViewMode,
      formatTokens,
      requestsSvgPoints,
      requestsSvgAreaPoints,
      updateAiAnalytics,
      updateAnalyticsTopProducts,
      aiLogs,
      aiLogSearchQuery,
      filteredAiLogs,
      loadingAiLogs,
      fetchAiLogs,
      deleteAiLog,
      clearAllAiLogs,
      showAiConfigModal,
      aiConfigForm,
      saveAiConfig,
      categories,
      inventoryLogs,
      flashSales,
      vouchers,
      loyaltyLevels,
      showLoyaltyModal,
      loyaltyForm,
      showPointsModal,
      pointsForm,
      fetchLoyaltyLevels,
      openEditLoyaltyModal,
      hasPrivilege,
      togglePrivilege,
      saveLoyaltyConfig,
      openEditPointsModal,
      saveCustomerPoints,
      pushCampaigns,
      fetchPushCampaigns,
      reviews,
      supportTickets,
      selectedSupportTicket,
      loadingSupportTickets,
      fetchSupportTickets,
      updateSupportTicketStatus,
      fullscreenImageUrl,
      admins,
      paymentPartners,
      auditLogs,
      searchAuditQuery,
      filteredAuditLogs,
      systemConfig,
      settingsTab,
      saveSettings,
      cleanTempData,
      isSidebarCollapsed,
      refreshData,
      t,
      showEmployeeModal,
      isEditingEmployee,
      employeeForm,
      openAddEmployeeModal,
      openEditEmployeeModal,
      saveEmployee,
      onPhoneKeypress,
      onPhoneInput,
      onPhonePaste,
      deleteEmployee,
      schedules,
      todayDate,
      showRosterModal,
      selectedRosterEmployee,
      rosterForm,
      openRosterModal,
      saveRoster,
      deleteRoster,
      orders,
      customers,
      handleAvatarError,
      formatImageUrl,
      getMembershipRank,
      getRankColor,
      getColorHex,
      onSidebarToggle,
      updateOrderStatus,
      openEditOrderModal,
      showOrderEditModal,
      orderEditForm,
      saveOrder,
      deleteOrder,
      searchOrderQuery,
      orderSortKey,
      orderSortOrder,
      filteredOrders,
      sortOrders,
      selectedOrderIds,
      toggleOrderSelection,
      toggleSelectAllOrders,
      deleteSelectedOrders,
      activeStatusMenu,
      toggleStatusMenu,
      refreshData,
      fetchInventoryLogs,
      deleteInventoryLog,
      // Product CRUD
      showProductModal,
      isEditingProduct,
      productForm,
      productFormErrors,
      productVariantsPreview,
      productColorsPreview,
      validateProductForm,
      openAddProductModal,
      openEditProductModal,
      saveProduct,
      deleteProduct,
      handleFileUpload,
      handleGalleryUpload,
      activePairings,
      presetColors,
      toggleColor,
      togglePairCapacity,
      tempColor,
      addTempColor,
      isPairCapacitySelected,
      cleanDescription,
      getProductSpecsList,
      onNativeColorPicked,
      stringToColor,
      // Customer search
      customerFilterQuery,
      filteredCustomers,
      // Recovery requests
      customerSubTab,
      resetRequests,
      showVerifyModal,
      selectedRequest,
      verifyForm,
      isVerified,
      isMatched,
      matchedUser,
      verificationMessage,
      generatedPassword,
      generatedPin,
      isResetting,
      pendingRequestsCount,
      fetchResetRequests,
      openVerifyModal,
      verifyCustomer,
      resetPassword,
      resetPin,
      copyText,
      // Business requests
      businessRequests,
      pendingBusinessRequestsCount,
      fetchBusinessRequests,
      approveBusinessRequest,
      rejectBusinessRequest,
      showAdminChatModal,
      selectedChatCustomer,
      adminChatMessages,
      adminChatInputText,
      loadingAdminChat,
      openAdminChatModal,
      fetchAdminChatMessages,
      sendAdminChatMessage,
      showAdminChatLoadPrevious,
      showAdminChatLoadNext,
      loadAdminChatPreviousMessages,
      loadAdminChatNextMessages,
      adminChatVisibleStartIdx,
      allAdminChatMessages,
      unreadChatStates,
      fetchUnreadChatStates,
      // Customer CRUD
      showCustomerModal,
      isEditingCustomer,
      editingCustomerId,
      customerForm,
      fetchOrders,
      updateOrderStatus,
      openAddCustomerModal,
      openEditCustomerModal,
      saveCustomer,
      deleteCustomer,
      commonCapacities,
      isCapacitySelected,
      toggleCapacity,
      commonRams,
      isRamSelected,
      toggleRam,
      stringToColor,
      selectedCustomerIds,
      toggleCustomerSelection,
      toggleSelectAllCustomers,
      deleteSelectedCustomers,
      updateEmployeeRole,
      deleteEmployee,
      openAddEmployeeModal,
      openEditEmployeeModal,
      showEmployeeModal,
      employeeForm,
      isEditingEmployee,
      saveEmployee,
      selectedProductIds,
      toggleSelectAllProducts,
      deleteSelectedProducts,
      filterQuery,
      selectedCategory,
      filteredProducts,
      productSortKey,
      productSortOrder,
      sortProducts,
      formatPrice,
      formatDate,
      docSoTien,
      voucherFilterQuery,
      filteredVouchers,
      selectedVoucherIds,
      toggleVoucherSelection,
      toggleSelectAllVouchers,
      deleteSelectedVouchers,
      showVoucherModal,
      isEditingVoucher,
      editingVoucherId,
      voucherForm,
      fetchVouchers,
      openAddVoucherModal,
      openEditVoucherModal,
      saveVoucher,
      deleteVoucher,
      toggleVoucherStatus,
      // Shipping CRUD
      shippingUnits,
      selectedShippingIds,
      toggleShippingSelection,
      toggleSelectAllShipping,
      deleteSelectedShipping,
      showShippingModal,
      isEditingShipping,
      editingShippingId,
      shippingForm,
      fetchShippingUnits,
      openAddShippingModal,
      openEditShippingModal,
      saveShippingUnit,
      deleteShippingUnit,
      toggleShippingActive,
      // Payment CRUD
      selectedPaymentIds,
      togglePaymentSelection,
      toggleSelectAllPayments,
      deleteSelectedPayments,
      showPaymentModal,
      isEditingPayment,
      editingPaymentId,
      paymentForm,
      fetchPaymentPartners,
      openAddPaymentModal,
      openEditPaymentModal,
      savePaymentPartner,
      deletePaymentPartner,
      togglePaymentActive
    };
  }
};
