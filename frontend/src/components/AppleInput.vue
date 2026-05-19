<template>
  <div class="apple-input-container">
    <label v-if="label" :for="id" class="apple-label">{{ label }}</label>
    <div class="input-wrapper">
      <input
        :id="id"
        :type="type"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :class="['apple-input', { 'has-error': error }]"
        v-bind="$attrs"
      />
      <p v-if="error" class="error-message">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  id: String,
  label: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  modelValue: [String, Number],
  error: String
});
defineEmits(['update:modelValue']);
</script>

<style scoped>
.apple-input-container {
  margin-bottom: var(--space-8);
  width: 100%;
}

.apple-label {
  display: block;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
  font-weight: 500;
}

.input-wrapper {
  position: relative;
}

.apple-input {
  width: 100%;
  padding: 14px 16px;
  font-family: var(--font-primary);
  font-size: var(--font-size-md);
  border: 1px solid var(--color-surface-strong);
  border-radius: var(--radius-md);
  background-color: white;
  transition: all var(--motion-fast) ease;
  outline: none;
}

.apple-input:focus {
  border-color: var(--color-surface-muted);
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

.apple-input.has-error {
  border-color: #ff3b30;
}

.error-message {
  font-size: var(--font-size-xs);
  color: #ff3b30;
  margin-top: 4px;
}
</style>
