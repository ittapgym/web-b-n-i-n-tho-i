<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="header">
        <h1 class="title">Peach Store</h1>
        <p class="subtitle">Đăng nhập bằng tài khoản của bạn</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
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
          placeholder="••••••••"
          v-model="form.password"
          :error="errors.password"
        />

        <div class="actions">
          <AppleButton :loading="loading" class="submit-btn">
            Đăng nhập
          </AppleButton>
        </div>
      </form>

      <div class="footer">
        <p>Chưa có tài khoản? <router-link to="/dang-ky">Tạo ngay bây giờ</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import AppleInput from '../components/AppleInput.vue';
import AppleButton from '../components/AppleButton.vue';
import { xacThucApi } from '../services/api';
import { useNotificationStore } from '../stores/notification';
import { useRouter } from 'vue-router';

const router = useRouter();
const notification = useNotificationStore();

const form = reactive({
  email: '',
  password: ''
});

const errors = reactive({
  email: '',
  password: ''
});

const loading = ref(false);

onMounted(() => {
  const redirectPath = localStorage.getItem('redirect_after_login');
  if (redirectPath) {
    notification.show("Vui lòng đăng nhập để tiếp tục mua hàng", "info");
  }
});

const handleLogin = async () => {
  // Reset errors
  errors.email = '';
  errors.password = '';
  
  if (form.email && form.email.length > 50) {
    errors.email = 'Email không được vượt quá 50 ký tự';
    return;
  }
  
  loading.value = true;
  try {
    const res = await xacThucApi.dangNhap({
      email: form.email,
      mat_khau: form.password
    });
    
    // Luu token vao LocalStorage
    localStorage.setItem('token', res.data.access_token);
    notification.show("Đăng nhập thành công! Chào mừng bạn quay lại.", "success");
    
    // Kiểm tra xem có redirect path không (từ Guest Mode)
    const redirectPath = localStorage.getItem('redirect_after_login');
    localStorage.removeItem('redirect_after_login');
    
    // Chuyen huong ve trang truoc do hoặc Trang Chu
    setTimeout(() => {
      if (redirectPath) {
        router.push(redirectPath);
      } else {
        router.push('/');
      }
    }, 1000);
    
  } catch (error) {
    console.error("Loi dang nhap:", error);
    if (error.response && error.response.status === 401) {
      notification.show("Email hoặc mật khẩu không chính xác", "error");
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
