<template>
  <div class="layout-wrapper">
    <header>
      <nav>
        <img class="logo" src="@/assets/logo.png"/>
        <p v-if="bttns"> Zalogowany jako {{ username }}</p>
        <div class="nav-links" v-if="bttns" >
          <router-link to="/home">Home</router-link>
          <router-link to="/friends">Friends</router-link>
          <router-link to="/challenge">Challenges</router-link>
          <router-link to="/profile">Profile</router-link>
        </div>
      </nav>
    </header>
    <main>
      <slot></slot>
    </main>
    <footer>
      <p>FututusDevelopment &copy; 2025</p>
    </footer>
  </div>
</template>

<script>
export default {
    name: 'MainLayout',
    props: {
      bttns: Boolean,
  },
  computed: {
  username() {
    return localStorage.getItem("username")
  }
}
}
</script>

<style>
.layout-wrapper {
  position: fixed;
  top: 0;
  width: 100vw;  
  color: #2e7d32;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
header {
  background: #f0f0f0;
}
nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
}
.nav-links {
  display: flex;
  gap: 20px;
}
nav a {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  padding: 10px 16px;
  border-radius: 6px;
  transition: background-color 0.3s;
  text-align: center;
}
nav a:hover {
  background-color: #45a049;
}
main {
  flex: 1;
  padding: 20px;
}
footer {
  text-align: center;
  padding: 15px;
  background: #eee;
  color: #666;
  font-size: 0.9em;
}
.logo{
   max-height: 50px;
}
</style>