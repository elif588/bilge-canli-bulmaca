FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    SDL_AUDIODRIVER=dummy \
    PORT=8765

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-mixer-2.0-0 \
    libsdl2-2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8765

CMD ["python", "-u", "run.py"]
