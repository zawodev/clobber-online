<template>
  <div class="layout-wrapper" v-auto-animate>
    <header>
      <nav>
        <router-link :to="bttns ? '/home' : '/'"><img class="logo" src="@/assets/logo.png" /></router-link>
        <p v-if="bttns">Logged in {{ username }}</p>
        <div class="nav-links" v-if="bttns" v-auto-animate>
          <router-link to="/home" class="link">Home</router-link>
          <router-link to="/friends" class="link">Friends</router-link>
          <router-link to="/challenge" class="link">Challenges</router-link>
          <router-link :to="`/profile/${username}`" class="link">Profile</router-link>
        </div>
      </nav>
    </header>

    <main>
      <slot></slot>
    </main>

    <!-- Chat Icon -->
    <div v-auto-animate>
      <div class="chat-icon" v-if="bttns" @click="toggleChat">
        💬
      </div>

      <!-- Chat Popup -->
      <ChatComponent v-if="bttns" :visible="chatOpen" :roomId="currentRoomId" @update:visible="chatOpen = $event" />
    </div>
    <footer>
      <p>FututusDevelopment &copy; 2025</p>
    </footer>
  </div>
</template>

<script>
import ChatComponent from "@/components/Chat.vue";

export default {
  name: 'MainLayout',
  components: { ChatComponent },
  props: {
    bttns: Boolean,
  },
  data() {
    return {
      chatOpen: false,
      currentRoomId: null,
    };
  },
  computed: {
    username() {
      return sessionStorage.getItem("username");
    },
    token() {
      return sessionStorage.getItem("token");
    }
  },
  mounted() {

  },
  methods: {
    toggleChat() {
      this.token = sessionStorage.getItem("token");
      this.username = sessionStorage.getItem("username");
      this.chatOpen = !this.chatOpen;
    }
  }
}
</script>

<style scoped>
.layout-wrapper {
  position: relative;
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

nav a.link {
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

nav a.link:hover {
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

.logo {
  max-height: 50px;
}

.chat-icon {
  position: fixed;
  bottom: 60px;
  right: 20px;
  background-color: #4caf50;
  color: white;
  font-size: 24px;
  padding: 12px;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  transition: background 0.3s;
}

.chat-icon:hover {
  background-color: #45a049;
}

.chat-popup {
  position: fixed;
  bottom: 120px;
  right: 20px;
  width: 300px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 400px;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  background-color: #4caf50;
  color: white;
  padding: 10px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: #f9f9f9;
}

.chat-message {
  margin-bottom: 10px;
}

.chat-username {
  font-weight: bold;
  color: #2e7d32;
  text-decoration: none;
}

.chat-username:hover {
  text-decoration: underline;
}

.chat-input {
  display: flex;
  padding: 10px;
  background: #fff;
  border-top: 1px solid #ccc;
}

.chat-input input {
  flex: 1;
  padding: 8px;
  margin-right: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.chat-input button {
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
}

.chat-input button:hover {
  background-color: #45a049;
}
</style>