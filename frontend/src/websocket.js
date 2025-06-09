// src/services/chatSocket.js
let socket = null;

export function connectToChat(token, onMessage) {
  if (socket) return socket;

  const url = `ws://localhost:8000/ws/chat/global/?token=${token}`;
  socket = new WebSocket(url);

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.username && data.message) {
        onMessage({
          username: data.username,
          message: data.message,
        });
      }
    } catch (err) {
      console.error("WebSocket message error:", err);
    }
  };

  socket.onclose = () => {
    console.warn("WebSocket closed.");
    socket = null;
  };

  return socket;
}

export function sendMessage(messageData) {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ message: messageData.message }));
  }
}

export function isSocketConnected() {
  return socket && socket.readyState === WebSocket.OPEN;
}

export function getSocketInstance() {
  return socket;
}

// NEW: Allow global init (without duplicating listeners)
export function initSocketAfterLogin() {
  const token = localStorage.getItem("token");
  if (!token || isSocketConnected()) return;

  connectToChat(token, (data) => {
    console.log("Global chat message received:", data);
    // This callback will only print — UI won't receive these unless manually passed later.
  });
}