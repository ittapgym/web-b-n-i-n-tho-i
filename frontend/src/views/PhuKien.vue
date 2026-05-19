<template>
  <div class="category-page">
    <main class="main-content">
      <section class="showcase-section">
        <div class="showcase-header">
          <span class="os-label watchos">watchOS 26</span>
          <h2 class="showcase-title">
            Thông minh.
            <br />Luôn đồng hành.
          </h2>
        </div>
        <div class="showcase-visual">
          <img
            src="../assets/images/banners/hero_accessory.svg"
            alt="Watch Lineup"
            class="showcase-img"
          />
        </div>
        <div class="carousel-container">
          <div class="carousel-header">
            <h3>Tất cả Phụ kiện</h3>
            <div class="carousel-nav">
              <button class="nav-btn prev" @click="scrollLeft">
                <svg
                  viewBox="0 0 24 24"
                  width="20"
                  height="20"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M15 18l-6-6 6-6" />
                </svg>
              </button>
              <button class="nav-btn next" @click="scrollRight">
                <svg
                  viewBox="0 0 24 24"
                  width="20"
                  height="20"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M9 18l6-6-6-6" />
                </svg>
              </button>
            </div>
          </div>
          <div v-if="loading" class="loading-state">Đang tải Phụ kiện...</div>
          <div v-else-if="products.length > 0" ref="gridRef" class="product-grid">
            <ProductCard v-for="product in products" :key="product.id" :product="product" />
          </div>
          <div v-else class="empty-carousel">
            <span>Không có sản phẩm nào trong danh mục này.</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ProductCard from '../components/ProductCard.vue';

/**
 * Danh sách sản phẩm thuộc danh mục phụ kiện.
 */
const products = ref([]);

/**
 * Trạng thái tải dữ liệu sản phẩm phụ kiện.
 */
const loading = ref(true);

/**
 * Tham chiếu đến phần tử HTML lưới sản phẩm phục vụ cuộn ngang.
 */
const gridRef = ref(null);

/**
 * Thực hiện cuộn mượt lưới sản phẩm phụ kiện sang bên trái.
 */
const scrollLeft = () => {
  if (gridRef.value) {
    gridRef.value.scrollBy({ left: -350, behavior: 'smooth' });
  }
};

/**
 * Thực hiện cuộn mượt lưới sản phẩm phụ kiện sang bên phải.
 */
const scrollRight = () => {
  if (gridRef.value) {
    gridRef.value.scrollBy({ left: 350, behavior: 'smooth' });
  }
};

/**
 * Tải danh sách sản phẩm phụ kiện từ backend API.
 */
const fetchProducts = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}/san-pham/danh-muc/phu-kien`);
    if (response.ok) {
      products.value = await response.json();
    }
  } catch (error) {
    console.error("Lỗi khi tải phụ kiện:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchProducts);
</script>

<style scoped>
.category-page {
  min-height: 100vh;
  background-color: #ffffff;
}

.main-content {
  padding-top: 44px;
}

.showcase-section {
  padding: 80px 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #ffffff;
  text-align: center;
}

.product-grid {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  gap: 30px;
  padding: 20px 10px;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x mandatory;
  text-align: left;
  
  /* Hide scrollbar */
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.product-grid::-webkit-scrollbar {
  display: none;
}

.product-grid :deep(.product-card) {
  flex-shrink: 0;
  width: 320px;
  scroll-snap-align: start;
}

.loading-state {
  padding: 100px;
  font-size: 18px;
  color: #86868b;
}

.showcase-header {
  margin-bottom: 40px;
}

.os-label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  display: block;
}

.os-label.watchos {
  color: #2ecc71;
  font-size: 20px;
}

.showcase-title {
  font-size: 56px;
  font-weight: 700;
  line-height: 1.1;
  color: #1d1d1f;
  letter-spacing: -0.02em;
}

.showcase-visual {
  max-width: 1200px;
  margin: 0 auto 60px;
}

.showcase-img {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.carousel-container {
  max-width: 1200px;
  margin: 0 auto;
  text-align: left;
}

.carousel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 10px;
}

.carousel-header h3 {
  font-size: 28px;
  font-weight: 600;
}

.carousel-nav {
  display: flex;
  gap: 12px;
}

.nav-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #f5f5f7;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #1d1d1f;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background-color: #e8e8ed;
}

.empty-carousel {
  height: 300px;
  background-color: transparent;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #86868b;
  font-size: 17px;
}

@media (max-width: 768px) {
  .showcase-title {
    font-size: 40px;
  }
  .product-grid :deep(.product-card) {
    width: 280px;
  }
}
</style>
