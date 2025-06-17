<template>
    <div class="chat-container" v-if="visible">
        <div class="chat-header">
            <h3>{{ chatTitle }}</h3>
            <button @click="closeChat">✖</button>
        </div>
        <div class="chat-messages">
            <div v-for="(msg, idx) in messages" :key="idx"
                :class="['chat-message', { 'own': msg.user === myUsername }]">
                <div class="bubble">
                    <router-link :to="`/profile/${msg.user}`" class="chat-username">
                        {{ msg.user }}
                    </router-link>
                    <p class="text">{{ msg.message }}</p>
                </div>
            </div>
        </div>
        <div class="chat-input">
            <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
            <button @click="sendMessage">Send</button>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue';

export default {
    name: 'ChatComponent',
    props: {
        /**
         * roomId: when provided, connects to room chat in addition to global
         */
        roomId: {
            type: String,
            default: null,
        },
        /**
         * visible: controls showing/hiding chat container
         */
        visible: {
            type: Boolean,
            default: true,
        }
    },
    setup(props, { emit }) {
        const token = sessionStorage.getItem('token');
        console.log('Token:', token);
        const globalSocket = ref(null);
        const roomSocket = ref(null);
        const messages = ref([]);
        const newMessage = ref('');
        const myUsername = sessionStorage.getItem('username');
        const chatTitle = computed(() => props.roomId ? `Room: ${props.roomId}` : 'Global Chat');

        function connectGlobal() {
            const url = `ws://localhost:8000/ws/chat/global/?token=${token}`;
            globalSocket.value = new WebSocket(url);
            globalSocket.value.onmessage = event => {
                const data = JSON.parse(event.data);
                messages.value.push(data);
            };
            globalSocket.value.onopen = () => console.log('Global chat connected');
            globalSocket.value.onclose = () => console.log('Global chat disconnected');
        }

        function connectRoom(id) {
            if (roomSocket.value) {
                roomSocket.value.close();
                roomSocket.value = null;
            }
            if (!id) return;
            const url = `ws://localhost:8000/ws/chat/room/${id}/?token=${token}`;
            roomSocket.value = new WebSocket(url);
            roomSocket.value.onmessage = event => {
                const data = JSON.parse(event.data);
                messages.value.push(data);
            };
            roomSocket.value.onopen = () => console.log(`Room ${id} chat connected`);
            roomSocket.value.onclose = () => console.log(`Room ${id} chat disconnected`);
        }

        function sendMessage() {
            if (!newMessage.value.trim()) return;
            const payload = JSON.stringify({ message: newMessage.value });
            // send to room if in a room, else to global
            if (props.roomId && roomSocket.value && roomSocket.value.readyState === WebSocket.OPEN) {
                roomSocket.value.send(payload);
            } else if (globalSocket.value.readyState === WebSocket.OPEN) {
                globalSocket.value.send(payload);
            }
            newMessage.value = '';
        }

        function closeChat() {
            emit('update:visible', false);
        }

        onMounted(() => {
            connectGlobal();
            if (props.roomId) connectRoom(props.roomId);
        });

        onBeforeUnmount(() => {
            if (globalSocket.value) globalSocket.value.close();
            if (roomSocket.value) roomSocket.value.close();
        });

        watch(() => props.roomId, newId => {
            // clear messages and reconnect room
            messages.value = [];
            if (newId) {
                connectRoom(newId);
            } else if (roomSocket.value) {
                roomSocket.value.close();
                roomSocket.value = null;
            }
        });

        return {
            messages,
            newMessage,
            sendMessage,
            chatTitle,
            closeChat,
            connectGlobal,
            myUsername
        };
    }
};
</script>

<style scoped>
.chat-container {
    position: fixed;
    pointer-events: auto; /* this stupid bull makes routerview function correctly */
    bottom: 20px;
    right: 20px;
    width: 360px;
    height: 500px;
    background: white;
    border: 1px solid #ccc;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chat-header {
    flex: 0 0 auto;
    padding: 8px;
    background: #4caf50;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chat-messages {
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.chat-message {
    display: flex;
    width: 100%;
}

.chat-message.own {
    justify-content: flex-end;
}

.bubble {
    display: inline-block;
    max-width: 70%;
    padding: 8px 12px;
    border-radius: 16px;
    word-wrap: break-word;
}

.sender {
    display: block;
    font-weight: bold;
    margin-bottom: 4px;
    text-decoration: none;
    color: #2e7d32;
}

.sender:hover {
    text-decoration: underline;
}

.text {
    margin: 0;
}

.chat-message.own .bubble {
    background: #4caf50;
    color: white;
    border-bottom-right-radius: 4px;
}

.chat-message:not(.own) .bubble {
    background: #eee;
    color: #333;
    border-bottom-left-radius: 4px;
}

.chat-input {
    flex: 0 0 auto;
    padding: 8px;
    border-top: 1px solid #eee;
    display: flex;
    gap: 6px;
}

.chat-input input {
    flex: 1;
    padding: 6px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.chat-input button {
    padding: 6px 12px;
    background: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
}

.chat-input button:hover {
    background: #45a049;
}
</style>