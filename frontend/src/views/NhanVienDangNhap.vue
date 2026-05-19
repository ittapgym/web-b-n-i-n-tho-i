<template>
  <div class="staff-login-page">
    <div class="glass-login-card">
      <div class="login-header">
        <div class="logo-glow">🔐</div>
        <h2>Cổng Nhân Viên</h2>
        <p>Hệ thống Quản lý & Lịch làm việc Peach Store</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>Tên đăng nhập</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <input type="text" v-model="username" placeholder="Nhập tài khoản của bạn..." maxlength="100" required />
          </div>
        </div>

        <div class="form-group">
          <label>Mật khẩu</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <input type="password" v-model="password" placeholder="••••••••" maxlength="100" required />
          </div>
        </div>

        <div v-if="errorMsg" class="error-banner">
          ⚠️ {{ errorMsg }}
        </div>

        <button type="submit" class="login-btn" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <span v-else>Đăng nhập hệ thống</span>
        </button>
      </form>

      <div class="login-footer">
        <router-link to="/">← Quay lại trang chủ</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const password = ref('');
const errorMsg = ref('');
const loading = ref(false);

const handleLogin = async () => {
  errorMsg.value = '';
  loading.value = true;
  
  try {
    const res = await fetch('http://127.0.0.1:8000/api/admin/employee-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value.trim(),
        password: password.value
      })
    });
    
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('logged_employee', JSON.stringify(data.employee));
      localStorage.setItem('staff_token', 'mock_staff_active_session');
      
      // Show success toast if window.showToast exists
      if (window.showToast) {
        window.showToast("Đăng nhập thành công", `Chào mừng trở lại, ${data.employee.name}!`, "success");
      }
      
      // Redirect to scheduling page
      router.push('/nhan-vien/lich-lam');
    } else {
      const data = await res.json();
      errorMsg.value = data.detail || 'Sai tài khoản hoặc mật khẩu!';
    }
  } catch (e) {
    errorMsg.value = 'Không thể kết nối đến máy chủ. Vui lòng kiểm tra lại!';
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.staff-login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f5f7 0%, #e3e3e8 100%);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Rounded", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  padding: 20px;
}

.glass-login-card {
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 24px;
  width: 100%;
  max-width: 400px;
  padding: 40px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.02);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-glow {
  font-size: 44px;
  filter: drop-shadow(0 4px 10px rgba(255, 149, 0, 0.25));
  margin-bottom: 12px;
}

.login-header h2 {
  font-size: 24px;
  color: #1d1d1f;
  font-weight: 700;
  letter-spacing: -0.5px;
  margin: 0 0 8px;
}

.login-header p {
  color: #86868b;
  font-size: 13.5px;
  font-weight: 500;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #1d1d1f;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: #86868b;
}

.input-wrapper input {
  width: 100%;
  padding: 12px 16px 12px 42px;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 12px;
  color: #1d1d1f;
  font-size: 14.5px;
  font-weight: 500;
  outline: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.input-wrapper input::placeholder {
  color: #c5c5c7;
}

.input-wrapper input:focus {
  border-color: #ff9500;
  box-shadow: 0 0 0 4px rgba(255, 149, 0, 0.15);
  background: #ffffff;
}

.error-banner {
  background: rgba(255, 59, 48, 0.08);
  border: 1px solid rgba(255, 59, 48, 0.15);
  border-radius: 10px;
  color: #ff3b30;
  font-size: 13px;
  font-weight: 600;
  padding: 10px 14px;
  text-align: center;
}

.login-btn {
  background: linear-gradient(135deg, #ff9500, #ff5e3a);
  border: none;
  border-radius: 12px;
  color: #ffffff;
  cursor: pointer;
  font-size: 15px;
  font-weight: 700;
  padding: 14px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 12px rgba(255, 149, 0, 0.25);
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(255, 94, 58, 0.35);
}

.login-btn:active {
  transform: translateY(1px);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
}

.login-footer a {
  color: #007aff;
  font-size: 13.5px;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}

.login-footer a:hover {
  opacity: 0.85;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
