<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="header">
        <h1 class="title">Tạo Tài Khoản</h1>
        <p class="subtitle">Bắt đầu hành trình của bạn với Peach Store</p>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <AppleInput
          id="ho_ten"
          label="Họ và Tên"
          placeholder="Nguyễn Văn A"
          v-model="form.ho_ten"
          :error="errors.ho_ten"
        />

        <AppleInput
          id="email"
          label="Email"
          type="email"
          placeholder="email@example.com"
          v-model="form.email"
          :error="errors.email"
          maxlength="50"
        />

        <AppleInput
          id="password"
          label="Mật khẩu"
          type="password"
          placeholder="Tối thiểu 8 ký tự"
          v-model="form.mat_khau"
          :error="errors.mat_khau"
        />

        <div class="actions">
          <AppleButton :loading="loading" class="submit-btn">
            Đăng ký
          </AppleButton>
        </div>
      </form>

      <div class="footer">
        <p>Đã có tài khoản? <router-link to="/login">Đăng nhập ngay</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import AppleInput from '../components/AppleInput.vue';
import AppleButton from '../components/AppleButton.vue';
import { xacThucApi } from '../services/api';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '../stores/notification';

const router = useRouter();
const notification = useNotificationStore();

/**
 * Trạng thái biểu mẫu đăng ký tài khoản mới.
 */
const form = reactive({
  ho_ten: '',
  email: '',
  mat_khau: ''
});

/**
 * Lưu trữ thông tin lỗi của từng trường nhập liệu trong biểu mẫu.
 */
const errors = reactive({
  ho_ten: '',
  email: '',
  mat_khau: ''
});

/**
 * Trạng thái tải (loading) khi đang xử lý gửi yêu cầu đăng ký lên server.
 */
const loading = ref(false);

/**
 * Xử lý đăng ký tài khoản khách hàng mới.
 * Thực hiện kiểm tra hợp lệ độ dài email và gửi yêu cầu đăng ký lên máy chủ.
 */
const handleRegister = async () => {
  // Reset errors
  Object.keys(errors).forEach(key => errors[key] = '');
  
  if (form.email && form.email.length > 50) {
    errors.email = 'Email không được vượt quá 50 ký tự';
    return;
  }
  
  loading.value = true;
  try {
    await xacThucApi.dangKy(form);
    notification.show("Tạo tài khoản thành công! Đang chuyển hướng...", "success");
    setTimeout(() => {
      router.push('/login');
    }, 1500);
  } catch (error) {
    console.error("Loi dang ky:", error);
    if (error.response && error.response.data.detail) {
      notification.show(error.response.data.detail, "error");
    } else {
      notification.show("Không thể kết nối đến máy chủ", "error");
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f7;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 460px;
  background: white;
  padding: 48px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: var(--font-size-3xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.subtitle {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
}

.auth-form {
  margin-bottom: 32px;
}

.submit-btn {
  width: 100%;
  margin-top: 16px;
}

.footer {
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.footer a {
  font-weight: 500;
}
@media (max-width: 480px) {
  .auth-card { padding: 32px 24px; }
  .title { font-size: 28px; }
}
</style>
