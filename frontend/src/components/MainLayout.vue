<template>
  <div class="layout-wrapper">
    <header>
      <nav>
        <img class="logo" src="@/assets/logo.png" />
        <p v-if="bttns">Zalogowany jako {{ username }}</p>
        <div class="nav-links" v-if="bttns">
          <router-link to="/home">Home</router-link>
          <router-link to="/friends">Friends</router-link>
          <router-link to="/challenge">Challenges</router-link>
          <router-link :to="`/profile/${username}`">Profile</router-link>
        </div>
      </nav>
    </header>

    <main>
      <slot></slot>
    </main>

    <!-- Chat Icon -->
    <div class="chat-icon" v-if="bttns" @click="toggleChat">
      💬
    </div>

    <!-- Chat Popup -->
    <div v-if="chatOpen" class="chat-popup">
      <div class="chat-header">
        <h3>Global Chat</h3>
        <button @click="toggleChat">✖</button>
      </div>
      <div class="chat-messages">
        <div v-for="(msg, index) in messages" :key="index" class="chat-message">
          <router-link :to="`/profile/${msg.username}`" class="chat-username">
            {{ msg.username }}
          </router-link>
          <p>{{ msg.text }}</p>
        </div>
      </div>
      <div class="chat-input">
        <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
        <button @click="sendMessage">Send</button>
      </div>
    </div>

    <footer>
      <p>FututusDevelopment &copy; 2025</p>
    </footer>
  </div>
</template>

<script>
import { connectToChat, sendMessage, isSocketConnected } from "@/websocket";

export default {
  name: 'MainLayout',
  props: {
    bttns: Boolean,
  },
  data() {
    return {
      chatOpen: false,
      messages: [],
      newMessage: "",
    };
  },
  computed: {
    username() {
      return localStorage.getItem("username");
    },
    token() {
      return localStorage.getItem("token");
    }
  },
  mounted() {
    // Only attach listener if connected
    if (this.token && isSocketConnected()) {
      connectToChat(this.token, this.onSocketMessage);
    }
  },
  methods: {
    toggleChat() {
      this.chatOpen = !this.chatOpen;
    },
    onSocketMessage(data) {
      this.messages.push({
        username: data.username,
        text: data.message,
      });
    },
    sendMessage() {
      if (this.newMessage.trim()) {
        sendMessage({ message: this.newMessage });
        this.newMessage = "";
      }
    }
  }
}
</script>

<style scoped>
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