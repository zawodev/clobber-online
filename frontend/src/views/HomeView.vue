<template>
    <div class="rooms-view">
        <h2>Dostępne pokoje publiczne</h2>
        <button @click="loadRooms" class="join-btn">
            Odśwież
        </button>
        <div v-if="loading" class="loading">Ładowanie pokoi…</div>

        <div v-else>
            <div v-if="rooms.length === 0" class="no-rooms">
                Brak publicznych pokoi
            </div>

            <div v-else class="rooms-list">
                <div v-for="room in rooms" :key="room.code" class="room-item">
                    <div class="info">
                        <p><strong>Kod:</strong> {{ room.code }}</p>
                        <p><strong>Host:</strong> {{ room.host }}</p>
                        <p><strong>Graczy:</strong> {{ room.players.length }}</p>
                        <p>
                            <strong>Rozmiar:</strong>
                            {{ room.width }}×{{ room.height }}
                        </p>
                        <p><strong>Utworzono:</strong> {{ formatDate(room.created_at) }}</p>
                    </div>
                    <button @click="joinRoom(room.code)" class="join-btn">
                        Dołącz
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

const rooms = ref([]);
const loading = ref(true);
const router = useRouter();


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


async function joinRoom(code) {
    try {
        await api.post('rooms/join/', { code });
        // store in sessionStorage
        sessionStorage.setItem('currentRoom', code);
        router.push({ name: 'RoomView', params: { code } });
    } catch (err) {
        console.error('Błąd dołączania do pokoju', err);
        alert('Nie udało się dołączyć do pokoju.');
    }
}


function formatDate(iso) {
    const d = new Date(iso);
    return d.toLocaleString('pl-PL', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
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