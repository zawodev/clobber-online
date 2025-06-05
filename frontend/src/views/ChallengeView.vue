
<template>
  <div class="home-container">
    <h2>Daily Challenges</h2>
    <div class="cards-grid">
      <!-- Dla każdego obiektu w challenges renderujemy ChallengeCard -->
      <RoomMiniSolo
        v-for="challenge in challenges"
        :key="challenge.id"
        :title="challenge.title"
        :points="challenge.points"
        :difficulty="challenge.difficulty"
        :boardSize="challenge.boardSize"
        :timeLimit="challenge.timeLimit"
        @play="handlePlay"
      />
    </div>
  </div>
</template>

<script>
import RoomMiniSolo from '@/components/RoomMiniSolo.vue';

export default {
  name: 'ChallengeView',
  components: { RoomMiniSolo },
  data() {
    return {
      // PRZYKŁADOWE DANE – w docelowej wersji podmienisz je na fetch z API
      challenges: [
        {
          id: 1,
          title: 'Win with AI',
          points: 30,
          difficulty: 'hard',
          boardSize: '5x6',
          timeLimit: 'Bullet +3'
        },
        {
          id: 2,
          title: 'Win with AI',
          points: 10,
          difficulty: 'easy',
          boardSize: '5x6',
          timeLimit: 'Bullet +3'
        },
        {
          id: 3,
          title: 'Win with AI',
          points: 30,
          difficulty: 'hard',
          boardSize: '5x6',
          timeLimit: 'Bullet +3'
        },
        {
          id: 4,
          title: 'Win with AI',
          points: 10,
          difficulty: 'easy',
          boardSize: '5x6',
          timeLimit: 'Bullet +3'
        }
        // …możesz ich mieć dowolnie wiele
      ]
    };
  },
  methods: {
    handlePlay(payload) {
      // payload = { title: 'Win with AI', points: 30 }
      console.log('Użytkownik kliknął „Play” na wyzwanie:', payload);
    }
  }
};
</script>

<style scoped>
.home-container {
  padding: 16px;
}

h2 {
  margin-bottom: 12px;
  color: #2e7d32;
}

.cards-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
</style>