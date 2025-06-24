<template>
    <div class="clobber-room-container">
        <div class="clobber-room">
            <h2>Room code: {{ code }}</h2>
            <div v-if="status === 'waiting'" class="waiting">
                Waiting for second player...
            </div>
            <div v-else class="board" :style="{
                gridTemplateColumns: `repeat(${cols}, ${tileSize}px)`,
                width: `${cols * tileSize}px`,
                height: `${rows * tileSize}px`
            }">
                <div v-for="(cell, idx) in boardFlat" :key="idx" class="cell" :class="{
                    'cell--light': isLight(idx),
                    'cell--dark': !isLight(idx),
                    'cell--selected': idx === selectedIdx,
                    'cell--legal': legalMoves.includes(idx)
                }" @click="onCellClick(idx)">
                    <transition name="fade">
                        <div v-if="cell !== '_'" class="piece" :class="cell === 'w' ? 'white' : 'black'"></div>
                    </transition>
                </div>
            </div>
            <div class="info-bar" v-if="status !== 'waiting'">
                <span>Current Player:</span>
                <span class="current-player-circle" :class="current"></span>
                <span>Your colour:</span>
                <span class="current-player-circle" :class="myColor"></span>
                <template v-if="status === 'finished'">
                    <span class="winner">🎉 {{ winner || 'Clobber-bot' }} won!</span>
                </template>
            </div>
            <button @click="leaveRoom" class="leave-button">Leave room</button>
        </div>

        <!-- CHAT PANE -->
        <div class="chat-pane">
            <h3>Send a message to your opponent.</h3>
            <div class="messages">
                <div v-for="(msg, i) in chatMessages" :key="i"
                    :class="['message', msg.user === myUsername ? 'mine' : 'theirs']">
                    <div class="bubble">
                        <small class="sender">{{ msg.user }}</small>
                        <p>{{ msg.message }}</p>
                    </div>
                </div>
            </div>
            <div class="chat-input">
                <input v-model="chatInput" @keyup.enter="sendChat" placeholder="Napisz wiadomość…" />
                <button @click="sendChat">Wyślij</button>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/api'
export default {
    name: 'RoomView',
    data() {
        return {
            code: this.$route.params.code,
            token: sessionStorage.getItem('token'),
            ws: null,
            board: [],          // 2D array of "_", "w", "b"
            rows: 0,
            cols: 0,
            current: null,      // username whose turn it is
            status: null,       // 'waiting' | 'playing' | 'finished'
            winner: null,
            selectedIdx: null,
            legalMoves: [],
            tileSize: 60,
            myUsername: sessionStorage.getItem('username'),
            // track which color YOU are:
            myColor: this.$route.query.color,      // "white" or "black"
            chatWs: null,
            chatMessages: [],           // { username, message }
            chatInput: ''
        };
    },
    computed: {
        boardFlat() {
            return this.board.flat();
        },
        opponentColor() {
            return this.myColor === 'white' ? 'black' : 'white';
        }
    },
    methods: {
        connect() {
            const url = `${process.env.VUE_APP_WSROOM}/${this.code}/?token=${this.token}`;
            this.ws = new WebSocket(url);

            this.ws.onopen = () => {
                this.ws.send(JSON.stringify({ action: 'join' }));
            };

            this.ws.onmessage = ({ data }) => {
                console.log('⟵ WS raw message:', event.data);

                const msg = JSON.parse(data);
                if (msg.type === 'state') {
                    this.applyState(msg);
                }
            };
        },

        applyState(msg) {
            this.board = msg.board;
            this.rows = msg.board.length;
            this.cols = msg.board[0]?.length || 0;
            this.current = msg.current;
            this.status = msg.status;
            this.winner = msg.winner;


            // reset selection and legal moves
            this.selectedIdx = null;
            this.legalMoves = [];
        },

        isLight(idx) {
            const r = Math.floor(idx / this.cols);
            const c = idx % this.cols;
            return (r + c) % 2 === 0;
        },

        calcLegalMoves(srcIdx) {
            const moves = [];
            const r0 = Math.floor(srcIdx / this.cols);
            const c0 = srcIdx % this.cols;
            const dirs = [
                [-1, 0], [1, 0], [0, -1], [0, 1]
            ];
            const me = this.myColor === 'white' ? 'w' : 'b';

            for (const [dr, dc] of dirs) {
                const nr = r0 + dr, nc = c0 + dc;
                if (nr < 0 || nr >= this.rows || nc < 0 || nc >= this.cols) continue;
                const occ = this.board[nr][nc];
                if (occ !== '_' && occ !== me) {
                    moves.push(nr * this.cols + nc);
                }
            }
            return moves;
        },

        onCellClick(idx) {
            // tylko jeśli trwa gra i jest tura użytkownika
            if (this.status !== 'playing' || this.current !== this.myColor) return;

            const mySymbol = this.myColor === 'white' ? 'w' : 'b';
            const val = this.boardFlat[idx];
            console.log("bruh")
            if (this.selectedIdx === null) {
                // Wybór pionka należącego do gracza
                if (val === mySymbol) {
                    this.selectedIdx = idx;
                    this.legalMoves = this.calcLegalMoves(idx);
                }
            } else {
                // Próba wykonania ruchu
                if (this.legalMoves.includes(idx)) {
                    const fromR = Math.floor(this.selectedIdx / this.cols);
                    const fromC = this.selectedIdx % this.cols;
                    const toR = Math.floor(idx / this.cols);
                    const toC = idx % this.cols;
                    console.log(fromR + ' , ' + fromC + " to " + toR + " , " + toC);
                    console.log("sending");
                    this.sendMove([fromR, fromC], [toR, toC]);
                }
                this.selectedIdx = null;
                this.legalMoves = [];
            }
        },

        sendMove(fromArr, toArr) {
            if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;
            this.ws.send(JSON.stringify({
                action: 'move',
                from: fromArr,
                to: toArr
            }));
            console.log("sent")
        },
        connectChat() {
            const chatUrl =
                `${process.env.VUE_APP_WSROOMCHAT}/${this.code}/?token=${this.token}`
            this.chatWs = new WebSocket(chatUrl)
            this.chatWs.onmessage = ({ data }) => {
                const { user, message } = JSON.parse(data)
                this.chatMessages.push({ user, message })
                this.$nextTick(() => {
                    const container = this.$el.querySelector('.messages')
                    container.scrollTop = container.scrollHeight
                })
            }
        },
        sendChat() {
            const text = this.chatInput.trim()
            if (!text || this.chatWs?.readyState !== WebSocket.OPEN) return
            this.chatWs.send(JSON.stringify({ message: text }))
            this.chatInput = ''
        },
        async leaveRoom() {
            try {
                const token = sessionStorage.getItem('token');
                if (token) {
                    api.defaults.headers.common['Authorization'] = `Token ${token}`;
                }

                await api.post('/rooms/leave/', {
                    code: this.code
                });

                // Clean up WebSocket connection
                this.ws?.close();
                this.chatWs?.close()
                // Navigate away
                this.$router.push('/home');

            } catch (err) {
                console.error('Leave room error:', err.response?.data || err.message);
                const msg = err.response?.data?.detail || 'Nie udało się opuścić pokoju.';
                alert(msg);
            }
        }
    },
    mounted() {
        this.connect();
        this.connectChat()
    },
    beforeUnmount() {
        this.ws?.close();
        this.chatWs?.close()
    }
};
</script>

<style scoped>
.clobber-room-container {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    gap: 16px;
    padding: 20px;
}

.clobber-room {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 20px;
}

.board {
    display: grid;
    border: 2px solid #555;
}

.cell {
    position: relative;
    cursor: pointer;
    box-sizing: border-box;
}

.cell--light {
    background-color: #d8e2dc;
}

.cell--dark {
    background-color: #84a59d;
}

.cell--selected {
    outline: 3px solid #f2cc8f;
}

.cell--legal {
    box-shadow: inset 0 0 0 3px #f28482;
}

.piece {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 70%;
    height: 70%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
}

.piece.white {
    background-color: #fff;
    border: 2px solid #aaa;
}

.piece.black {
    background-color: #333;
    border: 2px solid #111;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.info-bar {
    margin-top: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.current-player-circle {
    display: inline-block;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 2px solid #555;
}

.current-player-circle.white {
    background-color: #fff;
}

.current-player-circle.black {
    background-color: #333;
}

.waiting {
    margin: 20px;
    font-style: italic;
    color: #666;
}

.winner {
    margin-left: 16px;
    font-weight: bold;
    color: #4caf50;
}

.leave-button {
    margin: 16px 0;
    padding: 8px 16px;
    background: #f28482;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.leave-button:hover {
    background: #e76f6f;
}

.chat-pane {
    width: 300px;
    display: flex;
    flex-direction: column;
    height: 400px;
    border: 1px solid #ccc;
    border-radius: 6px;
    overflow: hidden;
}

.chat-pane h3 {
    margin: 0;
    padding: 8px;
    background: #f5f5f5;
    border-bottom: 1px solid #ddd;
}

.messages {
    flex: 1;
    padding: 3px;
    overflow-y: auto;
    background: #fafafa;
}

.message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 4px;
}

.message.mine {
    justify-content: flex-end;
}

.message.theirs {
    justify-content: flex-start;
}

.bubble {
    width: 55%;
    max-width: 80%;
    padding: 3px 3px;
    border-radius: 12px;
    background: #e0e0e0;
    position: relative;
    display: inline-block;
    line-height: 1;
}

.message.mine .bubble {
    background: #a5d6a7;
}

.sender {
    display: block;
    font-size: 0.7rem;
    color: #555;
    margin-bottom: 2px;
}

.chat-input {
    display: flex;
    border-top: 1px solid #ddd;
}

.chat-input input {
    flex: 1;
    border: none;
    padding: 8px;
    font-size: 0.9rem;
}

.chat-input input:focus {
    outline: none;
}

.chat-input button {
    border: none;
    background: #2e7d32;
    color: white;
    padding: 0 16px;
    cursor: pointer;
}

.chat-input button:hover {
    background: #27672a;
}
</style>