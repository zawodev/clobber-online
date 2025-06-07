# używamy obrazu python slim
FROM python:3.11-slim

# ustawiamy katalog roboczy
WORKDIR /app

# zainstaluj zależności systemowe (pip, build tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# kopiujemy requirements.txt i instalujemy zależności do pythona
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# kopiujemy resztę kodu
COPY . .

# zbieranie statycznych plików (CSS, JS, obrazy) - pewnie nie potrzebne ale d=_=b
RUN python manage.py collectstatic --noinput

# expose port
EXPOSE 8000

# komenda uruchamiająca aplikację (daphne obsługuje ASGI + WS czego nie można powiedzieć o domyślnym serwerze django)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
