<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const decks = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get('/api/decks')
    // Map API response to the shape the template expects
    decks.value = res.data.data.map(d => ({
      id: d.id,
      name: d.title,
      description: d.description || '',
      cardsCount: d.card_count,
      lastRepetition: d.updated_at
        ? formatRelativeTime(d.updated_at)
        : 'Never'
    }))
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load decks.'
  } finally {
    loading.value = false
  }
})

const filteredDecks = computed(() => {
  if (!searchQuery.value.trim()) return decks.value
  const q = searchQuery.value.toLowerCase()
  return decks.value.filter(
    d => d.name.toLowerCase().includes(q) || d.description.toLowerCase().includes(q)
  )
})

function formatRelativeTime(isoString) {
  const date = new Date(isoString)
  const now = new Date()
  const diffMs = now - date
  const diffMin = Math.floor(diffMs / 60000)
  if (diffMin < 1) return 'Just now'
  if (diffMin < 60) return `${diffMin} minute${diffMin > 1 ? 's' : ''} ago`
  const diffH = Math.floor(diffMin / 60)
  if (diffH < 24) return `${diffH} hour${diffH > 1 ? 's' : ''} ago`
  const diffD = Math.floor(diffH / 24)
  return `${diffD} day${diffD > 1 ? 's' : ''} ago`
}
</script>

<template>
  <div class="dashboard-container">

    <!-- Header -->
    <header class="dashboard-header">
      <router-link to="/" class="logo">
        <div class="mascot-placeholder">
          <span class="owl-icon">🎓</span>
        </div>
        <div class="logo-text">
          <h1 class="logo-title">STEP BY STEP</h1>
          <span class="logo-subtitle">Learn with Flashcards</span>
        </div>
      </router-link>

      <div class="search-bar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search your decks..."
          class="input-base search-input"
        />
        <span class="search-icon">🔍</span>
      </div>

      <router-link to="/cabinet" class="profile-icon" title="My Cabinet">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </router-link>
    </header>

    <!-- Main Content -->
    <main class="dashboard-content">

      <!-- Loading state -->
      <div v-if="loading" class="state-msg">Loading your decks...</div>

      <!-- Error state -->
      <div v-else-if="error" class="state-msg state-error">{{ error }}</div>

      <!-- Decks grid -->
      <div v-else class="decks-grid">

        <!-- Deck Cards -->
        <div v-for="deck in filteredDecks" :key="deck.id" class="deck-card">
          <div class="deck-actions">
            <!-- ▶ Play button → Study mode -->
            <router-link
              :to="'/deck/' + deck.id + '/study'"
              class="icon-btn play-btn"
              title="Study Deck"
            >
              <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
            </router-link>

            <!-- ✏ Edit button → Manage/edit deck -->
            <router-link
              :to="'/deck/' + deck.id + '/manage'"
              class="icon-btn edit-btn"
              title="Edit Deck"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </router-link>
          </div>

          <h2 class="deck-name">{{ deck.name }}</h2>
          <p class="deck-desc">{{ deck.description }}</p>
          <div class="deck-footer">
            <span class="stat">Cards: {{ deck.cardsCount }}</span>
            <span class="stat">Last studied:<br/>{{ deck.lastRepetition }}</span>
          </div>
        </div>

        <!-- Empty search result -->
        <div v-if="!loading && filteredDecks.length === 0 && searchQuery" class="state-msg">
          No decks match "{{ searchQuery }}"
        </div>

        <!-- Add Deck CTA -->
        <div class="add-deck-container">
          <span class="make-more-text">Make more!</span>
          <router-link to="/decks/create" class="add-btn">+</router-link>
        </div>

      </div>
    </main>

  </div>
</template>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  padding: 2rem 4rem;
  display: flex;
  flex-direction: column;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem 2rem;
  }
}

/* --- Header --- */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4rem;
  gap: 2rem;
}

.search-bar {
  flex: 1;
  max-width: 600px;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 2.5rem;
  border-radius: 30px;
  border: 1px solid #CCCCCC;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.5;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-wrap: wrap;
  }
  .search-bar {
    order: 3;
    width: 100%;
    max-width: 100%;
  }
}

/* --- Main Content --- */
.dashboard-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

.state-msg {
  font-family: 'Inter', sans-serif;
  font-size: 1.1rem;
  color: var(--color-text-light, #888);
  margin-top: 4rem;
}

.state-error {
  color: #ef4444;
}

.decks-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
  justify-content: center;
}

/* --- Deck Card --- */
.deck-card {
  width: 260px;
  min-height: 380px;
  background-color: var(--color-primary);
  border-radius: 16px;
  padding: 1.5rem;
  color: #FFFFFF;
  box-shadow: 0 8px 20px rgba(140, 82, 255, 0.4);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
  position: relative;
  text-align: center;
}

.deck-card:hover {
  transform: translateY(-5px);
}

/* ▶ and ✏ action buttons */
.deck-actions {
  position: absolute;
  top: 1.2rem;
  right: 1.2rem;
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  color: #FFFFFF;
  opacity: 0.6;
  width: 32px;
  height: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  transition: all 0.2s ease;
  background-color: rgba(255,255,255,0.1);
  text-decoration: none;
}

.icon-btn:hover {
  opacity: 1;
  background-color: rgba(255,255,255,0.25);
  transform: scale(1.1);
}

.play-btn svg {
  margin-left: 3px;
}

.deck-name {
  font-family: 'Inter', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  margin-top: 1rem;
  line-height: 1.2;
  margin-bottom: 0;
}

.deck-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  opacity: 0.9;
  flex: 1;
  line-height: 1.5;
  margin-bottom: 1.5rem;
  margin-top: 0.75rem;
}

.deck-footer {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-top: 1.5rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  opacity: 0.85;
}

/* --- Add Deck CTA --- */
.add-deck-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 260px;
  min-height: 380px;
  gap: 1.5rem;
}

.make-more-text {
  font-family: var(--font-main), 'Playfair Display', serif;
  font-size: 2rem;
  color: var(--color-text);
  font-weight: 700;
}

.add-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 1px solid var(--color-text);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2rem;
  color: var(--color-text);
  text-decoration: none;
  transition: all 0.3s ease;
  background-color: transparent;
}

.add-btn:hover {
  background-color: var(--color-text);
  color: white;
  transform: scale(1.1);
}
</style>