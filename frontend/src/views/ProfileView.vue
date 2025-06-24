<template>
  <div class="profile-view">
    <!-- HEADER: avatar + username -->
    <div class="profile-header">
      <div class="avatar-wrapper" @click="onAvatarClick" :class="{ clickable: isOwn }">
        <img :src="avatarSrc" alt="Avatar" class="avatar" />
        <input type="file" ref="fileInput" class="avatar-input" @change="uploadAvatar" accept="image/*" />
      </div>
      <h2 class="username">{{ profile.username }}</h2>
    </div>

    <!-- MAIN CONTENT -->
    <div class="profile-content">
      <!-- LEFT: stats -->
      <div class="stats">
        <p><strong>ELO:</strong> {{ profile.elo }}</p>
        <p><strong>Email:</strong> {{ profile.email }}</p>
      </div>

      <!-- RIGHT: friends -->
      <div class="friends">
        <button v-if="!isOwn && !isFriend" @click="inviteFriend" class="invite-btn">
          ➕ Send a friend invite!
        </button>
        <h3>Friends</h3>
        <div v-if="!profile.friends.length" class="no-friends">
          This user doesn't have any friends yet
        </div>
        <ul v-else>
          <li v-for="friend in profile.friends" :key="friend.username" class="friend">
            <img :src="friend.avatar || require('@/assets/def_profile.png')" class="friend-avatar" />
            <router-link :to="`/profile/${friend.username}`">{{ friend.username }}</router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';

const route = useRoute();
const router = useRouter();

const token = sessionStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Token ${token}`;
}

const usernameParam = route.params.username;
const myUsername = sessionStorage.getItem('username');

const isOwn = usernameParam === myUsername;
var isFriend = true;

const profile = ref({
  id: null,
  username: '',
  email: '',
  email_confirmed: false,
  avatar: null,
  elo: 0,
  friends: []
});

// file input ref
const fileInput = ref(null);

const avatarSrc = computed(() => {
  return profile.value.avatar || require('@/assets/def_profile.png');
});

async function fetchProfile() {
  try {
    const { data } = await api.get(`/users/profile/${usernameParam}/`);
    profile.value = data;
    isFriend = profile.value.friends.some(friend => friend.username === myUsername);
  } catch (err) {
    console.error('Failed to load profile', err);
    // e.g. redirect if 404
    if (err.response && err.response.status === 404) {
      router.replace('/');
    }
  }
}
async function inviteFriend() {
  try {
    await api.post('/users/friend-request/send/', {
      to_username: usernameParam
    });
    alert(`Wysłano zaproszenie do ${usernameParam}!`);
  } catch (err) {
    console.error('Błąd podczas wysyłania zaproszenia', err);
    if (err.response?.status === 400) {
      alert('Zaproszenie już zostało wysłane lub użytkownik jest już znajomym.');
    } else {
      alert('Nie udało się wysłać zaproszenia.');
    }
  }
}
function onAvatarClick() {
  if (isOwn && fileInput.value) {
    fileInput.value.click();
  }
}

async function uploadAvatar(event) {
  const file = event.target.files[0];
  if (!file) return;

  const form = new FormData();
  form.append('avatar', file);

  try {
    const { data } = await api.post(
      '/users/avatar/upload/',
      form,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    // assume response returns new avatar URL
    profile.value.avatar = data.avatar;
  } catch (err) {
    console.error('Avatar upload failed', err);
    alert('Nie udało się wgrać zdjęcia.');
  }
}

onMounted(fetchProfile);
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

/* LEFT COLUMN: stats */
.stats {
  flex: 1;
  font-size: 1rem;
}

.stats p {
  margin: 8px 0;
}

/* RIGHT COLUMN: friends */
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
</style>