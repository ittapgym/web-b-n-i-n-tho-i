<template>
  <div class="product-card" @click="goToDetail">
    <!-- Image Section -->
    <div class="product-image-wrap">
      <img :src="product.hinh_anh || '/images/default-product.png'" :alt="product.ten" class="product-img" />
    </div>

    <!-- Color Dots -->
    <div class="color-dots" v-if="colors.length > 0">
      <span 
        v-for="(color, index) in colors" 
        :key="index" 
        class="color-dot" 
        :style="{ backgroundColor: color }"
      ></span>
    </div>

    <!-- Info Section -->
    <div class="product-info">
      <span v-if="product.is_new" class="new-label">Mới</span>
      <h3 class="product-name">{{ product.ten }}</h3>
      <p class="product-desc">{{ cleanDescription }}</p>
      
      <div class="product-price">
        <span class="price-from">Giá từ {{ formatPrice(product.gia) }}</span>
        <span class="price-installment">hoặc {{ formatPrice(product.gia / 12) }}/tháng trong 12 th.</span>
      </div>

      <!-- Actions -->
      <div class="product-actions">
        <router-link :to="'/san-pham/' + product.id" class="pill-btn primary" @click.stop>Tìm hiểu thêm</router-link>
        <router-link :to="'/san-pham/' + product.id" class="buy-link" @click.stop>Mua</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const router = useRouter();

const goToDetail = () => {
  router.push('/san-pham/' + props.product.id);
};

const cleanDescription = computed(() => {
  if (!props.product.mo_ta) return '';
  return props.product.mo_ta.replace(/<!--SPECS_PAIRINGS:(.*?)-->/, '').trim();
});

const colors = computed(() => {
  if (!props.product.mau_sac) return [];
  return props.product.mau_sac.split(',').map(c => c.trim());
});

const formatPrice = (value) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
};
</script>

<style scoped>
.product-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
  max-width: 400px;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}

.product-image-wrap {
  width: 100%;
  height: 240px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.color-dots {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.color-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
  border: 1px solid rgba(0,0,0,0.05);
}

.product-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  flex-grow: 1;
}

.new-label {
  color: #bf4800;
  font-size: 12px;
  font-weight: 600;
  display: block;
  margin-bottom: 8px;
}

.product-name {
  font-size: 28px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 12px;
}

.product-desc {
  font-size: 17px;
  color: #1d1d1f;
  margin-bottom: 20px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 2.8em;
}

.product-price {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: auto;
  margin-bottom: 30px;
}

.price-from {
  font-size: 17px;
  color: #1d1d1f;
}

.price-installment {
  font-size: 12px;
  color: #1d1d1f;
}

.product-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.pill-btn {
  padding: 10px 22px;
  border-radius: 980px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.pill-btn.primary {
  background-color: #0071e3;
  color: white;
}

.pill-btn.primary:hover {
  background-color: #0077ed;
}

.buy-link {
  color: #0066cc;
  text-decoration: none;
  font-size: 17px;
  transition: opacity 0.2s;
}

.buy-link:hover {
  text-decoration: underline;
  opacity: 0.8;
}
@media (max-width: 734px) {
  .product-card { padding: 20px; }
  .product-image-wrap { height: 180px; }
  .product-name { font-size: 21px; }
  .product-desc { font-size: 14px; }
  .price-from { font-size: 14px; }
  .product-actions { gap: 15px; }
  .pill-btn { padding: 8px 16px; font-size: 12px; }
  .buy-link { font-size: 14px; }
}
</style>
