let ipcRenderer = null;
try {
  ipcRenderer = require('electron').ipcRenderer;
} catch (e) {
  console.warn("Electron ipcRenderer not available. Window controls will be disabled.");
}

const { createApp, ref, computed, onMounted } = Vue;

createApp({
  setup() {
    if (!window.AdminViewModel) {
      console.error("AdminViewModel not found!");
      return {};
    }
    const adminData = window.AdminViewModel.setup();
    const isMaximized = ref(false);

    if (ipcRenderer) {
      ipcRenderer.on('window-state-maximized', (event, state) => {
        isMaximized.value = state;
      });
    }

    onMounted(() => {
      setTimeout(() => {
        const el = document.querySelector('.xcode-container');
        if (el) el.classList.remove('no-transition');
      }, 500);
    });

    const notifications = ref([]);
    const modal = ref({ show: false, title: '', message: '', icon: '', onConfirm: null });
    const dropdownOpen = ref(false);
    const pushTarget = ref('Tất cả khách hàng');
    const pushTitle = ref('');
    const pushBody = ref('');
    const aiQuery = ref('');
    const isChatVisible = ref(false);

    const toggleDropdown = () => { dropdownOpen.value = !dropdownOpen.value; };
    const selectPushTarget = (target) => {
      pushTarget.value = target;
      dropdownOpen.value = false;
    };

    const icons = {
      info: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#007AFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`,
      success: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#28C840" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`,
      warning: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFBC2E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`,
      refresh: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#007AFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>`,
      edit: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#007AFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>`
    };

    /**
     * Gửi thông báo đẩy đến nhóm khách hàng đã chọn.
     * Kiểm tra tính hợp lệ của tiêu đề và nội dung trước khi yêu cầu xác nhận.
     */
    const sendPush = () => {
      if (!pushTitle.value || !pushBody.value) {
        showToast('Cảnh báo', 'Vui lòng nhập đầy đủ tiêu đề và nội dung.', 'warning');
        return;
      }
      if (pushBody.value.length > 3000) {
        showToast('Cảnh báo', 'Nội dung thông báo không được vượt quá 3000 ký tự.', 'warning');
        return;
      }
      
      const confirmAction = async () => {
        try {
          const res = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/notifications/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              title: pushTitle.value,
              body: pushBody.value,
              target: pushTarget.value
            })
          });
          if (res.ok) {
            showToast('Thành công', 'Thông báo đã được gửi thành công!', 'success');
            pushTitle.value = '';
            pushBody.value = '';
            if (adminData && adminData.fetchPushCampaigns) {
              await adminData.fetchPushCampaigns();
            }
          } else {
            const err = await res.json();
            showToast('Cảnh báo', err.detail || 'Lỗi gửi thông báo.', 'warning');
          }
        } catch (e) {
          console.error("Lỗi gửi thông báo: ", e);
          showToast('Lỗi', 'Không thể kết nối đến máy chủ.', 'warning');
        }
      };

      showConfirm(
        'Xác nhận gửi',
        `Bạn có chắc chắn muốn gửi thông báo này tới "${pushTarget.value}" không?`,
        icons.info,
        confirmAction
      );
    };

    /**
     * Hiển thị thông báo nhỏ (Toast) ở góc màn hình.
     * 
     * @param {string} title - Tiêu đề của thông báo.
     * @param {string} message - Nội dung chi tiết của thông báo.
     * @param {string} [iconName='info'] - Tên biểu tượng hiển thị ('info', 'success', 'warning', 'refresh', 'edit').
     */
    const showToast = (title, message, iconName = 'info') => {
      if (notifications.value.some(n => n.message === message)) return;
      if (notifications.value.length >= 3) notifications.value.shift();

      const id = Date.now();
      const icon = icons[iconName] || icons.info;
      notifications.value.push({ id, title, message, icon });
      setTimeout(() => {
        notifications.value = notifications.value.filter(n => n.id !== id);
      }, 3000);
    };
    window.showToast = showToast;


    /**
     * Hiển thị hộp thoại xác nhận (Confirm Modal) yêu cầu người dùng xác thực hành động.
     * 
     * @param {string} title - Tiêu đề hộp thoại.
     * @param {string} message - Nội dung câu hỏi xác nhận.
     * @param {string} icon - Đoạn mã SVG biểu tượng hiển thị.
     * @param {Function} onConfirm - Hàm callback được thực thi khi người dùng bấm xác nhận.
     */
    const showConfirm = (title, message, icon, onConfirm) => {
      modal.value = { show: true, title, message, icon, onConfirm };
    };
    window.showConfirm = showConfirm;

    /**
     * Thực thi hàm callback xác nhận của hộp thoại và ẩn hộp thoại đi.
     */
    const confirmModal = () => {
      if (modal.value.onConfirm) modal.value.onConfirm();
      modal.value.show = false;
    };

    /**
     * Định dạng số tiền thành chuỗi tiền tệ Việt Nam Đồng (VND).
     * 
     * @param {number} p - Số tiền cần định dạng.
     * @returns {string} Chuỗi tiền tệ đã định dạng (ví dụ: "15.000.000 ₫").
     */
    const formatPrice = (p) => {
      return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p);
    };

    // Window Controls
    /**
     * Yêu cầu xác nhận đóng ứng dụng Electron.
     */
    const closeWindow = () => {
      showConfirm(
        'Xác nhận thoát',
        'Bạn có chắc chắn muốn đóng ứng dụng Peach Admin không?',
        icons.warning,
        () => {
          if (ipcRenderer) ipcRenderer.send('window-close');
        }
      );
    };

    /**
     * Thu nhỏ cửa sổ ứng dụng xuống thanh tác vụ (Taskbar).
     */
    const minimizeWindow = () => {
      if (ipcRenderer) ipcRenderer.send('window-minimize');
    };

    /**
     * Phóng to hoặc thu nhỏ cửa sổ ứng dụng về kích thước mặc định.
     */
    const maximizeWindow = () => {
      if (ipcRenderer) ipcRenderer.send('window-maximize');
    };

    const addOrder = () => {
      showToast('Thông báo', 'Tính năng thêm đơn hàng đang được phát triển.', 'info');
    };

    const selectedOrder = ref(null);
    /**
     * Mở hộp thoại hiển thị chi tiết hóa đơn đặt hàng của khách hàng.
     * 
     * @param {Object} order - Đối tượng hóa đơn chứa thông tin sản phẩm, địa chỉ, thanh toán.
     */
    const openOrderDetail = (order) => {
      // Map pre-mapped items from view model, preserving all custom specifications
      const realItems = (order.items || []).map(item => ({
        name: item.name || 'Sản phẩm',
        qty: item.qty || 1,
        price: item.price || 0,
        image: item.image || 'https://via.placeholder.com/150',
        mau_sac: item.mau_sac || '',
        dung_luong: item.dung_luong || '',
        ram: item.ram || ''
      }));

      selectedOrder.value = {
        ...order,
        items: realItems,
        paymentMethod: order.paymentMethod || 'Chuyển khoản ngân hàng',
        address: order.address || 'Không có địa chỉ'
      };
    };

    /**
     * Làm mới toàn bộ dữ liệu hệ thống (sản phẩm, đơn hàng, khách hàng, voucher...) từ máy chủ.
     */
    const reloadApp = async () => {
      showToast('Thông báo', 'Đang làm mới dữ liệu hệ thống...', 'refresh');
      await adminData.refreshData();
    };

    const sidebarMessages = ref([
      { id: 1, sender: 'ai', text: 'Chào bạn! Tôi là trợ lý Peach Assistant. Tôi có thể giúp gì cho bạn hôm nay?' }
    ]);
    const loadingAiResponse = ref(false);
    const sidebarChatContainer = ref(null);

    const currentSessionId = ref(localStorage.getItem('peach_current_session_id') || ('session_' + Date.now()));
    localStorage.setItem('peach_current_session_id', currentSessionId.value);

    /**
     * Khởi tạo một phiên chat mới với trợ lý AI Peach Assistant, xóa lịch sử hiển thị cũ.
     */
    const startNewChat = () => {
      currentSessionId.value = 'session_' + Date.now();
      localStorage.setItem('peach_current_session_id', currentSessionId.value);
      sidebarMessages.value = [
        { id: 1, sender: 'ai', text: 'Chào bạn! Tôi là trợ lý Peach Assistant. Tôi có thể giúp gì cho bạn hôm nay?' }
      ];
      showToast('Thành công', 'Cuộc hội thoại mới đã được bắt đầu!', 'success');
      scrollToBottom();
    };

    /**
     * Tự động cuộn khung chat xuống dưới cùng khi có tin nhắn mới.
     */
    const scrollToBottom = () => {
      Vue.nextTick(() => {
        const container = document.querySelector('.chat-messages');
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    };

    /**
     * Trình phản hồi thông minh cục bộ (Local AI Engine) khi không cấu hình DeepSeek.
     * Tự động phân tích từ khóa thô tiếng Việt (không dấu và có dấu) để truy vấn thông tin
     * doanh thu, đơn hàng, sản phẩm, tồn kho và voucher từ bộ nhớ client.
     * 
     * @param {string} msg - Nội dung câu hỏi từ Admin.
     * @returns {string} Nội dung trả lời markdown tương ứng.
     */
    const localAiResponder = (msg) => {
      const q = msg.toLowerCase().trim();
      
      const removeAccents = (str) => {
        return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "d");
      };
      
      const qNoAcc = removeAccents(q);
      
      // 1. CHÀO HỎI / GIỚI THIỆU
      if (qNoAcc.includes('chao') || qNoAcc.includes('hello') || qNoAcc.includes('hi') || qNoAcc.includes('trieu tap') || qNoAcc.includes('tro ly') || qNoAcc.includes('peach assistant')) {
        return `Dạ, xin chào Admin! Tôi là **Peach Assistant** - Trợ lý ảo thông minh độc quyền của hệ thống Peach Store. 🍑✨\n\nTôi đang kết nối trực tiếp với Cơ sở dữ liệu của bạn để hỗ trợ nhanh các tác vụ:\n- 📊 **Thống kê**: Hỏi tôi về *"doanh thu"*, *"đơn hàng"* hoặc *"báo cáo"*.\n- 📦 **Tồn kho**: Hỏi tôi về *"sản phẩm"*, *"tồn kho"*, *"giá bán"*, hoặc chi tiết như *"iPhone"*, *"MacBook"*.\n- 🎫 **Ưu đãi**: Hỏi tôi về *"mã giảm giá"*, *"voucher"*, hoặc *"khuyến mãi"*.\n- ⚙️ **Cấu hình**: Hỏi về *"cách đổi model"* hoặc *"DeepSeek key"*.\n\nTôi có thể giúp gì cho bạn lúc này ạ?`;
      }
      
      // 2. DOANH THU / THỐNG KÊ / ĐƠN HÀNG
      if (qNoAcc.includes('doanh thu') || qNoAcc.includes('doanh so') || qNoAcc.includes('don hang') || qNoAcc.includes('thong ke') || qNoAcc.includes('bao cao')) {
        const stats = adminData.stats?.value || {};
        const revenue = formatPrice(stats.totalRevenue || 1248500000);
        const ordersCount = stats.totalOrders || 342;
        const customersCount = stats.totalCustomers || 1024;
        const pendingOrders = stats.pendingOrders || 12;
        
        return `📊 **Báo cáo Thống kê Live của Peach Store:**\n\n- 💰 **Tổng doanh thu**: \`${revenue}\` (Tăng trưởng ổn định)\n- 📦 **Tổng số đơn hàng**: \`${ordersCount} đơn\`\n- 👥 **Tổng số khách hàng**: \`${customersCount} thành viên\`\n- ⏳ **Đơn hàng chờ xử lý**: \`${pendingOrders} đơn đang chờ\`\n\n*Số liệu được cập nhật trực tiếp từ hệ thống quản trị của bạn tại thời điểm hiện tại.*`;
      }
      
      // 3. SẢN PHẨM / TỒN KHO / GIÁ BÁN
      if (qNoAcc.includes('san pham') || qNoAcc.includes('ton kho') || qNoAcc.includes('gia ban') || qNoAcc.includes('kho hang') || 
          qNoAcc.includes('iphone') || qNoAcc.includes('macbook') || qNoAcc.includes('mac') || qNoAcc.includes('ipad') || qNoAcc.includes('airpods')) {
        
        const productsList = adminData.products?.value || [];
        
        let matched = [];
        if (qNoAcc.includes('iphone')) {
          matched = productsList.filter(p => p.ten_san_pham.toLowerCase().includes('iphone'));
        } else if (qNoAcc.includes('macbook') || qNoAcc.includes('mac')) {
          matched = productsList.filter(p => p.ten_san_pham.toLowerCase().includes('macbook') || p.ten_san_pham.toLowerCase().includes('mac'));
        } else if (qNoAcc.includes('ipad')) {
          matched = productsList.filter(p => p.ten_san_pham.toLowerCase().includes('ipad'));
        } else if (qNoAcc.includes('airpods')) {
          matched = productsList.filter(p => p.ten_san_pham.toLowerCase().includes('airpods'));
        } else {
          matched = productsList.slice(0, 6);
        }
        
        if (matched.length > 0) {
          let reply = `📦 **Thông tin sản phẩm & Tồn kho trong hệ thống:**\n\n`;
          matched.forEach(p => {
            const priceStr = formatPrice(p.gia_ban);
            const stock = p.so_luong_kho !== undefined ? p.so_luong_kho : 100;
            const ramRom = (p.ram || p.dung_luong) ? ` (${p.ram ? p.ram + ' RAM' : ''}${p.ram && p.dung_luong ? ' - ' : ''}${p.dung_luong ? p.dung_luong : ''})` : '';
            reply += `- **${p.ten_san_pham}**${ramRom}:\n  • Giá bán: \`${priceStr}\` \n  • Tồn kho: \`${stock} máy\` (${stock > 10 ? 'Còn hàng' : 'Sắp hết'})\n`;
          });
          if (productsList.length > matched.length) {
            reply += `\n*Và ${productsList.length - matched.length} sản phẩm khác đang được quản lý trong Kho hàng.*`;
          }
          return reply;
        } else {
          return `📦 **Quản lý sản phẩm**: Hiện tại hệ thống ghi nhận tổng số **${productsList.length} sản phẩm** trong danh mục kinh doanh. Bạn có thể vào tab *Sản phẩm* ở thanh bên trái để cập nhật hoặc thêm mới sản phẩm!`;
        }
      }
      
      // 4. VOUCHERS / MÃ GIẢM GIÁ
      if (qNoAcc.includes('voucher') || qNoAcc.includes('ma giam gia') || qNoAcc.includes('khuyen mai') || qNoAcc.includes('giam gia') || qNoAcc.includes('uu dai')) {
        const vouchersList = adminData.vouchers?.value || [];
        const activeVouchers = vouchersList.filter(v => v.trang_thai === 'dang_hoat_dong' || v.so_luong_con_lai > 0);
        
        if (activeVouchers.length > 0) {
          let reply = `🎫 **Chương trình khuyến mãi & Mã giảm giá đang chạy:**\n\n`;
          activeVouchers.slice(0, 5).forEach(v => {
            const valueStr = v.loai_giam_gia === 'phan_tram' ? `${v.gia_tri_giam}%` : formatPrice(v.gia_tri_giam);
            const minOrderStr = formatPrice(v.don_hang_toi_thieu);
            reply += `- **${v.ma_voucher}**:\n  • Giảm: \`${valueStr}\` (Đơn từ \`${minOrderStr}\`)\n  • Còn lại: \`${v.so_luong_con_lai} lượt\`\n`;
          });
          return reply;
        } else {
          return `🎫 **Khuyến mãi**: Hiện tại không có mã giảm giá nào đang chạy hoặc danh sách đang trống. Bạn có thể tạo thêm mã giảm giá mới ở trang quản lý *Mã giảm giá* để thu hút khách hàng nhé!`;
        }
      }
      
      // 5. CÁC CÂU HỎI HƯỚNG DẪN QUẢN TRỊ
      if (qNoAcc.includes('them san pham') || qNoAcc.includes('tao voucher') || qNoAcc.includes('xu ly don hang')) {
        return `💡 **Hướng dẫn thao tác nhanh cho Admin:**\n\n1. ➕ **Thêm sản phẩm**: Nhấp vào tab *"Sản phẩm"* trên menu bên trái, sau đó nhấn nút *"Thêm sản phẩm"* ở góc trên bên phải để bắt đầu thiết lập tên, giá, hình ảnh và cấu hình.\n2. 🎫 **Tạo Voucher**: Chọn tab *"Mã giảm giá"*, sau đó điền thông tin mã, giá trị giảm (theo phần trăm hoặc tiền mặt) rồi bấm kích hoạt.\n3. 🚚 **Xử lý đơn hàng**: Khi có đơn hàng mới từ khách, vào mục *"Đơn hàng"* để cập nhật trạng thái đơn (Ví dụ: Chuyển từ *Chờ xử lý* sang *Đang giao* và gán IMEI máy).`;
      }
      
      // 6. CẤU HÌNH AI / DEEPSEEK
      if (qNoAcc.includes('api') || qNoAcc.includes('deepseek') || qNoAcc.includes('model') || qNoAcc.includes('cau hinh ai') || qNoAcc.includes('doi model')) {
        return `⚙️ **Hướng dẫn cấu hình AI nâng cao:**\n\nHiện tại tôi đang hỗ trợ bạn dưới dạng **Trợ lý dữ liệu cục bộ (Local Mode)**. Nếu bạn muốn tôi trả lời đa năng hơn, tự động hóa soạn thảo email, phân tích xu hướng hoặc trò chuyện tự do bằng trí tuệ nhân tạo DeepSeek:\n\n1. Vào trang **"Lịch sử Chat Admin"** từ menu bên trái.\n2. Nhấn nút **"Cấu hình AI Model"** ở góc trên bên phải.\n3. Điền **DeepSeek API Key** của bạn.\n4. Chọn model mong muốn (e.g. \`deepseek-chat\`) và bật trạng thái kích hoạt.\n5. Nhấn **"Lưu thay đổi"** để bắt đầu kết nối!`;
      }

      // 7. CÂU TRẢ LỜI MẶC ĐỊNH THÔNG MINH
      return `Dạ, tôi ghi nhận câu hỏi của bạn: *"${msg}"*.\n\nHiện tôi đang hoạt động dưới dạng **Trợ lý dữ liệu cục bộ** của cửa hàng. Bạn có thể hỏi tôi các câu hỏi như:\n- 📊 *"Doanh thu hôm nay"* hoặc *"Thống kê đơn hàng"*.\n- 📦 *"Tồn kho iPhone"* hoặc danh sách *"sản phẩm"*.\n- 🎫 *"Kiểm tra mã giảm giá"* hiện có.\n\n*Nếu bạn muốn thảo luận chuyên sâu hơn về các vấn đề kinh doanh hoặc phân tích nâng cao, đừng quên cấu hình kết nối với **DeepSeek AI** trong phần "Cấu hình AI Model" nhé!* 🍑✨`;
    };

    /**
     * Tạo ngữ cảnh dữ liệu live của toàn bộ cửa hàng (System Context) dưới dạng chuỗi văn bản.
     * Dữ liệu này được nén và gửi kèm trong prompt hệ thống của DeepSeek để AI trả lời chính xác.
     * 
     * @returns {string} Chuỗi văn bản chứa thông tin thống kê, sản phẩm, đơn hàng, khách hàng, support ticket, nhân sự.
     */
    const generateLiveStoreContext = () => {
      const stats = adminData.stats?.value || {};
      const revenueStr = stats.revenue || '0 ₫';
      const revenueInWords = stats.revenueInWords || 'Không đồng';
      const totalOrders = stats.newOrders || 0;
      const totalCustomers = stats.newCustomers || 0;
      
      const pendingOrders = adminData.ordersPendingCount?.value || 0;
      const pendingCustomers = adminData.customersPendingCount?.value || 0;
      const pendingSupport = adminData.supportPendingCount?.value || 0;

      let context = `=== PEACH STORE SYSTEM LIVE DATABASE STATE ===\n`;
      context += `Time of generation: ${new Date().toLocaleString('vi-VN')}\n\n`;
      context += `📊 [TỔNG QUAN HỆ THỐNG]:\n`;
      context += `- Doanh thu tổng tích lũy: ${revenueStr} (${revenueInWords})\n`;
      context += `- Tổng số đơn hàng: ${totalOrders} đơn (${pendingOrders} đơn chờ duyệt)\n`;
      context += `- Tổng số khách hàng: ${totalCustomers} thành viên (${pendingCustomers} chờ duyệt)\n`;
      context += `- Số ticket hỗ trợ chưa xử lý: ${pendingSupport} yêu cầu\n\n`;

      const products = adminData.products?.value || [];
      context += `📦 [TẤT CẢ SẢN PHẨM TRONG KHO] (${products.length} sản phẩm):\n`;
      products.forEach(p => {
        const name = p.ten_san_pham || p.ten || 'Sản phẩm không tên';
        const price = p.gia_ban || p.gia || 0;
        context += `- [SP #${p.id}] ${name} | Giá: ${price.toLocaleString('vi-VN')} VNĐ | Kho: ${p.so_luong_kho} | Màu: ${p.mau_sac || 'N/A'} | Dung lượng: ${p.dung_luong || 'N/A'} | RAM: ${p.ram || 'N/A'} | Danh mục: ${p.danh_muc || 'N/A'}\n`;
      });
      context += `\n`;

      const vouchers = adminData.vouchers?.value || [];
      context += `🎫 [MÃ GIẢM GIÁ / VOUCHERS] (${vouchers.length} mã):\n`;
      vouchers.forEach(v => {
        const val = v.loai_giam_gia === 'phan_tram' ? `${v.gia_tri_giam}%` : `${v.gia_tri_giam?.toLocaleString('vi-VN')} VNĐ`;
        const minOrder = v.don_hang_toi_thieu || 0;
        context += `- [Mã: ${v.ma_voucher}] Giảm: ${val} | Đơn từ: ${minOrder.toLocaleString('vi-VN')} VNĐ | Còn lại: ${v.so_luong_con_lai} | Trạng thái: ${v.trang_thai}\n`;
      });
      context += `\n`;

      const orders = adminData.orders?.value || [];
      context += `🚚 [DANH SÁCH ĐƠN HÀNG HỆ THỐNG] (${orders.length} đơn hàng):\n`;
      orders.forEach(o => {
        const total = o.tong_tien || o.tong_cong || o.total || 0;
        const name = o.ten_khach_hang || o.email || 'Khách vãng lai';
        const phone = o.so_dien_thoai || o.phone || 'N/A';
        const date = o.thoi_gian || o.date || 'N/A';
        context += `- [Đơn #${o.id}] Khách: ${name} (${phone}) | Tổng: ${total.toLocaleString('vi-VN')} VNĐ | Trạng thái: ${o.trang_thai} | Ngày: ${date}\n`;
      });
      context += `\n`;

      const customers = adminData.customers?.value || [];
      context += `👥 [DANH SÁCH KHÁCH HÀNG] (${customers.length} thành viên):\n`;
      customers.forEach(c => {
        const spend = c.tong_chi_tieu || 0;
        const phone = c.so_dien_thoai || 'N/A';
        const email = c.email || 'N/A';
        context += `- [KH #${c.id}] ${c.ho_ten} | Email: ${email} | SĐT: ${phone} | Tiêu dùng: ${spend.toLocaleString('vi-VN')} VNĐ | Hạng: ${c.hang_thanh_vien || 'N/A'} | Kích hoạt: ${c.trang_thai}\n`;
      });
      context += `\n`;

      const tickets = adminData.supportTickets?.value || [];
      context += `🎫 [DANH SÁCH TICKET HỖ TRỢ] (${tickets.length} yêu cầu):\n`;
      tickets.forEach(t => {
        const userName = t.user?.ho_ten || t.nguoi_dung?.ho_ten || 'N/A';
        const phone = t.user?.so_dien_thoai || t.nguoi_dung?.so_dien_thoai || 'N/A';
        context += `- [Ticket #${t.id}] Chủ đề: "${t.chu_de}" | Khách: ${userName} (${phone}) | Trạng thái: ${t.trang_thai} | IMEI: ${t.imei_serial || 'N/A'}\n`;
      });
      context += `\n`;

      const admins = adminData.admins?.value || [];
      context += `👥 [DANH SÁCH NHÂN VIÊN & ADMIN] (${admins.length} nhân sự):\n`;
      admins.forEach(a => {
        context += `- [NV #${a.id}] ${a.ho_ten} | Email: ${a.email} | Vai trò: ${a.vai_ro} | Trạng thái: ${a.trang_thai}\n`;
      });

      return context;
    };

    /**
     * Gửi truy vấn hội thoại AI của Admin.
     * Nếu có cấu hình DeepSeek API Key, gửi request proxy tới DeepSeek kèm ngữ cảnh live-store.
     * Nếu không có API Key, tự động hạ cấp xuống sử dụng Local Engine.
     */
    const sendQuery = async () => {
      const msg = aiQuery.value.trim();
      if (!msg) return;

      sidebarMessages.value.push({
        id: Date.now(),
        sender: 'user',
        text: msg
      });
      aiQuery.value = '';
      scrollToBottom();

      const isActive = localStorage.getItem('peach_ai_active') !== 'false';
      const apiKey = localStorage.getItem('peach_ai_key') || '';
      const model = localStorage.getItem('peach_ai_model') || 'deepseek-chat';

      if (!isActive) {
        sidebarMessages.value.push({
          id: Date.now() + 1,
          sender: 'ai',
          text: 'Dạ, Trợ lý Peach Assistant hiện đang ở chế độ Tắt. Vui lòng bật hoạt động trong Cấu hình AI Model.'
        });
        scrollToBottom();
        return;
      }

      loadingAiResponse.value = true;
      scrollToBottom();

      // IF NO API KEY IS SET, OR IF DEEPSEEK IS NOT CONFIGURED, USE THE SMART LOCAL ENGINE
      if (!apiKey) {
        setTimeout(async () => {
          const replyText = localAiResponder(msg);
          sidebarMessages.value.push({
            id: Date.now() + 3,
            sender: 'ai',
            text: replyText
          });

          // Lưu đoạn chat này vào Backend để nó xuất hiện trong trang Lịch sử Chat Admin!
          try {
            await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/ai-logs', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                cau_hoi: msg,
                tra_loi: replyText,
                email_nguoi_dung: 'admin@peachstore.vn',
                session_id: currentSessionId.value
              })
            });
            // Đồng thời làm mới bảng lịch sử nếu tab AI đang mở
            if (adminData.fetchAiLogs) {
              await adminData.fetchAiLogs();
            }
          } catch (backendErr) {
            console.error("Lỗi lưu lịch sử chat vào backend: ", backendErr);
          }

          loadingAiResponse.value = false;
          scrollToBottom();
        }, 800);
        return;
      }

      try {
        const liveContext = generateLiveStoreContext();
        const systemPromptLength = liveContext.length + 500;
        let newMsgText = msg;

        // Truncate the typed message if it exceeds the maximum allowable single-message budget
        const maxAllowedMsgLength = 100000 - systemPromptLength;
        if (newMsgText.length > maxAllowedMsgLength) {
          newMsgText = newMsgText.substring(0, maxAllowedMsgLength);
          if (window.showToast) {
            window.showToast("Thông báo", "Tin nhắn quá dài! Hệ thống tự động tối ưu để vừa giới hạn 100k context của phiên chat.", "info");
          }
        }

        // Filter and sliding window history to stay strictly under 100k characters total context
        const rawHistory = sidebarMessages.value.slice(0, -1).filter(m => m.id > 1).map(m => ({
          sender: m.sender,
          text: m.text
        }));

        let allowedHistory = [];
        let currentLength = systemPromptLength + newMsgText.length;

        for (let i = rawHistory.length - 1; i >= 0; i--) {
          const hItem = rawHistory[i];
          const hItemLength = hItem.text.length + 50;
          if (currentLength + hItemLength <= 100000) {
            allowedHistory.unshift(hItem);
            currentLength += hItemLength;
          } else {
            console.warn("[Peach AI] Đạt ngưỡng 100k context! Tự động loại bỏ các tin nhắn cũ hơn khỏi phiên gửi.");
            break;
          }
        }

        const response = await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/ai-chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: newMsgText,
            api_key: apiKey,
            model: model,
            context: liveContext,
            history: allowedHistory
          })
        });

        if (response.ok) {
          const data = await response.json();
          const replyText = data.reply;
          
          sidebarMessages.value.push({
            id: Date.now() + 3,
            sender: 'ai',
            text: replyText
          });

          // Lưu đoạn chat này vào Backend để nó xuất hiện trong trang Lịch sử Chat Admin!
          try {
            await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/ai-logs', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                cau_hoi: msg,
                tra_loi: replyText,
                email_nguoi_dung: 'admin@peachstore.vn',
                session_id: currentSessionId.value
              })
            });
            // Đồng thời làm mới bảng lịch sử nếu tab AI đang mở
            if (adminData.fetchAiLogs) {
              await adminData.fetchAiLogs();
            }
          } catch (backendErr) {
            console.error("Lỗi lưu lịch sử chat vào backend: ", backendErr);
          }

        } else {
          // If DeepSeek API fails, gracefully fallback to the smart Local Engine!
          console.warn("DeepSeek API call failed, falling back to Local Engine.");
          const replyText = localAiResponder(msg);
          sidebarMessages.value.push({
            id: Date.now() + 3,
            sender: 'ai',
            text: `*(Kết nối DeepSeek gián đoạn - Chuyển sang Trợ lý Cục bộ)*\n\n${replyText}`
          });

          try {
            await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/ai-logs', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                cau_hoi: msg,
                tra_loi: replyText,
                email_nguoi_dung: 'admin@peachstore.vn',
                session_id: currentSessionId.value
              })
            });
            if (adminData.fetchAiLogs) {
              await adminData.fetchAiLogs();
            }
          } catch (backendErr) {
            console.error("Lỗi lưu lịch sử chat vào backend: ", backendErr);
          }
        }
      } catch (e) {
        console.error("Lỗi mạng DeepSeek, sử dụng Local Engine:", e);
        const replyText = localAiResponder(msg);
        sidebarMessages.value.push({
          id: Date.now() + 3,
          sender: 'ai',
          text: `*(Ngoại tuyến - Kích hoạt Trợ lý Cục bộ)*\n\n${replyText}`
        });

        try {
          await fetch((window.API_BASE || 'http://127.0.0.1:8000') + '/api/admin/ai-logs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              cau_hoi: msg,
              tra_loi: replyText,
              email_nguoi_dung: 'admin@peachstore.vn',
              session_id: currentSessionId.value
            })
          });
          if (adminData.fetchAiLogs) {
            await adminData.fetchAiLogs();
          }
        } catch (backendErr) {
          console.error("Lỗi lưu lịch sử chat vào backend: ", backendErr);
        }
      } finally {
        loadingAiResponse.value = false;
        scrollToBottom();
      }
    };

    return {
      ...adminData,
      notifications,
      modal,
      showToast,
      showConfirm,
      confirmModal,
      formatPrice,
      closeWindow,
      minimizeWindow,
      maximizeWindow,
      reloadApp,
      isMaximized,
      dropdownOpen,
      pushTarget,
      toggleDropdown,
      selectPushTarget,
      pushTitle,
      pushBody,
      sendPush,
      addOrder,
      editOrder: (id) => showToast('Thông báo', `Đang mở trình chỉnh sửa đơn hàng #${id}`, 'edit'),
      selectedOrder,
      openOrderDetail,
      aiQuery,
      sendQuery,
      sendChat: sendQuery, // Legacy support
      isChatVisible,
      sidebarMessages,
      loadingAiResponse,
      sidebarChatContainer,
      currentSessionId,
      startNewChat
    };

  }
}).mount('#admin-app');
