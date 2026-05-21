<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '@/api'

const router = useRouter()

// step: 'email' → 'code' → 'newPassword'
const step = ref('email')

const email = ref('')
const code = ref(['', '', '', '', '', ''])
const newPassword = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const errorMsg = ref('')
const isLoading = ref(false)

const resendTimer = ref(30)
const canResend = ref(false)
let timerInterval = null

const startTimer = () => {
  resendTimer.value = 30
  canResend.value = false
  timerInterval = setInterval(() => {
    resendTimer.value--
    if (resendTimer.value <= 0) {
      clearInterval(timerInterval)
      canResend.value = true
    }
  }, 1000)
}

// Step 1: відправити код на email
const handleSendCode = async () => {
  if (!email.value) {
    errorMsg.value = 'Enter your email address'
    return
  }
  errorMsg.value = ''
  isLoading.value = true
  try {
    await userApi.sendPasswordResetCode(email.value)
    step.value = 'code'
    startTimer()
  } catch (e) {
    errorMsg.value = e.response?.data?.error ?? 'Failed to send code. Check your email.'
  } finally {
    isLoading.value = false
  }
}

const handleResend = async () => {
  if (!canResend.value) return
  isLoading.value = true
  errorMsg.value = ''
  try {
    await userApi.sendPasswordResetCode(email.value)
    startTimer()
  } catch (e) {
    errorMsg.value = e.response?.data?.error ?? 'Failed to resend code'
  } finally {
    isLoading.value = false
  }
}

// Обробники квадратиків
const handleCodeInput = (index, event) => {
  const value = event.target.value.replace(/\D/g, '')
  code.value[index] = value.slice(-1)
  if (value && index < 5) {
    document.getElementById(`reset-code-${index + 1}`)?.focus()
  }
}

const handleKeyDown = (index, event) => {
  if (event.key === 'Backspace' && !code.value[index] && index > 0) {
    document.getElementById(`reset-code-${index - 1}`)?.focus()
  }
}

const handlePaste = (event) => {
  event.preventDefault()
  const pasted = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6)
  pasted.split('').forEach((char, i) => { code.value[i] = char })
  const lastIdx = Math.min(pasted.length, 5)
  document.getElementById(`reset-code-${lastIdx}`)?.focus()
}

// Step 2: підтвердити код
const handleVerifyCode = async () => {
  const fullCode = code.value.join('')
  if (fullCode.length < 6) {
    errorMsg.value = 'Enter all 6 digits'
    return
  }
  errorMsg.value = ''
  isLoading.value = true
  try {
    await userApi.verifyPasswordResetCode(email.value, fullCode)
    step.value = 'newPassword'
  } catch (e) {
    errorMsg.value = e.response?.data?.error ?? 'Invalid code'
  } finally {
    isLoading.value = false
  }
}

// Step 3: встановити новий пароль
const handleResetPassword = async () => {
  if (!newPassword.value) {
    errorMsg.value = 'Enter new password'
    return
  }
  if (newPassword.value.length < 8) {
    errorMsg.value = 'Password must be at least 8 characters'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match'
    return
  }
  errorMsg.value = ''
  isLoading.value = true
  try {
    const fullCode = code.value.join('')
    await userApi.resetPassword(email.value, fullCode, newPassword.value)
    router.push('/login')
  } catch (e) {
    errorMsg.value = e.response?.data?.error ?? 'Failed to reset password'
  } finally {
    isLoading.value = false
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

      <!-- Step 1: Введи email -->
      <template v-if="step === 'email'">
        <h1 class="title">Forgot password?</h1>
        <p class="subtitle">Enter your email and we'll send you a reset code.</p>

        <form class="auth-form" @submit.prevent="handleSendCode">
          <div class="input-group">
            <label>Email <span class="required">*</span></label>
            <input
              type="email"
              v-model="email"
              class="input-base"
              placeholder="example@mail.com"
            />
          </div>

          <p v-if="errorMsg" class="error-banner">{{ errorMsg }}</p>

          <div class="actions">
            <button class="btn btn-primary action-btn" :disabled="isLoading">
              {{ isLoading ? 'Sending...' : 'Send code' }}
            </button>
          </div>

          <p class="switch-auth">
            <router-link to="/login" class="back-link">← Back to Log in</router-link>
          </p>
        </form>
      </template>

      <!-- Step 2: Введи код -->
      <template v-else-if="step === 'code'">
        <h1 class="title">Enter verification code</h1>
        <p class="subtitle">We sent a 6-digit code to <strong>{{ email }}</strong></p>

        <form class="auth-form" @submit.prevent="handleVerifyCode">
          <div class="input-group">
            <label>Verification Code <span class="required">*</span></label>
            <div class="code-inputs">
              <input
                v-for="(digit, idx) in code"
                :key="idx"
                :id="'reset-code-' + idx"
                type="text"
                inputmode="numeric"
                maxlength="1"
                v-model="code[idx]"
                @input="handleCodeInput(idx, $event)"
                @keydown="handleKeyDown(idx, $event)"
                @paste="handlePaste"
                class="digit-box"
              />
            </div>
          </div>

          <p v-if="errorMsg" class="error-banner">{{ errorMsg }}</p>

          <span
            class="resend-link"
            :class="{ 'resend-active': canResend }"
            @click="handleResend"
          >
            {{ canResend ? 'Resend code' : `Resend code in ${resendTimer}s` }}
          </span>

          <div class="actions">
            <button class="btn btn-primary action-btn" :disabled="isLoading">
              {{ isLoading ? 'Verifying...' : 'Verify' }}
            </button>
          </div>
        </form>
      </template>

      <!-- Step 3: Новий пароль -->
      <template v-else>
        <h1 class="title">Set new password</h1>
        <p class="subtitle">Create a strong new password for your account.</p>

        <form class="auth-form" @submit.prevent="handleResetPassword">
          <div class="input-group">
            <label>New Password <span class="required">*</span></label>
            <div class="password-wrapper">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="newPassword"
                class="input-base"
                placeholder="••••••••"
              />
              <span class="eye-icon" @mousedown.prevent="showPassword = !showPassword">
                {{ showPassword ? '🙈' : '👁️' }}
              </span>
            </div>
            <p class="hint-msg">At least 8 characters, 1 uppercase letter and 1 special character</p>
          </div>

          <div class="input-group">
            <label>Confirm Password <span class="required">*</span></label>
            <div class="password-wrapper">
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                v-model="confirmPassword"
                class="input-base"
                placeholder="••••••••"
              />
              <span class="eye-icon" @mousedown.prevent="showConfirmPassword = !showConfirmPassword">
                {{ showConfirmPassword ? '🙈' : '👁️' }}
              </span>
            </div>
          </div>

          <p v-if="errorMsg" class="error-banner">{{ errorMsg }}</p>

          <div class="actions">
            <button class="btn btn-primary action-btn" :disabled="isLoading">
              {{ isLoading ? 'Saving...' : 'Save new password' }}
            </button>
          </div>
        </form>
      </template>

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
.auth-logo:hover { transform: scale(1.02); }
.auth-logo:hover .mascot-placeholder { transform: rotate(0deg) scale(1.08); }
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
  margin-bottom: 0.75rem;
}
.subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  color: var(--color-text-light);
  margin-bottom: 1.5rem;
  line-height: 1.5;
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
.required { color: var(--color-error); }
.password-wrapper { position: relative; }
.eye-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  opacity: 0.6;
  user-select: none;
}
.eye-icon:hover { opacity: 1; }
.hint-msg {
  color: var(--color-text-light);
  font-size: 0.75rem;
  margin-top: 0.5rem;
}
.code-inputs {
  display: flex;
  gap: 0.8rem;
  justify-content: center;
  margin-top: 0.5rem;
}
.digit-box {
  width: 50px;
  height: 50px;
  text-align: center;
  font-size: 1.5rem;
  font-family: 'Inter', sans-serif;
  border: 1px solid #CCCCCC;
  border-radius: 8px;
  outline: none;
}
.digit-box:focus {
  border-color: var(--color-primary);
}
.resend-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  color: var(--color-text-light);
  text-align: center;
}
.resend-active {
  color: var(--color-primary);
  cursor: pointer;
  text-decoration: underline;
}
.error-banner {
  color: var(--color-error);
  background-color: rgba(255, 0, 0, 0.07);
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  text-align: center;
}
.actions { display: flex; justify-content: center; }
.action-btn {
  width: 100%;
  max-width: 300px;
  padding: 0.75rem;
}
.switch-auth { text-align: center; }
.back-link {
  color: var(--color-text-light);
  font-size: 0.9rem;
  text-decoration: none;
}
.back-link:hover {
  text-decoration: underline;
  color: var(--color-primary);
}
</style>