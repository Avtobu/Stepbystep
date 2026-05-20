<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '@/api/index.js'
import { useAuthStore } from '@/stores/auth'
import leftArrow from '@/assets/LeftArrow.png'

const router = useRouter()
const auth = useAuthStore()

const userId = ref(null)
const user = ref({ nickname: '', email: '' })
const loading = ref(true)
const globalError = ref(null)
const showDeleteModal = ref(false)

// ВИПРАВЛЕННЯ #10: додано поле пароля та помилки для модалки видалення
const deletePassword = ref('')
const deleteError = ref('')

onMounted(async () => {
  try {
    const { data } = await userApi.getMe()
    userId.value = data.data.id
    user.value.nickname = data.data.username
    user.value.email = data.data.email
  } catch (err) {
    globalError.value = 'Failed to load user data'
    console.error(err)
  } finally {
    loading.value = false
  }
})

const editingField = ref(null)
const editStep = ref('input')
const saving = ref(false)
const fieldError = ref('')
const fieldSuccess = ref('')
const tempNickname = ref('')
const tempEmail = ref('')
const tempNewPassword = ref('')
const tempConfirmPassword = ref('')
const verifyCode = ref(['', '', '', '', '', ''])

function startEdit(field) {
  editingField.value = field
  editStep.value = 'input'
  fieldError.value = ''
  fieldSuccess.value = ''
  verifyCode.value = ['', '', '', '', '', '']
  if (field === 'nickname') tempNickname.value = user.value.nickname
  if (field === 'email') tempEmail.value = ''
  if (field === 'password') { tempNewPassword.value = ''; tempConfirmPassword.value = '' }
}

function cancelEdit() {
  editingField.value = null
  editStep.value = 'input'
  fieldError.value = ''
  fieldSuccess.value = ''
  verifyCode.value = ['', '', '', '', '', '']
}

function getCodeString() {
  return verifyCode.value.join('')
}

function handleCodeInput(index, event) {
  const val = event.target.value.replace(/\D/g, '')
  verifyCode.value[index] = val.slice(-1)
  if (val && index < 5) {
    document.getElementById(`code-input-${index + 1}`)?.focus()
  }
}

function handleCodeKeydown(index, event) {
  if (event.key === 'Backspace' && !verifyCode.value[index] && index > 0) {
    document.getElementById(`code-input-${index - 1}`)?.focus()
  }
}

async function saveNickname() {
  const val = tempNickname.value.trim()
  if (!val) { fieldError.value = 'Nickname cannot be empty'; return }
  if (val.length < 3) { fieldError.value = 'Minimum 3 characters'; return }
  if (val === user.value.nickname) { cancelEdit(); return }
  saving.value = true; fieldError.value = ''
  try {
    await userApi.updateUsername(userId.value, val)
    user.value.nickname = val
    fieldSuccess.value = 'Nickname updated!'
    setTimeout(cancelEdit, 1500)
  } catch (err) {
    fieldError.value = err?.response?.data?.error || 'Failed to save'
  } finally {
    saving.value = false
  }
}

async function requestEmailChange() {
  const val = tempEmail.value.trim()
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!val) { fieldError.value = 'Please enter a new email'; return }
  if (!emailRegex.test(val)) { fieldError.value = 'Invalid email address'; return }
  if (val === user.value.email) { fieldError.value = 'This is already your current email'; return }
  saving.value = true; fieldError.value = ''
  try {
    await userApi.requestEmailChange(userId.value, val)
    editStep.value = 'verify'
    verifyCode.value = ['', '', '', '', '', '']
    setTimeout(() => document.getElementById('code-input-0')?.focus(), 100)
  } catch (err) {
    fieldError.value = err?.response?.data?.error || 'Failed to send verification code'
  } finally {
    saving.value = false
  }
}

async function confirmEmailChange() {
  const code = getCodeString()
  if (code.length < 6) { fieldError.value = 'Please enter the full 6-digit code'; return }
  saving.value = true; fieldError.value = ''
  try {
    await userApi.confirmEmailChange(userId.value, tempEmail.value.trim(), code)
    user.value.email = tempEmail.value.trim()
    fieldSuccess.value = 'Email updated successfully!'
    setTimeout(cancelEdit, 1500)
  } catch (err) {
    fieldError.value = err?.response?.data?.error || 'Invalid or expired code'
  } finally {
    saving.value = false
  }
}

async function requestPasswordChange() {
  if (!tempNewPassword.value) { fieldError.value = 'Please enter a new password'; return }
  if (tempNewPassword.value.length < 8) { fieldError.value = 'Minimum 8 characters'; return }
  if (tempNewPassword.value !== tempConfirmPassword.value) { fieldError.value = 'Passwords do not match'; return }
  saving.value = true; fieldError.value = ''
  try {
    await userApi.sendPasswordCode(userId.value)
    editStep.value = 'verify'
    verifyCode.value = ['', '', '', '', '', '']
    setTimeout(() => document.getElementById('code-input-0')?.focus(), 100)
  } catch (err) {
    fieldError.value = err?.response?.data?.error || 'Failed to send verification code'
  } finally {
    saving.value = false
  }
}

async function confirmPasswordChange() {
  const code = getCodeString()
  if (code.length < 6) { fieldError.value = 'Please enter the full 6-digit code'; return }
  saving.value = true; fieldError.value = ''
  try {
    await userApi.changePassword(userId.value, code, tempNewPassword.value)
    fieldSuccess.value = 'Password changed successfully!'
    setTimeout(cancelEdit, 1500)
  } catch (err) {
    fieldError.value = err?.response?.data?.error || 'Invalid or expired code'
  } finally {
    saving.value = false
  }
}

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}

// ВИПРАВЛЕННЯ #10: перевіряємо пароль перед видаленням акаунту
async function handleDeleteAccount() {
  deleteError.value = ''
  if (!deletePassword.value) {
    deleteError.value = 'Please enter your password to confirm'
    return
  }
  try {
    await userApi.deleteAccount(userId.value, deletePassword.value)
  } catch (err) {
    deleteError.value = err?.response?.data?.error || 'Incorrect password. Please try again.'
    return
  }
  await auth.logout()
  router.push('/login')
}

// ВИПРАВЛЕННЯ #10: скидаємо поля при закритті модалки
function closeDeleteModal() {
  showDeleteModal.value = false
  deletePassword.value = ''
  deleteError.value = ''
}
</script>

<template>
  <div class="page-container">
    <Transition name="modal">
      <!-- ВИПРАВЛЕННЯ #10: оновлена модалка з полем пароля -->
      <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
        <div class="modal-box">
          <div class="modal-icon">🗑️</div>
          <h2 class="modal-title">Delete account?</h2>
          <p class="modal-text">
            This action is <strong>permanent</strong> and cannot be undone.
            All your decks, cards, and progress will be lost.
            Enter your password to confirm.
          </p>
          <input
            type="password"
            v-model="deletePassword"
            class="input-base delete-password-input"
            placeholder="Enter your password"
            @keydown.enter="handleDeleteAccount"
          />
          <p v-if="deleteError" class="delete-error">{{ deleteError }}</p>
          <div class="modal-actions">
            <button class="modal-btn-cancel" @click="closeDeleteModal">Cancel</button>
            <button class="modal-btn-delete" @click="handleDeleteAccount">Yes, delete</button>
          </div>
        </div>
      </div>
    </Transition>

    <header class="page-header">
      <router-link to="/cabinet" class="cabinet-logo">
        <div class="mascot-placeholder cabinet-mascot">
          <span class="owl-icon cabinet-owl">🎓</span>
          <span class="back-arrow">
            <img :src="leftArrow" alt="Back" class="arrow-img" />
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

      <div v-if="loading" class="loading-state">Loading...</div>

      <div v-else-if="globalError" class="error-banner">
        {{ globalError }}
        <button class="retry-btn" @click="globalError = null; $router.go(0)">Retry</button>
      </div>

      <div v-else class="info-form">
        <!-- NICKNAME -->
        <div class="field-group">
          <label>Nickname</label>
          <template v-if="editingField !== 'nickname'">
            <div class="input-row">
              <input type="text" :value="user.nickname" class="input-base" readonly />
              <button class="edit-link" @click="startEdit('nickname')">Edit nickname</button>
            </div>
          </template>
          <template v-else>
            <div class="edit-block">
              <div class="input-row">
                <input
                  type="text"
                  v-model="tempNickname"
                  class="input-base input-active"
                  placeholder="New nickname"
                  autofocus
                  @keydown.enter="saveNickname"
                  @keydown.esc="cancelEdit"
                />
              </div>
              <p v-if="fieldError" class="field-error">{{ fieldError }}</p>
              <p v-if="fieldSuccess" class="field-success">{{ fieldSuccess }}</p>
              <div class="action-row">
                <button class="btn-save" @click="saveNickname" :disabled="saving">
                  {{ saving ? 'Saving...' : 'Save' }}
                </button>
                <button class="btn-cancel" @click="cancelEdit">Cancel</button>
              </div>
            </div>
          </template>
        </div>

        <!-- EMAIL -->
        <div class="field-group">
          <label>Email</label>
          <template v-if="editingField !== 'email'">
            <div class="input-row">
              <input type="email" :value="user.email" class="input-base" readonly />
              <button class="edit-link" @click="startEdit('email')">Edit email</button>
            </div>
          </template>
          <template v-else-if="editStep === 'input'">
            <div class="edit-block">
              <p class="edit-hint">Enter a new address — we'll send a verification code to it</p>
              <div class="input-row">
                <input
                  type="email"
                  v-model="tempEmail"
                  class="input-base input-active"
                  placeholder="New email address"
                  autofocus
                  @keydown.enter="requestEmailChange"
                  @keydown.esc="cancelEdit"
                />
              </div>
              <p v-if="fieldError" class="field-error">{{ fieldError }}</p>
              <div class="action-row">
                <button class="btn-save" @click="requestEmailChange" :disabled="saving">
                  {{ saving ? 'Sending...' : 'Send code' }}
                </button>
                <button class="btn-cancel" @click="cancelEdit">Cancel</button>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="edit-block verify-block">
              <p class="edit-hint">Code sent to <strong>{{ tempEmail }}</strong></p>
              <div class="code-inputs">
                <input
                  v-for="(digit, idx) in verifyCode"
                  :key="idx"
                  :id="'code-input-' + idx"
                  type="text"
                  inputmode="numeric"
                  maxlength="1"
                  :value="verifyCode[idx]"
                  @input="handleCodeInput(idx, $event)"
                  @keydown="handleCodeKeydown(idx, $event)"
                  class="digit-box"
                />
              </div>
              <p v-if="fieldError" class="field-error">{{ fieldError }}</p>
              <p v-if="fieldSuccess" class="field-success">{{ fieldSuccess }}</p>
              <div class="action-row">
                <button class="btn-save" @click="confirmEmailChange" :disabled="saving">
                  {{ saving ? 'Verifying...' : 'Confirm' }}
                </button>
                <button class="btn-cancel" @click="() => { editStep = 'input'; fieldError = '' }">Back</button>
              </div>
            </div>
          </template>
        </div>

        <!-- PASSWORD -->
        <div class="field-group">
          <label>Password</label>
          <template v-if="editingField !== 'password'">
            <div class="input-row">
              <input type="password" value="••••••••" class="input-base" readonly />
              <button class="edit-link" @click="startEdit('password')">Edit password</button>
            </div>
          </template>
          <template v-else-if="editStep === 'input'">
            <div class="edit-block">
              <p class="edit-hint">A verification code will be sent to your current email</p>
              <div class="input-row">
                <input
                  type="password"
                  v-model="tempNewPassword"
                  class="input-base input-active"
                  placeholder="New password (min. 8 characters)"
                  autofocus
                  @keydown.esc="cancelEdit"
                />
              </div>
              <div class="input-row" style="margin-top: 0.75rem;">
                <input
                  type="password"
                  v-model="tempConfirmPassword"
                  class="input-base input-active"
                  placeholder="Confirm new password"
                  @keydown.enter="requestPasswordChange"
                  @keydown.esc="cancelEdit"
                />
              </div>
              <p v-if="fieldError" class="field-error">{{ fieldError }}</p>
              <div class="action-row">
                <button class="btn-save" @click="requestPasswordChange" :disabled="saving">
                  {{ saving ? 'Sending...' : 'Send code' }}
                </button>
                <button class="btn-cancel" @click="cancelEdit">Cancel</button>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="edit-block verify-block">
              <p class="edit-hint">Code sent to <strong>{{ user.email }}</strong></p>
              <div class="code-inputs">
                <input
                  v-for="(digit, idx) in verifyCode"
                  :key="idx"
                  :id="'code-input-' + idx"
                  type="text"
                  inputmode="numeric"
                  maxlength="1"
                  :value="verifyCode[idx]"
                  @input="handleCodeInput(idx, $event)"
                  @keydown="handleCodeKeydown(idx, $event)"
                  class="digit-box"
                />
              </div>
              <p v-if="fieldError" class="field-error">{{ fieldError }}</p>
              <p v-if="fieldSuccess" class="field-success">{{ fieldSuccess }}</p>
              <div class="action-row">
                <button class="btn-save" @click="confirmPasswordChange" :disabled="saving">
                  {{ saving ? 'Verifying...' : 'Confirm' }}
                </button>
                <button class="btn-cancel" @click="() => { editStep = 'input'; fieldError = '' }">Back</button>
              </div>
            </div>
          </template>
        </div>
      </div>

      <div class="danger-zone">
        <button @click="handleLogout" class="btn btn-outline logout-btn">Log out</button>
        <button @click="showDeleteModal = true" class="btn btn-outline delete-btn">Delete account</button>
      </div>
    </main>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal-box {
  background: #fff;
  border-radius: 20px;
  padding: 2.5rem 2rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  animation: popIn 0.25s ease-out;
}
@keyframes popIn {
  from { opacity: 0; transform: scale(0.92); }
  to   { opacity: 1; transform: scale(1); }
}
.modal-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.modal-title {
  font-family: var(--font-main), 'Playfair Display', serif;
  font-size: 1.6rem;
  color: var(--color-text);
  margin-bottom: 0.75rem;
}
.modal-text {
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.25rem;
}
/* ВИПРАВЛЕННЯ #10: стилі для поля пароля і помилки в модалці */
.delete-password-input {
  width: 100%;
  margin-bottom: 0.5rem;
  text-align: center;
}
.delete-error {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #e53e3e;
  margin-bottom: 1rem;
}
.modal-actions { display: flex; gap: 1rem; justify-content: center; margin-top: 1.25rem; }
.modal-btn-cancel {
  padding: 0.6rem 1.5rem;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.15);
  background: none;
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.15s;
}
.modal-btn-cancel:hover { background: rgba(0,0,0,0.04); }
.modal-btn-delete {
  padding: 0.6rem 1.5rem;
  border-radius: 10px;
  border: none;
  background: #e53e3e;
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.15s;
}
.modal-btn-delete:hover { opacity: 0.88; transform: translateY(-1px); }
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }

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
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
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
.input-base { flex: 1; text-align: center; }
.input-base:read-only { background-color: #FAFAFA; }
.input-active {
  background-color: #fff;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
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
.edit-block {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  animation: slideDown 0.2s ease-out;
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}
.edit-hint {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: var(--color-text-light, #888);
  margin: 0 0 0.25rem 0.25rem;
}
.verify-block { align-items: center; }
.code-inputs {
  display: flex;
  gap: 0.6rem;
  margin: 0.5rem 0;
  justify-content: center;
}
.digit-box {
  width: 46px;
  height: 52px;
  text-align: center;
  font-size: 1.4rem;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  border: 1.5px solid #CCCCCC;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  caret-color: var(--color-primary);
}
.digit-box:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}
.action-row {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
  justify-content: flex-end;
}
.btn-save {
  background-color: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.45rem 1.2rem;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: opacity 0.2s ease, transform 0.15s ease;
}
.btn-save:hover:not(:disabled) { opacity: 0.88; transform: translateY(-1px); }
.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-cancel {
  background: none;
  border: 1px solid rgba(0,0,0,0.15);
  border-radius: 8px;
  padding: 0.45rem 1rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  color: var(--color-text);
  cursor: pointer;
  transition: background 0.15s ease;
}
.btn-cancel:hover { background-color: rgba(0,0,0,0.04); }
.field-error {
  font-size: 0.82rem;
  color: var(--color-error, #e53e3e);
  margin: 0;
  padding-left: 0.25rem;
}
.field-success {
  font-size: 0.82rem;
  color: #38a169;
  margin: 0;
  padding-left: 0.25rem;
}
.loading-state {
  color: var(--color-text);
  font-family: 'Inter', sans-serif;
  padding: 2rem;
  opacity: 0.6;
}
.error-banner {
  color: var(--color-error, #e53e3e);
  font-family: 'Inter', sans-serif;
  padding: 1rem;
  background: rgba(229, 62, 62, 0.07);
  border-radius: 8px;
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}
.retry-btn {
  background: none;
  border: 1px solid var(--color-error, #e53e3e);
  color: var(--color-error, #e53e3e);
  border-radius: 6px;
  padding: 0.3rem 1rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  cursor: pointer;
  transition: background 0.15s;
}
.retry-btn:hover { background: rgba(229, 62, 62, 0.08); }
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
.logout-btn {
  border-color: var(--color-primary);
  color: var(--color-primary);
  margin-bottom: 0.75rem;
}
.logout-btn:hover { background-color: rgba(99, 102, 241, 0.05); }
</style>