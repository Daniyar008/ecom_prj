# ================================
# DOCKER DEPLOYMENT GUIDE
# ================================
# Инструкция по использованию Docker для развертывания проекта

## 📋 Оглавление
1. [Обзор архитектуры](#архитектура)
2. [Быстрый старт](#быстрый-старт)
3. [Подробная настройка](#подробная-настройка)
4. [Управление сервисами](#управление-сервисами)
5. [Масштабирование](#масштабирование)
6. [Production deployment](#production)
7. [Troubleshooting](#troubleshooting)

---

## 🏗️ Архитектура

Docker Compose запускает следующие сервисы:

```
┌─────────────────────────────────────────────────┐
│               Nginx (Port 80/443)               │
│          Reverse Proxy + Static Files           │
└────────────────────┬────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐    ┌────────▼────────┐
│  Django Web     │    │  Django Web     │
│   (Port 8000)   │    │   (Port 8001)   │
│  Gunicorn x4    │    │  Gunicorn x4    │
└────────┬────────┘    └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐    ┌────────▼────────┐
│  PostgreSQL     │    │     Redis       │
│   (Port 5432)   │    │   (Port 6379)   │
│  Database       │    │ Cache + Broker  │
└─────────────────┘    └────────┬────────┘
                                 │
                     ┌───────────┴───────────┐
                     │                       │
            ┌────────▼────────┐    ┌────────▼────────┐
            │  Celery Worker  │    │  Celery Beat    │
            │  Background     │    │  Scheduler      │
            └─────────────────┘    └─────────────────┘
```

---

## 🚀 Быстрый старт

### Шаг 1: Установка Docker

**Windows:**
```bash
# Скачайте Docker Desktop:
https://www.docker.com/products/docker-desktop
```

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
# Скачайте Docker Desktop:
https://www.docker.com/products/docker-desktop
```

### Шаг 2: Подготовка конфигурации

```bash
# 1. Создайте .env файл из примера
cp .env.example .env

# 2. Отредактируйте .env (измените пароли и секретные ключи!)
# Windows:
notepad .env

# Linux/macOS:
nano .env
```

### Шаг 3: Запуск

```bash
# Сборка и запуск всех сервисов
docker-compose up -d --build

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f web
```

### Шаг 4: Проверка

Откройте в браузере:
- **Frontend**: http://localhost
- **Admin**: http://localhost/admin
- **API**: http://localhost/api

---

## ⚙️ Подробная настройка

### Переменные окружения (.env)

Критические настройки:

```bash
# ОБЯЗАТЕЛЬНО измените в production:
SECRET_KEY=your-unique-secret-key-here-at-least-50-chars
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# База данных
DB_PASSWORD=very-secure-password-here

# Redis
REDIS_PASSWORD=another-secure-password-here

# Email (для production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Создание суперпользователя

```bash
# Способ 1: Автоматически через .env
# Добавьте в .env:
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=secure_password

# Пересоздайте контейнеры
docker-compose up -d --force-recreate web

# Способ 2: Вручную
docker-compose exec web python manage.py createsuperuser
```

### Миграции базы данных

```bash
# Создать новые миграции
docker-compose exec web python manage.py makemigrations

# Применить миграции
docker-compose exec web python manage.py migrate

# Просмотр миграций
docker-compose exec web python manage.py showmigrations
```

### Сбор статических файлов

```bash
# Собрать статику
docker-compose exec web python manage.py collectstatic --noinput

# Проверка
docker-compose exec web ls -la /app/staticfiles
```

---

## 🎮 Управление сервисами

### Базовые команды

```bash
# Запустить все сервисы
docker-compose up -d

# Остановить все сервисы
docker-compose down

# Перезапустить конкретный сервис
docker-compose restart web

# Просмотр логов
docker-compose logs -f          # Все сервисы
docker-compose logs -f web      # Только Django
docker-compose logs -f nginx    # Только Nginx

# Выполнение команд в контейнере
docker-compose exec web bash
docker-compose exec web python manage.py shell

# Проверка статуса
docker-compose ps
docker-compose top
```

### Очистка

```bash
# Остановить и удалить контейнеры (данные сохранятся)
docker-compose down

# Удалить контейнеры и volumes (ДАННЫЕ УДАЛЯТСЯ!)
docker-compose down -v

# Очистить все Docker ресурсы
docker system prune -a --volumes
```

---

## 📈 Масштабирование

### Горизонтальное масштабирование Django

```bash
# Запустить 3 экземпляра Django
docker-compose up -d --scale web=3

# Nginx автоматически будет балансировать нагрузку
```

### Увеличение воркеров Celery

```bash
# Запустить 3 Celery worker контейнера
docker-compose up -d --scale celery_worker=3
```

### Настройка Gunicorn (в Dockerfile или docker-compose)

```yaml
# docker-compose.yml - для web сервиса:
command: gunicorn ecomprj.wsgi:application 
  --bind 0.0.0.0:8000 
  --workers 8          # Увеличить количество воркеров
  --threads 4          # Увеличить количество потоков
  --worker-class gthread
  --timeout 120
```

---

## 🌍 Production Deployment

### Шаг 1: SSL сертификаты

```bash
# Создайте директорию для SSL
mkdir -p docker/nginx/ssl

# Способ 1: Let's Encrypt (бесплатно)
# Используйте Certbot:
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Скопируйте сертификаты
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem docker/nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem docker/nginx/ssl/

# Способ 2: Свой сертификат
# Положите файлы fullchain.pem и privkey.pem в docker/nginx/ssl/
```

### Шаг 2: Настройка Nginx для HTTPS

Отредактируйте `docker/nginx/nginx.conf`:

```nginx
# Замените
server_name yourdomain.com www.yourdomain.com;

# На ваш реальный домен
```

### Шаг 3: Security настройки в .env

```bash
# Production settings
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=generate-new-secret-key-here

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

### Шаг 4: Мониторинг

```bash
# Установите monitoring tools
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

### Шаг 5: Backup база данных

```bash
# Создать backup
docker-compose exec db pg_dump -U postgres ecomprj_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановить backup
docker-compose exec -T db psql -U postgres ecomprj_db < backup_file.sql
```

---

## 🔧 Troubleshooting

### Проблема: Контейнеры не запускаются

```bash
# Проверьте логи
docker-compose logs

# Проверьте конфигурацию
docker-compose config

# Пересоздайте контейнеры
docker-compose down
docker-compose up -d --build --force-recreate
```

### Проблема: База данных не подключается

```bash
# Проверьте доступность PostgreSQL
docker-compose exec web nc -zv db 5432

# Проверьте переменные окружения
docker-compose exec web env | grep DB_

# Проверьте логи PostgreSQL
docker-compose logs db
```

### Проблема: Статические файлы не отдаются

```bash
# Пересоберите статику
docker-compose exec web python manage.py collectstatic --noinput --clear

# Проверьте права
docker-compose exec web ls -la /app/staticfiles

# Перезапустите nginx
docker-compose restart nginx
```

### Проблема: Redis не работает

```bash
# Проверьте статус Redis
docker-compose exec redis redis-cli ping

# С паролем
docker-compose exec redis redis-cli -a your_redis_password ping

# Проверьте подключение из Django
docker-compose exec web python -c "
import django
django.setup()
from django.core.cache import cache
cache.set('test', 'works')
print(cache.get('test'))
"
```

### Проблема: Celery не обрабатывает задачи

```bash
# Проверьте логи Celery
docker-compose logs -f celery_worker

# Проверьте очередь задач
docker-compose exec celery_worker celery -A ecomprj inspect active

# Перезапустите worker
docker-compose restart celery_worker
```

---

## 📊 Мониторинг

### Проверка здоровья контейнеров

```bash
# Статус всех контейнеров
docker-compose ps

# Health check
docker-compose exec web curl -f http://localhost:8000/health/
```

### Потребление ресурсов

```bash
# Статистика контейнеров
docker stats

# Использование дискового пространства
docker system df
```

### Просмотр логов

```bash
# Все логи
docker-compose logs --tail=100 -f

# Логи конкретного сервиса
docker-compose logs -f web nginx db

# Поиск ошибок
docker-compose logs | grep ERROR
```

---

## 🔐 Security Best Practices

1. **Никогда не используйте дефолтные пароли в production**
2. **Храните .env в .gitignore**
3. **Используйте HTTPS в production**
4. **Регулярно обновляйте Docker образы**
5. **Ограничьте доступ к портам (только через nginx)**
6. **Используйте secrets для чувствительных данных**

---

## 📚 Дополнительные ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [Redis Docker Hub](https://hub.docker.com/_/redis)

---

## 💡 Команды для быстрого доступа

```bash
# Алиасы (добавьте в .bashrc или .zshrc)
alias dc='docker-compose'
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'
alias dclogs='docker-compose logs -f'
alias dcps='docker-compose ps'
alias dcrestart='docker-compose restart'
alias dcweb='docker-compose exec web'
alias dcdb='docker-compose exec db psql -U postgres ecomprj_db'
```

---

**Примечание**: Этот Docker setup создан для демонстрации и может использоваться как шаблон. В текущем проекте используется Render.com deployment без Docker.
