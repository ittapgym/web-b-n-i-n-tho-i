  <template>
    <div class="trang-chu">
      <main class="content-reveal">
        <!-- HERO: iPhone 17 Pro Max -->
        <section class="hero-cinematic">
          <div class="hero-text-overlay">
            <h1 class="hero-title">iPhone 17 Pro Max</h1>
            <p class="hero-subtitle">Đặt hàng ngay hôm nay!</p>
            <div class="hero-actions">
              <AppleButton variant="primary" @click="router.push('/dien-thoai')">Sở hữu ngay</AppleButton>
              <a href="#" @click.prevent="router.push('/dien-thoai')" class="apple-link">Tìm hiểu thêm</a>
            </div>
          </div>
          <div class="hero-image-wrap">
            <img src="../assets/images/banners/hero.jpg" alt="iPhone 17 Pro Max" class="hero-img animate-zoom" />
          </div>
        </section>

        <!-- FEATURE: A19 Pro -->
        <section class="cinematic-feature">
          <div class="feature-container">
            <div class="feature-video">
              <video autoplay muted loop playsinline>
                <source src="../assets/images/video/bander.mp4" type="video/mp4" />
              </video>
            </div>
            <div class="feature-text">
              <h2>Sức mạnh của A19 Pro.</h2>
              <p>Hiệu năng vượt đỉnh. Đồ họa chân thực. Trí tuệ nhân tạo thế hệ mới tích hợp sâu trong hệ thống.</p>
            </div>
          </div>
        </section>

        <!-- LINEUP: iPhone -->
        <section class="lineup-section">
          <div class="lineup-content">
            <h2 class="section-title">iPhone</h2>
            <p class="section-subtitle">Khám phá dòng sản phẩm iPhone mới nhất.</p>
            <div class="lineup-actions">
              <AppleButton variant="primary" class="pill-btn" @click="router.push('/dien-thoai')">Tìm hiểu thêm</AppleButton>
              <AppleButton variant="secondary" class="pill-btn" @click="router.push('/dien-thoai')">Mua iPhone</AppleButton>
            </div>
          </div>
        </section>

        <!-- PROMO GRID -->
        <section class="promo-grid">
          <div class="grid-container">
            <!-- iPad Air -->
            <div class="promo-card">
              <div class="promo-header">
                <h2 class="promo-title">iPad <span class="air-text">air</span></h2>
                <p class="promo-subtitle">Mạnh mẽ vượt trội với chip M4.</p>
                <div class="promo-actions">
                  <AppleButton variant="primary" class="pill-btn primary grid-btn" @click="router.push('/may-tinh-bang')">Tìm hiểu thêm</AppleButton>
                  <AppleButton variant="secondary" class="pill-btn secondary grid-btn" @click="router.push('/may-tinh-bang')">Mua ngay</AppleButton>
                </div>
              </div>
              <img src="../assets/images/banners/promo_ipad_air_m4.svg" class="promo-img" alt="iPad Air" />
            </div>

            <!-- Watch -->
            <div class="promo-card">
              <div class="promo-header">
                <h2 class="promo-title watch-title">
                  Watch
                  <span class="series-text">Series 11</span>
                </h2>
                <p class="promo-subtitle">Người đồng hành hoàn hảo cho sức khỏe của bạn.</p>
                <div class="promo-actions">
                  <AppleButton variant="primary" class="pill-btn primary grid-btn" @click="router.push('/phu-kien')">Tìm hiểu thêm</AppleButton>
                  <AppleButton variant="secondary" class="pill-btn secondary grid-btn" @click="router.push('/phu-kien')">Mua ngay</AppleButton>
                </div>
              </div>
              <img src="../assets/images/banners/promo_apple_watch_series_11.svg" class="promo-img" alt="Watch" />
            </div>

            <!-- MacBook Air -->
            <div class="promo-card">
              <div class="promo-header">
                <h2 class="promo-title">MacBook <span class="air-text">air</span></h2>
                <p class="promo-subtitle">Siêu mỏng. Siêu nhẹ. Siêu mạnh mẽ với chip M3.</p>
                <div class="promo-actions">
                  <AppleButton variant="primary" class="pill-btn primary grid-btn" @click="router.push('/laptop')">Tìm hiểu thêm</AppleButton>
                  <AppleButton variant="secondary" class="pill-btn secondary grid-btn" @click="router.push('/laptop')">Mua ngay</AppleButton>
                </div>
              </div>
              <img src="../assets/images/banners/promo_macbook_air_m5.svg" class="promo-img" alt="MacBook" />
            </div>

            <!-- AirPods -->
            <div class="promo-card">
              <div class="promo-header">
                <h2 class="promo-title">AirPods <span class="pro-text">Pro</span></h2>
                <p class="promo-subtitle">Âm thanh sống động. Chống ồn chủ động.</p>
                <div class="promo-actions">
                  <AppleButton variant="primary" class="pill-btn primary grid-btn" @click="router.push('/phu-kien')">Tìm hiểu thêm</AppleButton>
                  <AppleButton variant="secondary" class="pill-btn secondary grid-btn" @click="router.push('/phu-kien')">Mua ngay</AppleButton>
                </div>
              </div>
              <img src="../assets/images/banners/promo_airpodspro_3.svg" class="promo-img" alt="AirPods" />
            </div>
          </div>
        </section>

        <!-- TRADE IN -->
        <section class="trade-in-banner">
          <div class="banner-inner">
            <div class="banner-text">
              <span class="label">Apple Trade In</span>
              <h2 class="title">Thu cũ đổi mới.<br/>Lên đời dễ dàng.</h2>
              <p class="desc">Nhận ưu đãi lên đến 15.000.000đ khi mang thiết bị cũ của bạn đến Peach Store.</p>
              <a href="#" class="apple-link text-lg">Xem giá thu cũ ></a>
            </div>
            <div class="banner-visual">
              <img src="../assets/images/banners/mac_and_iphone.svg" alt="Trade In" />
            </div>
          </div>
        </section>

        <!-- TRUST -->
        <section class="trust-section">
          <div class="trust-inner">
            <h2 class="trust-title">Tại sao chọn Peach Store?</h2>
            <div class="trust-grid">
              <div class="trust-item">
                <div class="icon-wrap">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>
                </div>
                <h3>100% Chính hãng</h3>
                <p>Cam kết hàng chính hãng, đầy đủ hóa đơn VAT.</p>
              </div>
              <div class="trust-item">
                <div class="icon-wrap">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="3" width="15" height="13" /><polygon points="16 8 20 8 23 11 23 16 16 16 16 8" /><circle cx="5.5" cy="18.5" r="2.5" /><circle cx="18.5" cy="18.5" r="2.5" /></svg>
                </div>
                <h3>Giao hàng nhanh</h3>
                <p>Giao nhanh trong ngày tại Hà Nội & TP.HCM.</p>
              </div>
              <div class="trust-item">
                <div class="icon-wrap">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg>
                </div>
                <h3>Bảo hành 12 tháng</h3>
                <p>Chính sách bảo hành chính hãng từ Apple Việt Nam.</p>
              </div>
              <div class="trust-item">
                <div class="icon-wrap">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 1 1-7.6-10.6 8.38 8.38 0 0 1 3.9.9l3.1-3.1" /><path d="M16 3h5v5" /></svg>
                </div>
                <h3>Hỗ trợ 24/7</h3>
                <p>Đội ngũ chuyên gia luôn sẵn sàng giải đáp thắc mắc.</p>
              </div>
            </div>
          </div>
        </section>

        <!-- NEWSLETTER -->
        <section class="newsletter-section">
          <div class="newsletter-inner">
            <h2 class="news-title">Nhận tin mới nhất.</h2>
            <div class="news-form-container">
              <Transition name="fade" mode="out-in">
                <div v-if="subscribed" class="news-success-card" key="success">
                  <div class="success-icon-wrap">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  </div>
                  <h3 class="success-title">Đăng ký bản tin thành công!</h3>
                  <p class="success-desc">Cảm ơn bạn. Chúng tôi sẽ gửi những thông tin ưu đãi mới nhất của Peach Store tới <strong>{{ emailInput }}</strong>.</p>
                  <button class="reset-sub-btn" @click="resetSubscription">Đăng ký bằng email khác</button>
                </div>
                <div v-else class="news-form" key="form">
                  <div class="news-input-wrapper">
                    <input 
                      type="email" 
                      v-model="emailInput" 
                      maxlength="100"
                      placeholder="Địa chỉ email của bạn" 
                      :class="['news-input', { 'has-error': hasError }]" 
                      @keyup.enter="handleSubscribe"
                    />
                    <span v-if="hasError" class="error-text">{{ errorMessage }}</span>
                  </div>
                  <AppleButton variant="primary" class="news-btn" @click="handleSubscribe">Đăng ký</AppleButton>
                </div>
              </Transition>
            </div>
          </div>
        </section>
      </main>
    </div>
  </template>

  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import AppleButton from '../components/AppleButton.vue';

  const router = useRouter();
  const emailInput = ref('');
  const subscribed = ref(false);
  const hasError = ref(false);
  const errorMessage = ref('');

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleSubscribe = () => {
    hasError.value = false;
    const trimmedEmail = emailInput.value.trim();
    if (!trimmedEmail) {
      hasError.value = true;
      errorMessage.value = 'Vui lòng nhập email của bạn.';
      return;
    }
    if (trimmedEmail.length > 100) {
      hasError.value = true;
      errorMessage.value = 'Địa chỉ email tối đa 100 ký tự.';
      return;
    }
    if (!validateEmail(trimmedEmail)) {
      hasError.value = true;
      errorMessage.value = 'Địa chỉ email không hợp lệ. Vui lòng nhập lại.';
      return;
    }
    subscribed.value = true;
  };

  const resetSubscription = () => {
    subscribed.value = false;
    emailInput.value = '';
    hasError.value = false;
  };

  onMounted(() => {
    // Other initialization if needed
  });
  </script>

  <style scoped>
  .trang-chu {
    background-color: white;
  }

  /* CONTENT REVEAL ANIMATION */
  .content-reveal {
    animation: fadeIn 1.2s cubic-bezier(0.22, 1, 0.36, 1);
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* HERO */
  .hero-cinematic {
    position: relative;
    background-color: #000;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    text-align: center;
  }

  .hero-text-overlay {
    padding-top: 80px;
    z-index: 10;
    color: white;
  }

  .hero-title {
    font-size: 56px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .hero-subtitle {
    font-size: 24px;
    margin-bottom: 24px;
  }

  .hero-actions {
    display: flex;
    gap: 24px;
    justify-content: center;
    align-items: center;
  }

  .hero-image-wrap {
    position: absolute;
    bottom: 0;
    width: 100%;
    max-width: 1400px;
    -webkit-mask-image: linear-gradient(to top, transparent 0%, black 10%);
    mask-image: linear-gradient(to top, transparent 0%, black 25%);
  }

  .hero-img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }

  /* FEATURE */
  .cinematic-feature {
    padding: 100px 20px;
    background-color: #000;
    color: white;
    display: flex;
    justify-content: center;
  }

  .feature-container {
    max-width: 1200px;
    display: flex;
    align-items: center;
    gap: 60px;
  }

  .feature-video {
    flex: 1;
  }

  .feature-video video {
    width: 100%;
    border-radius: 20px;
  }

  .feature-text {
    flex: 1;
  }

  .feature-text h2 {
    font-size: 48px;
    font-weight: 600;
    margin-bottom: 20px;
  }

  .feature-text p {
    font-size: 21px;
    color: #86868b;
    line-height: 1.4;
  }

  /* LINEUP */
  .lineup-section {
    padding-top: 80px;
    background-color: #f5f5f7;
    background-image: url("../assets/images/products/hero_iphone_family.jpg");
    background-size: cover; 
    background-position: center 85%; 
    background-repeat: no-repeat;
    text-align: center;
    min-height: 730px;
    transition: all 0.8s ease;
  }

  @media (min-width: 1440px) {
    .lineup-section {
      min-height: 740px; 
      background-position: center 95%;
      padding-top: 60px; 
    }
  }

  .lineup-content {
    max-width: 1000px;
    margin: 0 auto;
    position: relative;
    z-index: 2;
  }

  .section-title {
    font-size: 52px;
    font-weight: 700; 
    margin-bottom: 12px;
    color: #1d1d1f;
    letter-spacing: -0.01em;
  }

  .section-subtitle {
    font-size: 19px; 
    color: #1d1d1f;
    margin-bottom: 28px;
    font-weight: 400;
  }

  .lineup-actions {
    display: flex;
    gap: 18px;
    justify-content: center;
    margin-bottom: 60px;
  }

  .pill-btn {
    border-radius: 980px !important;
    padding: 12px 26px !important;
    font-size: 17px !important;
    min-width: auto !important;
    transition: all 0.3s ease;
  }

  .pill-btn.primary {
    background-color: #0071e3 !important;
    color: #ffffff !important;
    font-weight: 500;
  }

  .pill-btn.secondary {
    background-color: transparent !important;
    border: 1.5px solid #0071e3 !important;
    color: #0071e3 !important;
    font-weight: 500;
  }

  .pill-btn:hover {
    opacity: 0.8;
  }

  .promo-grid {
    padding: 12px;
    background-color: #ffffff;
  }

  .grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .promo-card {
    height: 450px;
    padding: 40px 20px 0;
    text-align: center;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: radial-gradient(circle at center, #ffffff 0%, #f2f7ff 100%);
    border-radius: 28px;
  }

  .promo-header {
    margin-bottom: 0;
    z-index: 10;
  }

  .promo-title {
    font-size: 40px;
    font-weight: 600;
    margin-bottom: 4px;
    color: #1d1d1f;
    text-align: center;
  }

  .air-text {
    font-family: 'Caveat', cursive;
    font-size: 42px;
    font-weight: 400;
    color: #2997ff;
    margin-left: 2px;
    display: inline-block;
    transform: translateY(3px) rotate(-2deg);
    letter-spacing: -0.02em;
  }

  .pro-text {
    background: linear-gradient(90deg, #bf5af2, #ff2d55);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    display: inline-block;
    margin-left: 4px;
  }

  .watch-title {
    font-size: 28px; 
    letter-spacing: normal;
  }

  .series-text {
    font-family: 'Caveat', cursive;
    font-size: 34px; 
    font-weight: 548;
    color: #2997ff;
    margin-left: 6px;
    display: inline-block;
    transform: translateY(2px) rotate(-2deg);
    letter-spacing: -0.01em;
  }

  .apple-logo {
    display: inline-block;
    vertical-align: -2px; 
    margin-right: 4px;
  }

  .promo-subtitle {
    font-size: 17px;
    color: #86868b;
    margin-bottom: 12px;
    font-weight: 400;
  }

  .promo-actions {
    display: flex;
    gap: 8px;
    justify-content: center;
    z-index: 5;
  }

  .grid-btn {
    padding: 12px 26px !important;
    font-size: 17px !important;
    font-weight: 500 !important;
  }

  .promo-img {
    width: 115%;
    flex: 1;
    margin-top: -65px;
    object-fit: contain;
    object-position: top;
    transition: transform 0.5s ease;
    mix-blend-mode: multiply; 
    pointer-events: none;
  }

  @media (hover: hover) and (min-width: 1024px) {
    .promo-card:hover .promo-img {
      transform: scale(1.05);
    }
  }

  /* TRADE IN */
  .trade-in-banner {
    padding: 100px 20px;
    background-color: #ffffff;
  }

  .banner-inner {
    max-width: 1000px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 40px;
  }

  .banner-text {
    flex: 1;
  }

  .banner-text .title {
    font-size: 48px;
    font-weight: 600;
    margin: 12px 0;
  }

  .banner-text .desc {
    font-size: 19px;
    color: #424245;
    margin-bottom: 20px;
  }

  .banner-visual img {
    width: 100%;
    max-width: 400px;
  }

  /* TRUST */
  .trust-section {
    padding: 100px 20px;
    background-color: #f5f5f7;
    text-align: center;
  }

  .trust-title {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 60px;
  }

  .trust-grid {
    max-width: 1100px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 40px;
  }

  .icon-wrap {
    width: 40px;
    height: 40px;
    margin: 0 auto 20px;
    color: #1d1d1f;
  }

  .trust-item h3 {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .trust-item p {
    font-size: 14px;
    color: #86868b;
    line-height: 1.5;
  }

  /* NEWSLETTER */
  .newsletter-section {
    padding: 100px 20px;
    text-align: center;
  }

  .news-title {
    font-size: 40px;
    font-weight: 600;
    margin-bottom: 30px;
  }

  .news-form {
    display: flex;
    justify-content: center;
    gap: 12px;
    max-width: 500px;
    margin: 0 auto;
  }

  .news-input {
    flex: 1;
    padding: 12px 20px;
    border-radius: 12px;
    border: 1px solid #d2d2d7;
    font-size: 17px;
    outline: none;
  }

  .news-input:focus {
    border-color: #0071e3;
  }

  .news-btn {
    white-space: nowrap !important;
    flex-shrink: 0 !important;
  }

  .apple-link {
    color: #2997ff;
    text-decoration: none;
    font-size: 17px;
    display: inline-flex;
    align-items: center;
    transition: opacity 0.2s;
  }

  .apple-link:hover {
    opacity: 1;
    text-decoration: underline;
  }
  /* RESPONSIVE */
  @media (min-width: 768px) and (max-width: 1068px) {
    .hero-image-wrap {
      width: 140%; 
      transform: translateY(5%);
    }
    .hero-title { font-size: 88px; }
    .feature-text h2 { font-size: 40px; }
    .section-title { font-size: 44px; }
    .promo-title { font-size: 32px; }
    .promo-card { height: 500px; }
    .promo-img { width: 140%; margin-top: -20px; }
    .trust-grid { grid-template-columns: repeat(2, 1fr); }
  }

  @media (max-width: 767px) {
    .hero-cinematic { height: auto; min-height: 80vh; }
    .hero-text-overlay { padding-top: 60px; }
    .hero-title { font-size: 40px; }
    .hero-subtitle { font-size: 19px; }
    
    .feature-container { flex-direction: column; text-align: center; gap: 40px; }
    .feature-text h2 { font-size: 32px; }
    .feature-text p { font-size: 17px; }

    .lineup-section { 
      min-height: 400px; 
      padding-top: 40px; 
      background-size: 340%; 
      background-position: center bottom;
    }
    .section-title { font-size: 36px; }
    .section-subtitle { font-size: 17px; margin-bottom: 20px; }
    .lineup-actions { margin-bottom: 30px; }
    
    .grid-container { grid-template-columns: 1fr; gap: 12px; }
    .promo-card { 
      height: 480px; 
      padding: 40px 20px; 
    }
    .promo-img {
      width: 215%;
      margin-top: 0;
      object-position: center bottom;
      transform: translateY(-22%);
    }
    .promo-title { font-size: 52px; }
    .promo-subtitle { font-size: 17px; }
    
    .banner-inner { flex-direction: column; text-align: center; }
    .banner-text .title { font-size: 32px; }
    
    .trust-grid { grid-template-columns: 1fr; gap: 40px; }
    
    .news-form { flex-direction: column; width: 100%; padding: 0 20px; }
    .news-btn { width: 100%; }

    .hero-actions { flex-direction: column; gap: 12px; }
    .promo-actions { flex-wrap: wrap; }

    .hero-image-wrap {
      bottom: 10%; 
      transform: translateY(-20px) scale(1.50);
    }

    .cinematic-feature {
      margin-top: -5%;
      padding-top: 60px; 
    }
  }


  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @media (max-width: 480px) {
    .hero-title { font-size: 42px; }
    .section-title { font-size: 28px; }
    .promo-title { font-size: 28px; }
    .air-text { font-size: 32px; }
    .series-text { font-size: 24px; }
    .watch-title { font-size: 24px; }
  }

  @media (min-width: 768px) and (max-width: 1199px) {
    .hero-cinematic { height: 85vh; }
    .hero-title { font-size: 52px; }
    .hero-subtitle { font-size: 24px; }
    
    .lineup-section {
      min-height: 550px;
      padding-top: 80px;
      background-size: 220%; 
      background-position: center bottom;
    }
    .section-title { font-size: 48px; }
    
    .grid-container {
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      padding: 0 20px;
    }
    
    .promo-card {
      height: 500px;
      padding: 40px 30px;
    }
    
    .promo-img {
      width: 175%; 
      margin-top: -80px;
      object-position: top;
    }

    .promo-title { font-size: 36px; }
    
  }

  @media (min-width: 1200px) {

    .grid-container {
      grid-template-columns: repeat(2, 1fr);
      gap: 32px;
      padding: 40px;
      max-width: 1800px;
      margin: 0 auto;
    }

    .promo-card {
      height: 500px; 
      border-radius: 32px;
      transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }


    .promo-img {
      width: 125%;
      margin-top: -150px;
    }

    .promo-title {
      font-size: 48px; 
    }

    .promo-subtitle {
      font-size: 19px;
      max-width: 85%;
      margin: 0 auto 20px;
    }

    .section-title {
      font-size: 64px;
      letter-spacing: -0.02em;
    }


  }

  /* Enhancements for Ultrawide monitors */
  @media (min-width: 2000px) {

    .grid-container {
      gap: 60px;
      max-width: 2200px;
    }

    .promo-card {
      height: 750px; /* Reduced from 850px */
    }

    .watch-title, .series-text {
      font-size: 38px; /* Reduced to match new promo-title scale */
    }

    .section-title {
      font-size: 88px;
    }
    
  }

  @media (max-width: 540px) {
    .section-title {
      font-size: 32px;
    }
    .section-subtitle {
      font-size: 15px;
      padding: 0 20px;
    }
    .lineup-section {
      padding-top: 70px;
      min-height: 420px;
      background-size: 250%;
    }
    .promo-title {
      font-size: 38px !important;
    }
    .air-text {
      font-size: 28px !important;
    }
    .promo-card {
      height: 520px;
      padding-top: 40px;
    }
    .promo-img {
      width: 155%;
      margin-top: 10px;
      transform: translateY(0);
      flex: none; /* Prevent flex from stretching it weirdly */
      height: auto;
    }
    .grid-container {
      gap: 10px;
      padding: 10px;
    }
  }

  @media (min-width: 541px) and (max-width: 570px) {
    .section-title {
      font-size: 36px;
    }
    .lineup-section {
      padding-top: 80px;
      min-height: 480px;
      background-size: 270%;
    }
    .promo-card {
      height: 560px;
      padding-top: 50px;
    }
    .promo-img {
      width: 160%;
      margin-top: 15px;
      flex: none;
      height: auto;
    }
    .promo-title {
      font-size: 42px !important;
    }
    .grid-container {
      gap: 12px;
      padding: 12px;
    }
  }

  @media (min-width: 571px) and (max-width: 750px) {
    .section-title {
      font-size: 40px;
    }
    .lineup-section {
      padding-top: 100px;
      min-height: 520px;
      background-size: 280%;
    }
    .promo-card {
      height: 650px;
      padding-top: 60px;
    }
    .promo-img {
      width: 140%;
      margin-top: 30px;
      flex: none;
      height: auto;
      transform: none;
    }
    .promo-title {
      font-size: 52px !important;
    }
    .grid-container {
      gap: 15px;
      padding: 15px;
    }
  }

  @media (min-width: 751px) and (max-width: 900px) {
    .promo-card {
      height: 680px;
      padding-top: 50px;
    }
    .promo-img {
      width: 220%;
      margin-top: 20px;
      flex: none;
      height: auto;
      transform: none;
    }
    .promo-title {
      font-size: 44px !important;
    }
    .promo-actions {
      gap: 10px;
    }
    .pill-btn {
      padding: 10px 20px !important;
      font-size: 15px !important;
      white-space: nowrap;
    }
    .grid-container {
      gap: 20px;
      padding: 20px;
    }
  }

  @media (min-width: 901px) and (max-width: 1280px) {
    .section-title {
      font-size: 52px;
    }
    .lineup-section {
      padding-top: 100px;
      min-height: 700px;
      background-size: 180%;
      background-position: center 95%;
    }
    .promo-card {
      height: 680px;
      padding-top: 60px;
    }
    .promo-img {
      width: 200%;
      margin-top: -25px;
      flex: none;
      height: auto;
    }
    .promo-title {
      font-size: 52px !important;
    }
    .grid-container {
      gap: 24px;
      padding: 24px;
    }
  }

  @media (min-width: 1281px) and (max-width: 1600px) {
    .promo-card {
      height: 680px;
      padding-top: 80px;
    }
    .promo-img {
      width: 160%;
      margin-top: -120px;
      flex: none;
      height: auto;
    }
    .promo-title {
      font-size: 58px !important;
    }
    .grid-container {
      gap: 32px;
      padding: 32px;
    }
  }

  /* --- PREMIUM NEWSLETTER STYLES --- */
  .news-form-container {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }

  .news-input-wrapper {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 6px;
    text-align: left;
  }

  .news-input.has-error {
    border-color: #ff3b30 !important;
    box-shadow: 0 0 0 3px rgba(255, 59, 48, 0.15) !important;
    animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
  }

  .error-text {
    font-size: 13px;
    color: #ff3b30;
    padding-left: 8px;
    font-family: 'Outfit', sans-serif;
  }

  @keyframes shake {
    10%, 90% { transform: translate3d(-1px, 0, 0); }
    20%, 80% { transform: translate3d(2px, 0, 0); }
    30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
    40%, 60% { transform: translate3d(4px, 0, 0); }
  }

  .news-success-card {
    background: rgba(0, 113, 227, 0.05); /* Frosty light blue glass */
    border: 1px solid rgba(0, 113, 227, 0.15);
    border-radius: 20px;
    padding: 30px;
    max-width: 500px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    animation: newsletterFadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }

  @keyframes newsletterFadeInUp {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .success-icon-wrap {
    width: 48px;
    height: 48px;
    background: #0071e3;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
    margin: 0 auto;
  }

  .success-title {
    font-size: 20px;
    font-weight: 600;
    color: #1d1d1f;
    margin: 0;
    font-family: 'Outfit', sans-serif;
  }

  .success-desc {
    font-size: 15px;
    color: #515154;
    line-height: 1.5;
    margin: 0;
    font-family: 'Outfit', sans-serif;
  }

  .reset-sub-btn {
    background: none;
    border: none;
    color: #0071e3;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    text-decoration: underline;
    font-family: 'Outfit', sans-serif;
    transition: opacity 0.2s;
    margin-top: 8px;
  }

  .reset-sub-btn:hover {
    opacity: 0.8;
  }
  </style>
