import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import CabinetView from '../views/CabinetView.vue'
import ProgressView from '../views/ProgressView.vue'
import PersonalInfoView from '../views/PersonalInfoView.vue'
import TwoFactorAuthView from '../views/TwoFactorAuthView.vue'
import DashboardView from '../views/DashboardView.vue'
import CreateDeckView from '../views/CreateDeckView.vue'
import ManageDeckView from '../views/ManageDeckView.vue'
import StudyView from '../views/StudyView.vue'
import StudySuccessView from '../views/StudySuccessView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ── Public routes ───────────────────────────────────────────────
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      meta: { guestOnly: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true }
    },
    {
      path: '/cabinet/2fa',
      name: 'two-factor-auth',
      component: TwoFactorAuthView,
      // без requiresAuth — guard сам перевіряє pendingUserId
    },
    // ── Protected routes ────────────────────────────────────────────
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/cabinet',
      name: 'cabinet',
      component: CabinetView,
      meta: { requiresAuth: true }
    },
    {
      path: '/cabinet/progress',
      name: 'progress',
      component: ProgressView,
      meta: { requiresAuth: true }
    },
    {
      path: '/cabinet/personal-info',
      name: 'personal-info',
      component: PersonalInfoView,
      meta: { requiresAuth: true }
    },
    {
      path: '/decks/create',
      name: 'create-deck',
      component: CreateDeckView,
      meta: { requiresAuth: true }
    },
    {
      path: '/deck/:id/manage',
      name: 'manage-deck',
      component: ManageDeckView,
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: '/deck/:id/study',
      name: 'study-deck',
      component: StudyView,
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: '/deck/:id/success',
      name: 'study-success',
      component: StudySuccessView,
      props: true,
      meta: { requiresAuth: true }
    }
  ]
})

// ── Navigation Guard ────────────────────────────────────────────────
router.beforeEach(async (to) => {
  const { useAuthStore } = await import('../stores/auth')
  const auth = useAuthStore()

  if (!auth.sessionChecked) {
    await auth.fetchMe()
  }

  // Дозволити /cabinet/2fa тільки якщо є pendingUserId або юзер авторизований
  if (to.name === 'two-factor-auth') {
    if (!auth.pendingUserId && !auth.isAuthenticated) {
      return { name: 'login' }
    }
    return true
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }
})

export default router