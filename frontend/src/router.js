import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ChallengeView from '@/views/ChallengeView.vue'

import ClobberGame from './components/ClobberGame.vue'

const routes = [
  { path: '/', name: 'LoginView', component: LoginView },
    { path: '/register', name: 'RegisterView', component: RegisterView },
    { path: '/challenge', name: 'ChallengeView', component: ChallengeView },
    {path: '/clob', name: 'ClobberTest', component: ClobberGame}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router