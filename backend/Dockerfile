FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

USER root

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Dependencies (cache layer)
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ARG UID=1000
RUN useradd -m -u $UID appuser

COPY backend/ /app
# Создаем директории для логов и файлов, даем права записи
RUN mkdir -p /app/src/core/logs /app/src/infrastructure/files_work/files \
    && chown -R appuser:appuser /app/src/core/logs /app/src/infrastructure/files_work/files \
    && chmod -R 777 /app/src/core/logs /app/src/infrastructure/files_work/files \
    && chmod -R 777 /app/src/core/logs /app/src/infrastructure/files_work/files /app/src/infrastructure/db/migrations

# Copy entrypoint
COPY backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown appuser:appuser /entrypoint.sh

# Non-root user
USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
