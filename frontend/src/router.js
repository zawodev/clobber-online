import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ChallengeView from '@/views/ChallengeView.vue'

import ClobberGame from './components/ClobberGame.vue'
import ProfileView from './views/ProfileView.vue'
import FriendsView from './views/FriendsView.vue'
import HomeView from './views/HomeView.vue'
import RoomView from './views/RoomView.vue'

const routes = [
  { path: '/', name: 'LoginView', component: LoginView },
    { path: '/register', name: 'RegisterView', component: RegisterView },
    { path: '/challenge', name: 'ChallengeView', component: ChallengeView },
  { path: '/clob', name: 'ClobberTest', component: ClobberGame },
  { path: '/profile/:username', name: 'ProfileView', component: ProfileView },
  { path: '/friends', name: 'FriendsView', component: FriendsView },
  { path: '/home', name: 'HomeView', component: HomeView },
  { path: '/room/:code', name: 'RoomView', component: RoomView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router