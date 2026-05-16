import axios from 'axios'

// In dev, Vite proxy handles /api → http://localhost:5000
const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true  // REQUIRED: Flask-Login uses session cookies
})

api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      const { useAuthStore } = await import('@/stores/auth')
      const auth = useAuthStore()
      auth.logout()  // скидає стор
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// No JWT interceptors needed — Flask-Login handles auth via cookies.
// If the server returns 401, the router guard will redirect to /login.

export default api
