import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  // ── State ───────────────────────────────────────────────────────────
  const user = ref(null)      // { id, username, email, is_verified, two_fa_enabled }
  const loading = ref(false)
  const error = ref(null)

  // After register, we store user_id to pass to verify-email step
  const pendingUserId = ref(null)
  const needsEmailVerification = ref(false)
  const needs2fa = ref(false)

  // ── Getters ─────────────────────────────────────────────────────────
  // Flask-Login uses session cookies — user is logged in if we have user data
  const isAuthenticated = computed(() => !!user.value)
  const username = computed(() => user.value?.username ?? '')

  // ── Actions ─────────────────────────────────────────────────────────

  /**
   * Login with email + password.
   * Flask may return requires_2fa: true — in that case we navigate to 2FA step.
   */
  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const { data } = await authApi.login({ email, password })
      const payload = data.data  // Flask wraps in { success, data, message }

      if (payload?.requires_2fa) {
        needs2fa.value = true
        pendingUserId.value = payload.user_id
        return '2fa'
      }

      user.value = payload
      return 'ok'
    } catch (e) {
      error.value = e.response?.data?.error ?? e.response?.data?.message ?? 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Register new user.
   * Flask sends a verification email — returns user_id for the next step.
   */
  async function register(username, email, password, confirmPassword) {
    loading.value = true
    error.value = null
    try {
      // Server requires confirm_password field
      const { data } = await authApi.register({ username, email, password, confirm_password: confirmPassword })
      pendingUserId.value = data.data?.user_id
      needsEmailVerification.value = true
      return 'verify'
    } catch (e) {
      error.value = e.response?.data?.error ?? e.response?.data?.message ?? 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  /** Submit email verification code */
  async function verifyEmail(code) {
    loading.value = true
    error.value = null
    try {
      await authApi.verifyEmail(pendingUserId.value, code)
      needsEmailVerification.value = false
      pendingUserId.value = null
      return true
    } catch (e) {
      error.value = e.response?.data?.error ?? 'Invalid code'
      return false
    } finally {
      loading.value = false
    }
  }

  /** Submit 2FA code after login */
  async function verify2fa(code) {
    loading.value = true
    error.value = null
    try {
      const { data } = await authApi.verify2fa(code)
      user.value = data.user ?? data
      needs2fa.value = false
      return true
    } catch (e) {
      error.value = e.response?.data?.error ?? 'Invalid 2FA code'
      return false
    } finally {
      loading.value = false
    }
  }

  /** Logout — clears Flask session cookie */
  async function logout() {
    try {
      await authApi.logout()
    } catch (_) { /* ignore */ }
    user.value = null
    needs2fa.value = false
    needsEmailVerification.value = false
  }

  return {
    user, loading, error,
    pendingUserId, needsEmailVerification, needs2fa,
    isAuthenticated, username,
    login, register, verifyEmail, verify2fa, logout
  }
})
