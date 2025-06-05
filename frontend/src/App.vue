<template>
  <MainLayout :bttns="layoutComponent">
    <router-view />
  </MainLayout>
</template>

<script>
import MainLayout from '@/components/MainLayout.vue';

export default {
  name: 'App',
   computed: {
    layoutComponent() {
      const path = this.$route.path
      if (path === '/' || path === '/register') {
        return false // Brak layoutu
      } else {
        return true // Pokaż layout na innych stronach
      }
    }
  },
  components: {
    MainLayout
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
