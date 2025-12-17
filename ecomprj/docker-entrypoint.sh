#!/bin/bash

# ================================
# Docker Entrypoint для Django
# ================================

set -e  # Остановка при ошибке

echo "🚀 Starting Django application..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для ожидания доступности PostgreSQL
wait_for_db() {
    echo -e "${YELLOW}⏳ Waiting for PostgreSQL...${NC}"
    
    while ! nc -z $DB_HOST $DB_PORT; do
        echo -e "${YELLOW}PostgreSQL is unavailable - sleeping${NC}"
        sleep 1
    done
    
    echo -e "${GREEN}✅ PostgreSQL is up!${NC}"
}

# Функция для ожидания доступности Redis
wait_for_redis() {
    if [ ! -z "$REDIS_URL" ]; then
        echo -e "${YELLOW}⏳ Waiting for Redis...${NC}"
        
        REDIS_HOST=$(echo $REDIS_URL | sed -n 's/.*\/\/\([^:]*\).*/\1/p')
        REDIS_PORT=$(echo $REDIS_URL | sed -n 's/.*:\([0-9]*\).*/\1/p')
        
        while ! nc -z $REDIS_HOST ${REDIS_PORT:-6379}; do
            echo -e "${YELLOW}Redis is unavailable - sleeping${NC}"
            sleep 1
        done
        
        echo -e "${GREEN}✅ Redis is up!${NC}"
    fi
}

# Ожидание баз данных
if [ ! -z "$DB_HOST" ] && [ ! -z "$DB_PORT" ]; then
    wait_for_db
fi

wait_for_redis

# Применяем миграции
echo -e "${YELLOW}📦 Running database migrations...${NC}"
python manage.py migrate --noinput || {
    echo -e "${RED}❌ Migrations failed!${NC}"
    exit 1
}
echo -e "${GREEN}✅ Migrations completed!${NC}"

# Собираем статику
echo -e "${YELLOW}🎨 Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear || {
    echo -e "${RED}❌ Static collection failed!${NC}"
    exit 1
}
echo -e "${GREEN}✅ Static files collected!${NC}"

# Создаем суперпользователя (если нужно)
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo -e "${YELLOW}👤 Creating superuser...${NC}"
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created!')
else:
    print('Superuser already exists.')
END
    echo -e "${GREEN}✅ Superuser check completed!${NC}"
fi

# Запуск Celery worker в фоне (если нужен)
if [ "$START_CELERY_WORKER" = "true" ]; then
    echo -e "${YELLOW}🔧 Starting Celery worker...${NC}"
    celery -A ecomprj worker -l info &
    echo -e "${GREEN}✅ Celery worker started!${NC}"
fi

# Запуск Celery beat в фоне (если нужен)
if [ "$START_CELERY_BEAT" = "true" ]; then
    echo -e "${YELLOW}⏰ Starting Celery beat...${NC}"
    celery -A ecomprj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
    echo -e "${GREEN}✅ Celery beat started!${NC}"
fi

echo -e "${GREEN}✨ Django application is ready!${NC}"
echo -e "${GREEN}🌐 Starting server...${NC}"

# Запуск команды (gunicorn, runserver и т.д.)
exec "$@"
