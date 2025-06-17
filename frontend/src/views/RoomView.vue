<template>
    <div class="clobber-room">
        <h2>Pokój: {{ code }}</h2>
        <div v-if="status === 'waiting'" class="waiting">
            Oczekiwanie na gracza…
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
            <span>Aktualny gracz:</span>
            <span class="current-player-circle" :class="current === myUsername ? myColor : opponentColor"></span>
            <template v-if="status === 'finished'">
                <span class="winner">🎉 {{ winner }} wygrał!</span>
            </template>
        </div>
        <button @click="leaveRoom" class="leave-button">
            Opuść pokój
        </button>
    </div>
</template>

<script>
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
            myColor: null,      // "white" or "black"
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
            const url = `ws://localhost:8000/ws/game/${this.code}/?token=${this.token}`;
            this.ws = new WebSocket(url);

            this.ws.onopen = () => {
                this.ws.send(JSON.stringify({ action: 'join' }));
            };

            this.ws.onmessage = ({ data }) => {
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

            // Determine your color once on first state: if you are host (first player) assume black,
            // else white.  If backend returns creator_color you could use that instead.
            if (!this.myColor) {
                // simple heuristic: if current === myUsername and board[0][0] === "_"?
                // (Better to have backend tell you, but we'll infer)
                this.myColor = msg.board[0][0] === 'b' ? 'black' : 'white';
            }

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
            const me = this.current === this.myUsername ?
                (this.myColor === 'white' ? 'w' : 'b') :
                (this.myColor === 'white' ? 'b' : 'w');

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
            // only your turn
            if (this.status !== 'playing' || this.current !== this.myUsername) return;

            const val = this.boardFlat[idx];
            if (this.selectedIdx === null) {
                // select your piece
                const mySym = this.myColor === 'white' ? 'w' : 'b';
                if (val === mySym) {
                    this.selectedIdx = idx;
                    this.legalMoves = this.calcLegalMoves(idx);
                }
            } else {
                // attempt move
                if (this.legalMoves.includes(idx)) {
                    const fromR = Math.floor(this.selectedIdx / this.cols);
                    const fromC = this.selectedIdx % this.cols;
                    const toR = Math.floor(idx / this.cols);
                    const toC = idx % this.cols;
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
        },
        async leaveRoom() {
            try {
                const res = await fetch('http://localhost:8000/rooms/leave/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${this.token}`
                    },
                    body: JSON.stringify({ code: this.code })
                });

                if (!res.ok) {
                    const error = await res.json();
                    throw new Error(error.detail || 'Błąd opuszczania pokoju.');
                }

                // Clean up WebSocket
                this.ws?.close();
                this.$router.push('/home');

            } catch (err) {
                console.error('Leave room error:', err.message);
                alert('Nie udało się opuścić pokoju: ' + err.message);
            }
        }
    },
    mounted() {
        this.connect();
    },
    beforeUnmount() {
        this.ws?.close();
    }
};
</script>

<style scoped>
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
</style>