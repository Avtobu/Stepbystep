<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const deckId = route.params.id

// State
const cards = ref([])
const loading = ref(true)
const error = ref(null)

const currentIndex = ref(0)
const isFlipped = ref(false)
const userGuess = ref(null)
const isCorrectGuess = ref(false)

// Track per-session stats
const correctCount = ref(0)
const studiedCount = ref(0)

const currentCard = computed(() => cards.value[currentIndex.value])

// Fetch cards from API
onMounted(async () => {
  try {
    const res = await fetch(`/api/decks/${deckId}/cards`, { credentials: 'include' })
    const json = await res.json()
    if (json.success) {
      cards.value = json.data
    } else {
      error.value = json.error || 'Failed to load cards.'
    }
  } catch (e) {
    error.value = 'Network error. Please try again.'
  } finally {
    loading.value = false
  }
})

// Sync progress to backend
const syncProgress = async () => {
  try {
    await fetch('/api/sync-progress', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        deck_id: Number(deckId),
        cards_studied: studiedCount.value,
        cards_correct: correctCount.value,
      }),
    })
  } catch (e) {
    console.warn('Progress sync failed:', e)
  }
}

// ВИПРАВЛЕННЯ #9: порівнюємо вибір юзера з реальною відповіддю картки
const guess = (userSaidCorrect) => {
  if (isFlipped.value) return

  userGuess.value = userSaidCorrect

  // Реальна відповідь картки: 'correct' = true, 'wrong' = false
  const cardIsCorrect = currentCard.value.answer === 'correct'

  // Юзер правий якщо його вибір співпадає з відповіддю картки
  isCorrectGuess.value = userSaidCorrect === cardIsCorrect

  if (isCorrectGuess.value) correctCount.value++
  studiedCount.value++

  isFlipped.value = true
}

const nextCard = async () => {
  if (currentIndex.value < cards.value.length - 1) {
    isFlipped.value = false
    setTimeout(() => {
      currentIndex.value++
      userGuess.value = null
    }, 400)
  } else {
    // Finished — sync progress then navigate
    await syncProgress()
    router.push(`/deck/${deckId}/success`)
  }
}

const prevCard = () => {
  if (currentIndex.value > 0) {
    isFlipped.value = false
    setTimeout(() => {
      currentIndex.value--
      userGuess.value = null
    }, 400)
  }
}

const resetAndClose = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="study-container">

    <!-- Loading / Error states -->
    <div v-if="loading" class="state-msg">Loading cards…</div>
    <div v-else-if="error" class="state-msg error">{{ error }}</div>
    <div v-else-if="!cards.length" class="state-msg">
      This deck has no cards yet.
      <button class="btn btn-primary" style="margin-top:1rem" @click="router.push('/dashboard')">Go back</button>
    </div>

    <template v-else>
      <!-- Top Bar -->
      <header class="study-header">
        <div class="header-left"></div>

        <div class="progress-indicator">
          <span class="progress-text">Card {{ currentIndex + 1 }} of {{ cards.length }}</span>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" :style="{ width: ((currentIndex + 1) / cards.length) * 100 + '%' }"></div>
          </div>
        </div>

        <button class="close-btn" @click="resetAndClose" title="Exit Study Mode">
          <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </header>

      <!-- Main Card Area -->
      <main class="card-scene">
        <button class="nav-arrow left-arrow" @click="prevCard" :disabled="currentIndex === 0">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>

        <div class="flashcard-wrapper" :class="{ 'is-flipped': isFlipped }">
          <div class="flashcard-inner">

            <!-- FRONT: QUESTION -->
            <div class="flashcard-face flashcard-front">
              <h2 class="q-title">Q:</h2>
              <p class="card-text">{{ currentCard.question }}</p>
              <div class="hint-text">Tap Correct or Wrong below</div>
            </div>

            <!-- BACK: ANSWER -->
            <div class="flashcard-face flashcard-back" :class="isCorrectGuess ? 'result-success' : 'result-error'">
              <div class="back-content">
                <div class="result-icon-wrapper">
                  <svg v-if="isCorrectGuess" viewBox="0 0 24 24" fill="none" class="result-icon success-icon" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" class="result-icon error-icon" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </div>
                <h2 class="result-title">{{ isCorrectGuess ? 'Got it!' : 'Keep going!' }}</h2>
                <p class="card-text small-text">Answer:</p>
                <h2 class="a-title">{{ currentCard.answer }}</h2>
              </div>
            </div>

          </div>
        </div>

        <button class="nav-arrow right-arrow" @click="nextCard">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </main>

      <!-- Bottom Actions -->
      <footer class="study-footer">
        <template v-if="!isFlipped">
          <button class="btn guess-btn btn-wrong lg-btn" @click="guess(false)">Wrong</button>
          <button class="btn guess-btn btn-correct lg-btn" @click="guess(true)">Correct</button>
        </template>
        <template v-else>
          <button class="btn btn-primary lg-btn action-next-btn" @click="nextCard">
            {{ currentIndex < cards.length - 1 ? 'Next Card' : 'Finish' }}
          </button>
        </template>
      </footer>
    </template>

  </div>
</template>

<style scoped>
.study-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 2rem 4rem;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .study-container { padding: 1rem; }
}

.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  font-family: 'Inter', sans-serif;
  font-size: 1.2rem;
  color: var(--color-text-light);
}
.state-msg.error { color: #ef4444; }

/* Header */
.study-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.header-left { width: 50px; }
.progress-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}
.progress-text {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  color: var(--color-text-light);
  font-size: 1.1rem;
}
.close-btn {
  width: 50px; height: 50px;
  border-radius: 50%;
  border: 1px solid #CCCCCC;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  color: var(--color-text);
  transition: all 0.2s ease;
}
.close-btn svg { width: 24px; height: 24px; }
.close-btn:hover {
  border-color: var(--color-error);
  color: var(--color-error);
  transform: scale(1.05);
}

/* Card Scene */
.card-scene {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1200px;
  gap: 2rem;
  margin: 2rem 0;
}
.flashcard-wrapper {
  width: 100%;
  max-width: 600px;
  height: 450px;
}
.flashcard-inner {
  position: relative;
  width: 100%; height: 100%;
  text-align: center;
  transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
  transform-style: preserve-3d;
}
.flashcard-wrapper.is-flipped .flashcard-inner {
  transform: rotateY(180deg);
}
.flashcard-face {
  position: absolute;
  width: 100%; height: 100%;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  background-color: #FFFFFF;
  border-radius: 32px;
  padding: 3rem;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 2px solid rgba(192, 132, 252, 0.15);
}
.flashcard-face::before {
  content: '';
  position: absolute;
  top: 10px; left: 10px; right: -10px; bottom: -10px;
  border: 2px solid rgba(192, 132, 252, 0.1);
  border-radius: 32px;
  background-color: #FAFAFA;
  z-index: -1;
}
.flashcard-back {
  transform: rotateY(180deg);
  transition: background-color 0.4s ease, border-color 0.4s ease;
}
.result-success { background-color: #f0fdf4; border-color: #86efac; }
.result-error   { background-color: #fef2f2; border-color: #fca5a5; }

/* Typography */
.q-title {
  font-family: var(--font-main), 'Playfair Display', serif;
  font-size: 2.2rem;
  color: var(--color-primary);
  margin-bottom: 1rem;
}
.a-title {
  font-family: var(--font-main), 'Playfair Display', serif;
  font-size: 2rem;
  color: #38BDF8;
  margin-top: 0.5rem;
  word-break: break-word;
}
.card-text {
  font-family: 'Inter', sans-serif;
  font-size: 1.5rem;
  color: var(--color-text);
  line-height: 1.5;
  font-weight: 500;
}
.small-text { font-size: 1.1rem; color: var(--color-text-light); }
.result-icon-wrapper { display: flex; justify-content: center; margin-bottom: 1rem; }
.result-icon { width: 80px; height: 80px; }
.success-icon { color: #22c55e; }
.error-icon   { color: #ef4444; }
.result-title {
  font-family: var(--font-main), 'Playfair Display', serif;
  font-size: 2.8rem;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}
.hint-text {
  position: absolute;
  bottom: 2rem;
  font-size: 0.9rem;
  color: #A0A0A0;
  text-transform: uppercase;
  letter-spacing: 2px;
}

/* Nav Arrows */
.nav-arrow {
  width: 60px; height: 60px;
  border-radius: 50%;
  border: none;
  background-color: #FFFFFF;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  color: var(--color-primary);
  transition: all 0.2s ease;
}
.nav-arrow svg { width: 30px; height: 30px; }
.nav-arrow:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 8px 25px rgba(140, 82, 255, 0.2);
}
.nav-arrow:disabled { opacity: 0.3; cursor: not-allowed; }

@media (max-width: 900px) {
  .nav-arrow { display: none; }
}

/* Footer */
.study-footer {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  padding-bottom: 2rem;
}
.guess-btn {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  border: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  color: #fff;
}
.guess-btn:hover { transform: translateY(-3px); }
.btn-correct {
  background-color: #22c55e;
  box-shadow: 0 8px 20px rgba(34, 197, 94, 0.3);
}
.btn-correct:hover {
  background-color: #16a34a;
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.4);
}
.btn-wrong {
  background-color: #ef4444;
  box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
}
.btn-wrong:hover {
  background-color: #dc2626;
  box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4);
}
.action-next-btn { width: 100%; max-width: 400px; }

/* Progress bar */
.progress-bar-bg {
  width: 300px;
  height: 6px;
  background-color: rgba(140, 82, 255, 0.15);
  border-radius: 10px;
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  background-color: var(--color-primary);
  border-radius: 10px;
  transition: width 0.4s ease;
}
</style>