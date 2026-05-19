const INACTIVITY_TIMEOUT = 15 * 60 * 1000 // 15 phút
let inactivityTimer = null

const EVENTS = ['mousedown', 'keydown', 'mousemove', 'touchstart', 'scroll', 'click']

export function startInactivityMonitor() {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  if (!token) return

  stopInactivityMonitor()

  const logout = async () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('token')
    
    try {
      const { useNotificationStore } = await import('../stores/notification')
      const notification = useNotificationStore()
      if (notification && notification.show) {
        notification.show('Phiên đăng nhập đã hết hạn do không hoạt động. Vui lòng đăng nhập lại.', 'error')
      }
    } catch (e) {
      // fallback
    }
    
    setTimeout(() => {
      window.location.href = '/login'
    }, 1500)
  }

  inactivityTimer = setTimeout(logout, INACTIVITY_TIMEOUT)
}

export function stopInactivityMonitor() {
  if (inactivityTimer) {
    clearTimeout(inactivityTimer)
    inactivityTimer = null
  }
}

export function resetInactivityTimer() {
  stopInactivityMonitor()
  startInactivityMonitor()
}

export function initInactivityTracking() {
  const resetHandler = () => resetInactivityTimer()
  
  EVENTS.forEach(event => {
    window.addEventListener(event, resetHandler, { passive: true })
  })
  
  startInactivityMonitor()
  
  return () => {
    EVENTS.forEach(event => {
      window.removeEventListener(event, resetHandler)
    })
    stopInactivityMonitor()
  }
}
