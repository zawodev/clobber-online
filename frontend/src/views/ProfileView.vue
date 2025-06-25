<template>
  <div class="profile-view">
    <div class="profile-header">
      <div class="avatar-wrapper" @click="onAvatarClick" :class="{ clickable: isOwn }">
        <img :src="avatarSrc" alt="Avatar" class="avatar" />
        <input type="file" ref="fileInput" class="avatar-input" @change="uploadAvatar" accept="image/*" />
      </div>
      <h2 class="username">{{ profile.username }}</h2>
      <button v-if="isOwn" @click="logout" class="logout-btn">Logout</button>
    </div>

    <div class="profile-content">
      <div class="stats">
        <p><strong>ELO:</strong> {{ profile.elo }}</p>
        <p><strong>Wins:</strong> {{ profile.wins }}</p>
        <p><strong>Losses:</strong> {{ profile.losses }}</p>
        <p><strong>Winrate:</strong> {{ profile.winrate }}</p>
      </div>

      <div class="friends">
        <button v-if="!isOwn && !isFriend" @click="inviteFriend" class="invite-btn">
          ➕ Send a friend invite!
        </button>
        <h3>Friends</h3>
        <div v-if="!profile.friends.length" class="no-friends">
          This user doesn't have any friends yet
        </div>
        <div class="friends-list-wrapper" v-else>
          <ul>
            <li v-for="friend in profile.friends" :key="friend.username" class="friend">
              <img :src="friend.avatar || require('@/assets/def_profile.png')" class="friend-avatar" />
              <router-link :to="`/profile/${friend.username}`">
                {{ friend.username }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <h3>Game History</h3>
    <div class="history-container" v-auto-animate>
      <div class="history-wrapper" v-auto-animate>
        <ul class="history-list" v-auto-animate>
          <li v-for="item in history" :key="item.id" class="history-item">
            <strong>{{ item.played_at.slice(0, 10) }}</strong><br />
            Winner: {{ item.winner || 'Clobber-bot' }}<br />
            Loser: {{ item.loser || 'Clobber-bot' }}
          </li>
        </ul>
        <div v-if="historyLoading" class="loading">Loading…</div>
      </div>

      <div class="history-controls">
        <button @click="loadPrevious" :disabled="!prevHistoryUrl || historyLoading">
          ⬆ Prev
        </button>
        <button @click="loadNext" :disabled="!nextHistoryUrl || historyLoading">
          ⬇ Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const token = sessionStorage.getItem('token')
if (token) api.defaults.headers.common['Authorization'] = `Token ${token}`

const usernameParam = route.params.username
const myUsername = sessionStorage.getItem('username')
const isOwn = usernameParam === myUsername
let isFriend = false

const profile = ref({
  id: null, username: '',
  email: '', email_confirmed: false,
  avatar: null, elo: 0,
  wins: 0, losses: 0, winrate: 0,
  friends: []
})

const fileInput = ref(null)
const avatarSrc = computed(() =>
  profile.value.avatar || require('@/assets/def_profile.png')
)

const history = ref([])
const nextHistoryUrl = ref(null)
const prevHistoryUrl = ref(null)
const historyLoading = ref(false)

async function fetchProfile() {
  try {
    const { data } = await api.get(`/users/profile/${usernameParam}/`)
    profile.value = data
    isFriend = data.friends.some(f => f.username === myUsername)
    // after profile loads, load first page of history
    fetchHistoryPage()
  }
  catch (err) {
    if (err.response?.status === 404) router.replace('/')
  }
}

async function inviteFriend() {
  try {
    await api.post('/users/friend-request/send/', {
      to_username: usernameParam
    })
    alert(`Sent invite to ${usernameParam}!`)
  }
  catch {
    alert('Error sending friend invite.')
  }
}

function onAvatarClick() {
  if (isOwn && fileInput.value) fileInput.value.click()
}
async function uploadAvatar(e) {
  const file = e.target.files[0]
  if (!file) return
  const form = new FormData()
  form.append('avatar', file)
  try {
    const { data } = await api.post(
      '/users/avatar/upload/',
      form,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    profile.value.avatar = data.avatar
    window.location.reload(true)
  }
  catch {
    alert('Nie udało się wgrać zdjęcia.')
  }
}

async function fetchHistoryPage(url = null) {
  if (historyLoading.value) return
  historyLoading.value = true

  let res
  if (url) {
    // next/previous links already include limit & offset
    res = await api.get(url, { data: { username: profile.value.username } })
  }
  else {
    res = await api.get('game/history/', {
      params: { username: profile.value.username, limit: 2, offset: history.value.length },
    })
  }

  history.value = res.data.results
  nextHistoryUrl.value = res.data.next
  prevHistoryUrl.value = res.data.previous
  historyLoading.value = false
}

function loadNext() {
  if (nextHistoryUrl.value) {
    fetchHistoryPage(nextHistoryUrl.value, true)
  }
}
function loadPrevious() {
  if (prevHistoryUrl.value) {
    fetchHistoryPage(prevHistoryUrl.value, true)
  }
}
function logout() {
  sessionStorage.clear()
  router.push('/')
  .then(() => {
      window.location.reload();
    });
}

onMounted(fetchProfile)
</script>


<style scoped>
.profile-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 16px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.avatar-wrapper {
  position: relative;
}

.avatar-wrapper.clickable {
  cursor: pointer;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #2e7d32;
}

.avatar-input {
  display: none;
}

.username {
  font-size: 1.5rem;
  color: #2e7d32;
}

.profile-content {
  display: flex;
  gap: 32px;
}

.stats {
  flex: 1;
  font-size: 1rem;
}

.stats p {
  margin: 8px 0;
}

.friends {
  flex: 1;
}

.friends h3 {
  margin-bottom: 8px;
}

.no-friends {
  color: #999;
  font-style: italic;
}

.friends-list-wrapper {
  flex: 1;
  max-height: 200px;
  overflow-y: auto;
  margin-top: 8px;
}

.friend {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.friend-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #ccc;
}

.friend-name {
  font-size: 1rem;
  color: #333;
}

.invite-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  margin-left: auto;
}

.invite-btn:hover {
  background-color: #388e3c;
}

.logout-btn {
  background-color: #dd4343;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  margin-left: auto;
}
.logout-btn:hover {
  background-color: #732f26;
}
.history-wrapper {
  height: 200px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px;
}

.history-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.history-item {
  background: #fafafa;
  margin-bottom: 8px;
  padding: 12px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.loading,
.end {
  text-align: center;
  padding: 12px;
  color: #666;
}
.history-controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
  justify-content: start;
}

.history-controls button {
  padding: 6px 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.history-controls button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>