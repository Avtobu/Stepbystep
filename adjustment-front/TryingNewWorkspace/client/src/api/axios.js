import axios from 'axios'

// In dev, Vite proxy handles /api → http://localhost:5000
const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true  // REQUIRED: Flask-Login uses session cookies
})


// No JWT interceptors needed — Flask-Login handles auth via cookies.
// If the server returns 401, the router guard will redirect to /login.

export default api
