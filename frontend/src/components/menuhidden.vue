<template>
  <Transition name="menu-slide">
    <div v-if="visible" class="menu-hidden">
      <div class="menu-content">
        <!-- Các liên kết điều hướng -->
        <router-link to="/dien-thoai" class="menu-link" @click="closeMenu">Điện thoại</router-link>
        <router-link to="/may-tinh-bang" class="menu-link" @click="closeMenu">Máy tính bảng</router-link>
        <router-link to="/laptop" class="menu-link" @click="closeMenu">Laptop</router-link>
        <router-link to="/phu-kien" class="menu-link" @click="closeMenu">Phụ kiện</router-link>
        <router-link to="/ho-tro" class="menu-link" @click="closeMenu">Hỗ trợ</router-link>

        <!-- Divider mỏng ở cuối nếu cần, hoặc giữa các mục -->
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { watch } from 'vue';

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close']);

const closeMenu = () => {
  emit('close');
};

// Khóa cuộn trang khi menu mở
watch(() => props.visible, (isVisible) => {
  if (isVisible) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});
</script>

<style scoped>
.menu-hidden {
  position: fixed;
  top: 48px; /* Khớp với chiều cao header */
  left: 0;
  width: 100%;
  height: calc(100vh - 48px);
  background-color: #ffffff;
  z-index: 9998;
  overflow-y: auto;
  display: block;
}

.menu-content {
  display: flex;
  flex-direction: column;
  padding: 0 40px; /* Padding lề trái phải rộng hơn theo screenshot */
}

.menu-link {
  color: #1d1d1f;
  font-size: 28px; /* Kích thước chữ lớn và đậm theo screenshot */
  font-weight: 600;
  text-decoration: none;
  padding: 24px 0;
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.1);
  transition: opacity 0.2s;
  width: 100%;
  text-align: left;
  letter-spacing: -0.01em;
}

.menu-link:last-child {
  border-bottom: none;
}

.menu-link:active {
  opacity: 0.7;
}

/* Transition animation: Trượt xuống từ trên */
.menu-slide-enter-active,
.menu-slide-leave-active {
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
}

.menu-slide-enter-from {
  transform: translateY(-20px);
  opacity: 0;
}

.menu-slide-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>
