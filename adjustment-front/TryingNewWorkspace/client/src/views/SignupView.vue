<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const passwordStrength = ref('')
const errorMsg = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// ✅ ЗМІНЕНО: масив з 6 цифр замість одного рядка
const code = ref(['', '', '', '', '', ''])

const checkPassword = () => {
  if (password.value.length === 0) {
    passwordStrength.value = ''
    return
  }
  if (password.value.length < 8) {
    passwordStrength.value = 'Password is too weak'
  } else {
    passwordStrength.value = ''
  }
}

const handleRegister = async () => {
  errorMsg.value = ''
  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match'
    return
  }
  if (passwordStrength.value) return

  const result = await auth.register(username.value, email.value, password.value, confirmPassword.value)
  if (!result) {
    errorMsg.value = auth.error || 'Registration failed'
  }
}

// ✅ ДОДАНО: обробники для квадратиків
const handleCodeInput = (index, event) => {
  const value = event.target.value.replace(/\D/g, '')
  code.value[index] = value.slice(-1)
  if (value && index < 5) {
    document.getElementById(`signup-code-${index + 1}`)?.focus()
  }
}

const handleKeyDown = (index, event) => {
  if (event.key === 'Backspace' && !code.value[index] && index > 0) {
    document.getElementById(`signup-code-${index - 1}`)?.focus()
  }
}

const handlePaste = (event) => {
  event.preventDefault()
  const pasted = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6)
  pasted.split('').forEach((char, i) => { code.value[i] = char })
  const lastIdx = Math.min(pasted.length, 5)
  document.getElementById(`signup-code-${lastIdx}`)?.focus()
}

const handleVerifyEmail = async () => {
  errorMsg.value = ''
  const fullCode = code.value.join('')
  if (fullCode.length < 6) {
    errorMsg.value = 'Enter all 6 digits'
    return
  }
  const ok = await auth.verifyEmail(fullCode)
  if (ok) {
    router.push('/login')
  } else {
    errorMsg.value = auth.error || 'Invalid code'
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

      <!-- Step 1: Registration form -->
      <template v-if="!auth.needsEmailVerification">
        <h1 class="title">Sign up</h1>

        <form class="auth-form" @submit.prevent="handleRegister">
          <div class="input-group">
            <label>Username <span class="required">*</span></label>
            <input
              type="text"
              v-model="username"
              class="input-base"
              placeholder="johndoe"
            />
          </div>

          <div class="input-group">
            <label>Email <span class="required">*</span></label>
            <input
              type="email"
              v-model="email"
              class="input-base"
              placeholder="example@mail.com"
            />
          </div>

          <div class="input-group">
            <label>Password <span class="required">*</span></label>
            <div class="password-wrapper">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                class="input-base"
                :class="{ 'input-error': passwordStrength }"
                @input="checkPassword"
                placeholder="••••••••"
              />
              <span class="eye-icon" @mousedown.prevent="showPassword = !showPassword">
                {{ showPassword ? '🙈' : '👁️' }}
              </span>
            </div>
            <span v-if="passwordStrength" class="error-msg">{{ passwordStrength }}</span>
            <p class="hint-msg">Password must contain 1 uppercase letter and 1 special character</p>
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

          <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

          <div class="actions">
            <button class="btn btn-primary create-btn" :disabled="auth.loading">
              {{ auth.loading ? 'Creating account...' : 'Create an account' }}
            </button>
          </div>

          <p class="switch-auth">
            Already have an account? <router-link to="/login">Log in</router-link>
          </p>
        </form>
      </template>

      <!-- Step 2: Email Verification -->
      <template v-else>
        <h1 class="title">Verify your email</h1>
        <p class="verify-hint">We sent a code to <strong>{{ email }}</strong>. Enter it below:</p>

        <form class="auth-form" @submit.prevent="handleVerifyEmail">
          <div class="input-group">
            <label>Verification Code <span class="required">*</span></label>

            <!-- ✅ ЗМІНЕНО: квадратики замість одного поля -->
            <div class="code-inputs">
              <input
                v-for="(digit, idx) in code"
                :key="idx"
                :id="'signup-code-' + idx"
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

          <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

          <div class="actions">
            <button class="btn btn-primary create-btn" :disabled="auth.loading">
              {{ auth.loading ? 'Verifying...' : 'Verify' }}
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
  font-family: 'Inter', sans-serif;
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
  user-select: none;
}
.eye-icon:hover {
  opacity: 1;
}
.actions {
  display: flex;
  flex-direction: column;
  align-items: center;
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
.error-msg {
  color: var(--color-error);
  font-size: 0.85rem;
  display: block;
  margin-top: 0.5rem;
}
.hint-msg {
  color: var(--color-text-light);
  font-size: 0.75rem;
  margin-top: 0.5rem;
}
.create-btn {
  width: 100%;
  max-width: 300px;
  padding: 0.75rem;
}
.verify-hint {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  color: var(--color-text-light);
  margin-bottom: 1.5rem;
  line-height: 1.5;
}
/* ✅ ДОДАНО: стилі для квадратиків */
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
</style>