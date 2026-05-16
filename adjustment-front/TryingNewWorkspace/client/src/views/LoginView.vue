<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const errorMsg = ref('')

const handleLogin = async () => {
  errorMsg.value = ''
  const result = await auth.login(email.value, password.value)

  if (result === '2fa') {
    router.push({ name: 'two-factor-auth' })
  } else if (result === 'ok') {
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } else {
    errorMsg.value = auth.error || 'Invalid credentials'
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-box">
      <router-link to="/" class="auth-logo">
        <div class="mascot-placeholder">
          <span class="owl-icon">🎓</span>
        </div>
        <div class="logo-text">
          <span class="logo-title">STEP BY STEP</span>
          <span class="logo-subtitle">Learn with Flashcards</span>
        </div>
      </router-link>

      <h1 class="title">Log in</h1>

      <form class="auth-form" @submit.prevent="handleLogin">
        <div class="input-group">
          <label>Email / Username <span class="required">*</span></label>
          <input
            type="text"
            v-model="email"
            class="input-base"
            placeholder="example@mail.com"
          />
        </div>

        <div class="input-group">
          <label>Password <span class="required">*</span></label>
          <div class="password-wrapper">
            <input
              type="password"
              v-model="password"
              class="input-base"
              placeholder="••••••••"
            />
            <span class="eye-icon">👁️</span>
          </div>
          <div class="forgot-wrapper">
            <a href="#" class="forgot-link">Forgot password?</a>
          </div>
        </div>

        <p v-if="errorMsg" class="error-banner">{{ errorMsg }}</p>

        <div class="actions">
          <button class="btn btn-primary login-btn" :disabled="auth.loading">
            {{ auth.loading ? 'Logging in...' : 'Log in' }}
          </button>
        </div>

        <p class="switch-auth">
          Don't have an account? <router-link to="/signup">Sign up</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<style scoped>
.auth-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  text-decoration: none;
  margin-bottom: 2rem;
  transition: transform 0.2s ease;
}
.auth-logo:hover {
  transform: scale(1.02);
}
.auth-logo:hover .mascot-placeholder {
  transform: rotate(0deg) scale(1.08);
}
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
}
.auth-box {
  width: 100%;
  max-width: 480px;
  padding: 3rem 2rem;
  text-align: center;
}
.title {
  font-family: var(--font-main), 'Playfair Display', serif;
  font-size: 1.8rem;
  margin-bottom: 2rem;
}
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  text-align: left;
}
.input-group label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  font-weight: bold;
}
.required {
  color: var(--color-error);
}
.password-wrapper {
  position: relative;
}
.eye-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  opacity: 0.6;
}
.forgot-wrapper {
  text-align: left;
  margin-top: 0.5rem;
}
.forgot-link {
  color: var(--color-text-light);
  font-size: 0.8rem;
  text-decoration: none;
}
.forgot-link:hover {
  text-decoration: underline;
  color: var(--color-primary);
}
.login-btn {
  width: 100%;
  max-width: 300px;
  padding: 0.75rem;
}
.error-banner {
  color: var(--color-error);
  background-color: rgba(255, 0, 0, 0.07);
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 0.5rem;
}
.actions {
  display: flex;
  justify-content: center;
}
.switch-auth {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}
.switch-auth a {
  color: var(--color-primary);
  font-weight: bold;
  text-decoration: none;
}
.switch-auth a:hover {
  text-decoration: underline;
}
</style>