# ================================
# Multi-stage Docker build для Django
# ================================

# Stage 1: Builder (сборка зависимостей)
FROM python:3.11-slim as builder

# Устанавливаем системные зависимости для компиляции пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем только requirements для кеширования слоя
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime (финальный образ)
FROM python:3.11-slim

# Метаданные
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="Django E-commerce Multivendor Platform"

# Аргументы для build-time переменных
ARG DJANGO_ENV=production
ENV DJANGO_ENV=${DJANGO_ENV}

# Устанавливаем runtime зависимости
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для запуска (НЕ root!)
RUN groupadd -r django && useradd -r -g django django

# Копируем виртуальное окружение из builder
COPY --from=builder /opt/venv /opt/venv

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем код проекта
COPY --chown=django:django . .

# Создаем необходимые директории
RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chown -R django:django /app

# Активируем виртуальное окружение
ENV PATH="/opt/venv/bin:$PATH"

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=ecomprj.settings \
    PORT=8000

# Собираем статику (если нужно при билде)
# RUN python manage.py collectstatic --noinput || true

# Копируем entrypoint скрипт
COPY --chown=django:django docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Переключаемся на непривилегированного пользователя
USER django

# Открываем порт
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Запуск через entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["gunicorn", "ecomprj.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
