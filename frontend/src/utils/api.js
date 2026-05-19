const API_BASE = import.meta.env.VITE_API_BASE || `${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}`

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  })
  
  // Tự động bắt lỗi 401 - Token hết hạn
  if (res.status === 401) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('token')
    localStorage.setItem('redirect_after_login', window.location.pathname)
    
    const { useNotificationStore } = await import('../stores/notification')
    const notification = useNotificationStore()
    if (notification && notification.show) {
      notification.show('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.', 'error')
    }
    
    setTimeout(() => {
      window.location.href = '/login'
    }, 1500)
    
    throw new Error('Token expired')
  }
  
  return res
}
