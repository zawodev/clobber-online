<template>
  <div class="challenges-view">
    <h2>Available Challenges</h2>
    <div class="challenges-list">
      <RoomMiniSolo
        v-for="challenge in challenges"
        :key="challenge.id"
        :id="challenge.id"
        :title="challenge.title"
        :description="challenge.description"
        :width="challenge.width"
        :height="challenge.height"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import RoomMiniSolo from '@/components/RoomMiniSolo.vue'

const challenges = ref([])

onMounted(async () => {
  try {
    const { data } = await api.get('/challenges/')
    // assume `data` is an array of { id, title, description, width, height, … }
    challenges.value = data
  } catch (err) {
    console.error('Failed to load challenges', err)
  }
})
</script>

<style scoped>
.challenges-view {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
}

.challenges-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}
</style>