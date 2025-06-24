<template>
  <MainLayout :bttns="layoutComponent">
    <router-view :key="$route.fullPath" />
  </MainLayout>
</template>

<script>
import MainLayout from '@/components/MainLayout.vue';

export default {
  name: 'App',
   computed: {
    layoutComponent() {
      const p = this.$route.path.replace(/\/$/, '')
      if (p === '' || p === '/' || p === '/register' || p === '/auth-callback') {
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
}
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}
main, header, nav {
  margin: 0;
  padding: 0;
}
</style>
