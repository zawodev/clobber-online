<template>
  <div class="friends-view">
    <h2>Zaproszenia do znajomych</h2>

    <div v-if="loading" class="loading">
      Ładowanie…
    </div>

    <div v-else>
      <div v-if="requests.length === 0" class="no-requests">
        Brak oczekujących zaproszeń
      </div>

      <div v-else class="requests-list">
        <div
          v-for="req in requests"
          :key="req.id"
          class="request-item"
        >
          <div class="info">
            <strong>{{ req.from_username }}</strong>
            <small>{{ formatDate(req.created) }}</small>
          </div>
          <div class="actions">
            <button @click="respond(req.id, 'accept')">Accept</button>
            <button @click="respond(req.id, 'deny')">Deny</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const requests = ref([]);
const loading  = ref(true);

// ensure auth header
const token = sessionStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Token ${token}`;
}

// fetch incoming requests
async function loadRequests() {
  loading.value = true;
  try {
    const { data } = await api.get('users/friend-request/incoming/');
    requests.value = data;
  } catch (err) {
    console.error('Failed to load friend requests', err);
    alert('Nie udało się pobrać zaproszeń.');
  } finally {
    loading.value = false;
  }
}

// respond to a request
async function respond(id, action) {
  try {
    await api.post(`users/friend-request/${id}/respond/`, { action });
    // remove from list
    requests.value = requests.value.filter(r => r.id !== id);
  } catch (err) {
    console.error('Failed to respond to friend request', err);
    alert('Coś poszło nie tak przy wysyłaniu odpowiedzi.');
  }
}

// utility to format ISO timestamp
function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleString('pl-PL', {
    year:   'numeric',
    month:  '2-digit',
    day:    '2-digit',
    hour:   '2-digit',
    minute: '2-digit',
  });
}

onMounted(loadRequests);
</script>

<style scoped>
.friends-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
}

.loading,
.no-requests {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 24px;
}

.requests-list {
  max-height: 400px;       /* scroll if too many */
  overflow-y: auto;
  margin-top: 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.request-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.request-item:last-child {
  border-bottom: none;
}

.info {
  display: flex;
  flex-direction: column;
}

.info strong {
  color: #2e7d32;
}

.info small {
  color: #999;
  font-size: 0.85em;
}

.actions button {
  margin-left: 8px;
  padding: 6px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.actions button:first-child {
  background-color: #4caf50;
  color: white;
}

.actions button:first-child:hover {
  background-color: #388e3c;
}

.actions button:last-child {
  background-color: #f44336;
  color: white;
}

.actions button:last-child:hover {
  background-color: #c62828;
}
</style>