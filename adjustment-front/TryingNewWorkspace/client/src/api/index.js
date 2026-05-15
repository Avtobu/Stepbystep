import api from './axios'

// ── AUTH ─────────────────────────────────────────────────────────────
// All endpoints match app/api/routes.py in the Flask backend

export const authApi = {
  /**
   * POST /api/register
   * Body: { username, email, password }
   * Returns: { message, user_id } — then need to verify email
   */
  register: (data) => api.post('/register', data),

  /**
   * POST /api/verify-email
   * Body: { user_id, code }
   * Called after register to verify email with the code sent to inbox
   */
  verifyEmail: (userId, code) => api.post('/verify-email', { user_id: userId, code }),

  /**
   * POST /api/login
   * Body: { email, password }
   * Sets session cookie via Flask-Login
   */
  login: (data) => api.post('/login', data),

  /**
   * POST /api/verify-2fa
   * Body: { code }
   * Only needed if user has 2FA enabled
   */
  verify2fa: (code) => api.post('/verify-2fa', { code }),

  /**
   * POST /api/logout
   * Clears the session cookie
   */
  logout: () => api.post('/logout'),
}

// ── DECKS ─────────────────────────────────────────────────────────────

export const decksApi = {
  /** GET /api/decks — list all decks for current user */
  getAll: () => api.get('/decks'),

  /** GET /api/decks/:id */
  getOne: (id) => api.get(`/decks/${id}`),

  /**
   * POST /api/decks
   * Body: { title, description }
   * Note: the server uses "title" not "name"
   */
  create: (data) => api.post('/decks', data),

  /**
   * PUT /api/decks/:id
   * Body: { title, description }
   */
  update: (id, data) => api.put(`/decks/${id}`, data),

  /** DELETE /api/decks/:id */
  remove: (id) => api.delete(`/decks/${id}`),
}

// ── CARDS ─────────────────────────────────────────────────────────────

export const cardsApi = {
  /** GET /api/decks/:deckId/cards */
  getAll: (deckId) => api.get(`/decks/${deckId}/cards`),

  /**
   * POST /api/decks/:deckId/cards
   * Body: { question, answer }
   * Note: our UI uses isCorrect (true/false) for Yes/No cards.
   * Map isCorrect → answer: isCorrect ? 'Correct' : 'Wrong' before sending
   */
  create: (deckId, data) => api.post(`/decks/${deckId}/cards`, data),

  /**
   * PUT /api/cards/:id
   * Body: { question, answer }
   */
  update: (id, data) => api.put(`/cards/${id}`, data),

  /** DELETE /api/cards/:id */
  remove: (id) => api.delete(`/cards/${id}`),
}

export const userApi = {
  /** GET /api/me — get current logged-in user info */
  getMe: () => api.get('/me'),
}
