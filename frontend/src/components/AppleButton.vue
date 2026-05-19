<template>
  <button
    :class="['apple-button', variant, { 'is-loading': loading }]"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <span v-if="loading" class="spinner"></span>
    <slot v-else></slot>
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary' // primary, secondary, ghost
  },
  disabled: Boolean,
  loading: Boolean
});
</script>

<style scoped>
.apple-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  font-family: var(--font-primary);
  font-size: var(--font-size-md);
  font-weight: 500;
  border-radius: var(--radius-sm); /* Pill shape */
  border: none;
  cursor: pointer;
  transition: all var(--motion-fast) ease;
  min-width: 100px;
  position: relative;
  outline: none;
}

/* Primary Variant */
.apple-button.primary {
  background-color: var(--color-surface-muted);
  color: white;
}

.apple-button.primary:hover {
  background-color: #0077ed;
}

.apple-button.primary:active {
  background-color: #0062c3;
  transform: scale(0.98);
}

/* Secondary Variant */
.apple-button.secondary {
  background-color: var(--color-surface-strong);
  color: var(--color-text-primary);
}

/* States */
.apple-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

.apple-button:focus-visible {
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.3);
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
