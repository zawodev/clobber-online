# Clobber Online

Aplikacja webowa do gry w Clobber online z personalnym czatem z naszym przeciwnikiem, dziennymi wyzwaniami oraz systemem logowania i rejestracji.

## Funkcjonalności

- **Gra wieloosobowa**: Rozgrywka w Clobber w trybie PvP.
- **Czat na żywo**: Wbudowany czat umożliwiający komunikację podczas rozgrywki.
- **Daily Challenge**: Codzienne wyzwania z różnymi nagrodami.
- **Użytkownicy**: Rejestracja, logowanie, zarządzanie profilem, statystyki (wygrane, przegrane, rankingi).

## Technologie

- Frontend: Vue
- Backend: Django
- Baza danych: SQLite

- WebSocket: Socket.io (do czatu i synchronizacji gry)

## Uruchomienie lokalne

Wymagany jest Docker i Docker Compose
1. Utwórz lokalną konfigurację:
	```bash
	cp .env.example .env
	```

2. Uruchom backend, Redis i frontend:
	```bash
	docker compose up --build
	```

3. Otwórz aplikację pod adresem:
   ```
   http://localhost
   ```




