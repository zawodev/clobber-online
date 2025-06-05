<template>
  <div class="clobber-game">
    <div
      class="board"
      :style="{
        gridTemplateColumns: `repeat(${cols}, ${tileSize}px)`,
        width: `${cols * tileSize}px`,
        height: `${rows * tileSize}px`
      }"
    >
      <div
        v-for="(cell, idx) in boardFlat"
        :key="idx"
        class="cell"
        :class="{
          'cell--light': isLight(idx),
          'cell--dark': !isLight(idx),
          'cell--selected': idx === selectedIdx,
          'cell--legal': legalMoves.includes(idx)
        }"
        @click="onCellClick(idx)"
      >
        <transition name="fade">
          <div
            v-if="cell"
            class="piece"
            :class="cell"
          ></div>
        </transition>
      </div>
    </div>

    <div class="info-bar">
      <span>Aktualny gracz:</span>
      <span
        class="current-player-circle"
        :class="currentPlayer"
      ></span>
      <button class="reset-btn" @click="resetGame">Restartuj</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClobberGame',

  props: { // params - can make diff boads
    rows: {
      type: Number,
      default: 6
    },
    cols: {
      type: Number,
      default: 8
    },
    tileSize: {
      type: Number,
      default: 60
    }
  },

  data() {
    return {
      //board rep
      board: [],

      // piece selected
      selectedIdx: null,

      // we calc legal moves to not overload backend
      legalMoves: [],

      currentPlayer: 'white' // might not be corect with backend - idk if matters
    };
  },

  computed: {
    boardFlat() {
      return this.board.flat();
    }
  },

  methods: {
    // (r+c)%2 → biały / czarny
    initBoard() {
      const newBoard = [];
      for (let r = 0; r < this.rows; r++) {
        const rowArr = [];
        for (let c = 0; c < this.cols; c++) {
          rowArr.push((r + c) % 2 === 0 ? 'white' : 'black');
        }
        newBoard.push(rowArr);
      }
      this.board = newBoard;
      this.selectedIdx = null;
      this.legalMoves = [];
      this.currentPlayer = 'white';
    },


    isLight(idx) {
      const r = Math.floor(idx / this.cols);
      const c = idx % this.cols;
      return (r + c) % 2 === 0;
    },

    calcLegalMoves(sourceIdx) {
      const moves = [];
      const r0 = Math.floor(sourceIdx / this.cols);
      const c0 = sourceIdx % this.cols;
      const dirs = [
        [-1, 0], // góra
        [1, 0],  // dół
        [0, -1], // lewo
        [0, 1]   // prawo
      ];

      for (const [dr, dc] of dirs) {
        const nr = r0 + dr;
        const nc = c0 + dc;
        if (nr < 0 || nr >= this.rows || nc < 0 || nc >= this.cols) continue;

        const occupant = this.board[nr][nc]; // null / 'white' / 'black'
        if (occupant && occupant !== this.currentPlayer) {
          moves.push(nr * this.cols + nc);
        }
      }
      return moves;
    },

    onCellClick(idx) {
      const clickedValue = this.boardFlat[idx]; // null / 'white' / 'black'

      if (this.selectedIdx === null) {
        
        if (clickedValue === this.currentPlayer) {
          this.selectedIdx = idx;
          this.legalMoves = this.calcLegalMoves(idx);
        }
        return;
      }

      // 2) Gdy już mamy selectedIdx, sprawdzamy, czy kliknięcie jest na legalnym celu:
      if (this.legalMoves.includes(idx)) {
        this.performMove(this.selectedIdx, idx);
        // tutaj wysyłanie do api
        this.selectedIdx = null;
        this.legalMoves = [];
        this.currentPlayer = this.currentPlayer === 'white' ? 'black' : 'white';
        return;
      }

      // clicked on other piece
      if (clickedValue === this.currentPlayer) {
        this.selectedIdx = idx;
        this.legalMoves = this.calcLegalMoves(idx);
      } else {
        this.selectedIdx = null;
        this.legalMoves = [];
      }
    },

    performMove(sourceIdx, targetIdx) {
    const movingPlayer = this.currentPlayer;//timeout switches players

      const r0 = Math.floor(sourceIdx / this.cols);
      const c0 = sourceIdx % this.cols;
      const rt = Math.floor(targetIdx / this.cols);
      const ct = targetIdx % this.cols;

      this.board[rt][ct] = null;

      setTimeout(() => {
        this.board[rt][ct] = movingPlayer;
      }, 150);

  
      this.board[r0][c0] = null;
    },

    resetGame() {
      this.initBoard();
    }
  },

  mounted() {
    this.initBoard();
  }
};
</script>

<style scoped>
.clobber-game {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}
.board {
  display: grid;
  border: 2px solid #555;
}


.cell {
  position: relative;
  width: 100%;
  height: 100%;
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
  box-shadow: 0 0 4px rgba(0,0,0,0.3);
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
  font-family: Arial, sans-serif;
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

.reset-btn {
  padding: 6px 12px;
  background-color: #f28482;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
}
.reset-btn:hover {
  background-color: #f1a9a0;
}
</style>