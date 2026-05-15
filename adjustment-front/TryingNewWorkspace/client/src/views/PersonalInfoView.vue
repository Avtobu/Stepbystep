<script setup>
import { ref, onMounted } from 'vue'
import { userApi } from '@/api/index.js'

const user = ref({
  nickname: '',
  email: '',
  password: '',        // реальний пароль (якщо API повертає)
})

const loading = ref(true)
const error = ref(null)
const showPassword = ref(false)

// Якщо API не повертає пароль — зберігаємо placeholder окремо
const HIDDEN = '••••••••'

onMounted(async () => {
  try {
    const { data } = await userApi.getMe()
    user.value.nickname = data.data.username
    user.value.email = data.data.email
    // Якщо бекенд повертає пароль:
    // user.value.password = data.data.password
    // Якщо ні — залишаємо порожнім, показуємо placeholder
  } catch (err) {
    error.value = 'Не вдалося завантажити дані користувача'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page-container">
    <header class="page-header">
      <router-link to="/cabinet" class="cabinet-logo">
        <div class="mascot-placeholder cabinet-mascot">
          <span class="owl-icon cabinet-owl">🎓</span>
          <span class="back-arrow">
            <img src="/src/assets/LeftArrow.png" alt="Back" class="arrow-img" />
          </span>
        </div>
        <div class="logo-text">
          <h1 class="logo-title">STEP BY STEP</h1>
          <span class="logo-subtitle">Learn with Flashcards</span>
        </div>
      </router-link>
    </header>

    <main class="content-box">
      <h1 class="page-title">Personal Information</h1>

      <div class="info-form">

        <div class="field-group">
          <label>Nickname</label>
          <div class="input-row">
            <input type="text" v-model="user.nickname" class="input-base" readonly />
            <button class="edit-link">Edit</button>
          </div>
        </div>

        <div class="field-group">
          <label>Email</label>
          <div class="input-row">
            <input type="email" v-model="user.email" class="input-base" readonly />
            <button class="edit-link">Edit email</button>
          </div>
        </div>

        <div class="field-group">
          <label>Password</label>
          <div class="input-row">
            <div class="password-wrapper">
              <!-- Якщо пароль невідомий — показуємо placeholder-текст -->
              <input
                v-if="!user.password"
                type="text"
                :value="showPassword ? '[пароль недоступний]' : HIDDEN"
                class="input-base"
                readonly
              />
              <!-- Якщо пароль є — показуємо/ховаємо його -->
              <input
                v-else
                :type="showPassword ? 'text' : 'password'"
                v-model="user.password"
                class="input-base"
                readonly
              />
              <button class="eye-btn" @click="showPassword = !showPassword" type="button" :title="showPassword ? 'Сховати пароль' : 'Показати пароль'">
                <!-- Oko відкрите -->
                <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <!-- Oko закрите -->
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
                  <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
            <button class="edit-link">Edit password</button>
          </div>
        </div>

      </div>

      <div class="danger-zone">
        <button @click="handleDeleteAccount" class="btn btn-outline delete-btn">Delete account</button>
      </div>

    </main>
  </div>
</template>

<style scoped>
/* (стилі ті самі що раніше — нічого не змінювалось) */
.page-container {
  min-height: 100vh;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-header {
  width: 100%;
  max-width: 1200px;
  margin-bottom: 2rem;
}

.cabinet-logo {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  text-decoration: none;
  transition: transform 0.2s ease;
}
.cabinet-logo:hover { transform: scale(1.02); }

.cabinet-mascot { position: relative; overflow: hidden; }

.cabinet-owl,
.back-arrow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: opacity 0.25s ease, transform 0.25s ease;
  line-height: 1;
}
.back-arrow {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
.arrow-img {
  width: 26px;
  height: 26px;
  filter: brightness(0) invert(1);
  display: block;
}
.cabinet-logo:hover .cabinet-mascot { transform: rotate(0deg) scale(1.08); }
.cabinet-logo:hover .cabinet-owl { opacity: 0; transform: translate(-50%, -50%) scale(0.6); }
.cabinet-logo:hover .back-arrow { opacity: 1; transform: translate(-50%, -50%) scale(1); }

.content-box {
  width: 100%;
  max-width: 600px;
  background-color: transparent;
  animation: fadeIn 0.4s ease-out;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  font-family: var(--font-main), 'Playfair Display', serif;
  font-size: 2.2rem;
  color: var(--color-text);
  margin-bottom: 2.5rem;
  text-align: center;
}

.info-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: center;
  width: 100%;
}

.field-group label {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text);
  align-self: flex-start;
  margin-left: 0.5rem;
}

.input-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  justify-content: center;
}

.input-base {
  flex: 1;
  text-align: center;
}
.input-base:read-only { background-color: #FAFAFA; }

.password-wrapper {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
}
.password-wrapper .input-base {
  width: 100%;
  padding-right: 2.5rem;
}

.eye-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-muted, #888);
  display: flex;
  align-items: center;
  padding: 0;
  line-height: 1;
  transition: color 0.2s ease;
}
.eye-btn:hover { color: var(--color-primary); }

.edit-link {
  background: none;
  border: none;
  color: var(--color-primary);
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  white-space: nowrap;
  width: 110px;
  text-align: left;
}
.edit-link:hover { text-decoration: underline; }

.danger-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  width: 100%;
}
.delete-btn {
  border-color: var(--color-error);
  color: var(--color-error);
}
.delete-btn:hover { background-color: rgba(255, 0, 0, 0.05); }
</style>