<template>
  <div class="challenge-card">
    <div class="card-header">
      <span class="points">{{ points }} points</span>
      <h3 class="title">{{ title }}</h3>
    </div>
    <ul class="card-details">
      <li><strong>Difficulty:</strong> {{ difficulty }}</li>
      <li><strong>Board size:</strong> {{ boardSize }}</li>
      <li><strong>Time limit:</strong> {{ timeLimit }}</li>
    </ul>
    <button class="play-btn" @click="onPlay">Play</button>
  </div>
</template>

<script>
export default {
  name: 'RoomMiniSolo',
  props: {
    title: {
      type: String,
      required: true
    },
    points: {
      type: Number,
      required: true
    },
    difficulty: {
      type: String,
      required: true
    },
    boardSize: {
      type: String,
      required: true
    },
    timeLimit: {
      type: String,
      required: true
    }
  },
  methods: {
    onPlay() {
      // Tutaj możesz emitować event wybranego wyzwania, np. do routera lub rodzica:
      this.$emit('play', { title: this.title, points: this.points });
    }
  }
}
</script>

<style scoped>
.challenge-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  padding: 16px;
  width: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 8px;
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