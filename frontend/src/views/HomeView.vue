<template>
  <div class="rooms-view">
    <div class="join-by-code">
      <input
        v-model="codeInput"
        type="text"
        placeholder="Wpisz kod pokoju…"
      />
      <button @click="joinByCode" class="join-btn">
        Join room
      </button>
    </div>
    <h2>Public rooms</h2>

    <!-- Create Room Panel -->
    <div class="create-panel">
      <h3>Create Your room</h3>
      <div class="field">
        <label>Width: {{ form.width }}</label>
        <input type="range" min="1" max="10" v-model.number="form.width" />
      </div>
      <div class="field">
        <label>Height: {{ form.height }}</label>
        <input type="range" min="1" max="10" v-model.number="form.height" />
      </div>
      <div class="field">
        <label>
          <input type="checkbox" v-model="form.is_public" />
          Public
        </label>
      </div>
      <div class="field">
        <label>Your colour:</label>
        <select v-model="form.creator_color">
          <option value="white">White</option>
          <option value="black">Black</option>
        </select>
      </div>
      <button @click="createRoom" class="create-btn">
        Create room
      </button>
    </div>

    <button @click="loadRooms" class="join-btn">
      Refresh rooms
    </button>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else>
      <div v-if="rooms.length === 0" class="no-rooms">
        No public rooms currently
      </div>

      <div v-else class="rooms-list">
        <div
          v-for="room in rooms"
          :key="room.code"
          class="room-item"
        >
          <div class="info">
            <p><strong>Code:</strong> {{ room.code }}</p>
            <p><strong>Host:</strong> {{ room.host }}</p>
            <p><strong>Players:</strong> {{ room.players.length }}</p>
            <p><strong>Board size:</strong> {{ room.width }}×{{ room.height }}</p>
            <p><strong>Open:</strong> {{ formatDate(room.created_at) }}</p>
          </div>
          <button @click="joinRoom(room.code, room.creator_color)" class="join-btn">
            Join
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router';

const rooms       = ref([]);
const loading     = ref(true);
const router = useRouter();
const codeInput = ref('');

// Form state for creation
const form = ref({
  is_public: true,
  width: 2,
  height: 2,
  creator_color: 'white'
});


const token = sessionStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Token ${token}`;
}

async function loadRooms() {
  loading.value = true;
  try {
    const { data } = await api.get('rooms/public/');
    rooms.value = data;
  } catch (err) {
    console.error('Nie udało się pobrać listy pokoi', err);
    alert('Błąd ładowania pokoi.');
  } finally {
    loading.value = false;
  }
}

// Join a room by code
async function joinRoom(code, creator_color) {
  try {
    await api.post('rooms/join/', { code });
    sessionStorage.setItem('currentRoom', code);
    const colorr = creator_color == "white" ? "black" : "white";
    console.log(colorr)
    router.push({ name: 'RoomView', params: { code },query: { color: colorr } });
  } catch (err) {
    const resp = err.response?.data;
    if (resp?.code === 'already in room' || resp?.detail === 'already in room') {
      sessionStorage.setItem('currentRoom', code);
      const colorr = creator_color == "white" ? "black" : "white";
      router.push({
        name: 'RoomView',
        params: { code },
        query: { color: colorr }
      });
      return;
    }

    console.error('Błąd dołączania do pokoju', err);
    alert(resp?.detail || 'Nie udało się dołączyć do pokoju.');
  }
}

async function createRoom() {
  try {
    const payload = { ...form.value };
    const { data } = await api.post('rooms/create/', payload);

    // Save to localStorage array "createdRooms"
    const existing = JSON.parse(localStorage.getItem('createdRooms') || '[]');
    existing.push(data.code);
    localStorage.setItem('createdRooms', JSON.stringify(existing));
    sessionStorage.setItem('currentRoom', data.code);
      const code = data.code;
    const colorr = data.creator_color
      router.push({ name: 'RoomView', params: { code },query: { color: colorr } });
    console.log(colorr)
  } catch (err) {
    console.error('Błąd tworzenia pokoju', err);
    alert('Nie udało się stworzyć pokoju.');
  }
}
async function joinByCode() {
  const code = codeInput.value.trim();
  if (!code) {
    alert('Podaj kod pokoju.');
    return;
  }
  const { data } = await api.get(`rooms/details/${code}/`);
  console.log("pobrany kolor"+data.creator_color);
  joinRoom(code, data.creator_color);
}

// Utility: format ISO timestamp
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

onMounted(loadRooms);
</script>

<style scoped>
.rooms-view {
  max-width: 700px;
  margin: 0 auto;
  padding: 16px;
}

.create-panel {
  border: 1px solid #4caf50;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  background: #f1f8f1;
}
.create-panel h3 {
  margin-top: 0;
}
.field {
  margin: 8px 0;
}
.create-btn {
  background-color: #197b30;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
}
.create-btn:hover {
  background-color: #145c24;
}

.loading,
.no-rooms {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 24px;
}

.rooms-list {
  max-height: 450px;
  overflow-y: auto;
  margin-top: 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.room-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.room-item:last-child {
  border-bottom: none;
}

.info p {
  margin: 4px 0;
}

.join-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
}

.join-btn:hover {
  background-color: #388e3c;
}
</style>