<template>
  <transition name="toast">
    <div v-if="store.visible" :class="['apple-toast', store.type]">
      <div class="toast-content">
        <span class="icon">{{ icon }}</span>
        <span class="message">{{ store.message }}</span>
      </div>
      <button class="close-btn" @click="store.hide">×</button>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue';
import { useNotificationStore } from '../stores/notification';

const store = useNotificationStore();

const icon = computed(() => {
  switch (store.type) {
    case 'success': return '✓';
    case 'error': return '✕';
    case 'info': return 'ℹ';
    default: return '•';
  }
});
</script>

<style scoped>
.apple-toast {
  position: fixed;
  top: 40px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  min-width: 320px;
  max-width: 90%;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  padding: 14px 20px;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 14px;
  font-weight: bold;
}

.success .icon { background: #34c759; color: white; }
.error .icon { background: #ff3b30; color: white; }
.info .icon { background: #0071e3; color: white; }

.message {
  font-family: var(--font-primary);
  font-size: var(--font-size-md);
  color: var(--color-text-primary);
  font-weight: 500;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 0 4px;
}

/* Transitions */
.toast-enter-active, .toast-leave-active {
  transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translate(-50%, -100%);
}
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px);
}
</style>
