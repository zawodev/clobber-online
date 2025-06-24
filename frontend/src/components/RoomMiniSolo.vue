<template>
  <div class="challenge-card">
    <div class="card-header">
      <h3 class="title">{{ title }}</h3>
      <span class="description">{{ description }}</span>
    </div>
    <ul class="card-details">
      <li><strong>Difficulty:</strong> Medium</li>
      <li><strong>Width:</strong> {{ width }}</li>
      <li><strong>Height</strong> {{ height }}</li>
    </ul>
    <button class="play-btn" @click="onPlay">Play</button>
  </div>
</template>

<script>
import api from '@/api';
import router from '@/router';

export default {
  name: 'RoomMiniSolo',
  props: {
    id: {
      type: Number,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    width: {
      type: Number,
      required: true
    },
    height: {
      type: Number,
      required: true
    }
  },
  methods: {
    async onPlay() {
      const { data } = await api.post('rooms/create/', {
        "is_public": false,
        "width": this.width,
        "height": this.height,
        "creator_color": "black",
        "challenge": this.id
      });
      const existing = JSON.parse(localStorage.getItem('createdRooms') || '[]');
      existing.push(data.code);
      localStorage.setItem('createdRooms', JSON.stringify(existing));
      sessionStorage.setItem('currentRoom', data.code);
      const code = data.code;
      const colorr = data.creator_color
      router.push({ name: 'RoomView', params: { code }, query: { color: colorr } });
    }
  }
}
</script>

<style scoped>
.challenge-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  padding: 16px;
  width: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 8px;
  transition: transform 0.2s ease;
  transform-style: preserve-3d;
  perspective: 1000px;

}

.card-header {
  margin-bottom: 12px;
}

.points {
  font-size: 0.9rem;
  color: #555;
}

.title {
  margin: 4px 0 0;
  font-size: 1.1rem;
  color: #333;
}

.card-details {
  list-style: none;
  padding: 0;
  margin: 0 0 12px;
  font-size: 0.9rem;
  color: #444;
}

.card-details li {
  margin-bottom: 4px;
}

.play-btn {
  align-self: flex-middle;
  padding: 8px 12px;
  background-color: #2e7d32;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.play-btn:hover {
  background-color: #27672a;
}
</style>