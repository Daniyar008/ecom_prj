# ОТЧЕТ ПО УЧЕБНОЙ ПРАКТИКЕ

---

## ТИТУЛЬНЫЙ ЛИСТ

**Тема:** Разработка и развертывание многовендорной платформы электронной коммерции с использованием контейнеризации

**Выполнили:**
- Султангереев Данияр
- Ауданғалиев Нұрислам

**Период практики:** 21.11.2025 – 22.12.2025

**Технологии:** Python, Django, PostgreSQL, Redis, Docker, Nginx, Kubernetes

**Рабочий сайт:** https://multivendor-shop-iz5t.onrender.com

**GitHub:** https://github.com/Daniyar008/ecom_prj

---

## СОДЕРЖАНИЕ

1. Введение
2. Анализ предметной области
3. Обоснование выбора технологий
4. Архитектура системы
5. Структура базы данных
6. Контейнеризация (Docker)
7. Оркестрация (Kubernetes)
8. Веб-сервер (Nginx)
9. Функциональность системы
10. Проблемы и их решения
11. Тестирование
12. Заключение
13. Список литературы
14. Приложения

---

## 1. ВВЕДЕНИЕ

### 1.1 Цель практики

Систематизировать знания в области веб-разработки, архитектуры информационных систем и DevOps на примере создания многовендорной e-commerce платформы. Изучить и применить принципы контейнеризации, оркестрации и современные подходы к развертыванию.

### 1.2 Задачи практики

| № | Задача | Тип |
|---|--------|-----|
| 1 | Проанализировать существующие маркетплейсы (Ozon, Wildberries) | Аналитическая |
| 2 | Изучить и сравнить фреймворки (Django, Flask, FastAPI) | Исследовательская |
| 3 | Спроектировать архитектуру и базу данных | Проектная |
| 4 | Реализовать backend и frontend | Практическая |
| 5 | Контейнеризировать приложение (Docker) | DevOps |
| 6 | Настроить оркестрацию (Kubernetes) | DevOps |
| 7 | Развернуть в production с Nginx | Практическая |

### 1.3 Объект и предмет исследования

**Объект:** Многовендорные электронные коммерческие платформы

**Предмет:** Принципы проектирования, контейнеризации и развертывания веб-приложений

---

## 2. АНАЛИЗ ПРЕДМЕТНОЙ ОБЛАСТИ

### 2.1 Исследование существующих решений

| Платформа | Сильные стороны | Слабые стороны |
|-----------|-----------------|----------------|
| **Ozon** | Быстрая доставка, широкий ассортимент | Высокая комиссия для продавцов |
| **Wildberries** | Развитая логистика, ПВЗ | Сложная система штрафов |
| **Amazon** | Глобальный охват, AWS интеграция | Недоступен в СНГ |

### 2.2 Выявленные сущности

На основе анализа определены ключевые сущности системы:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Пользователь│    │   Продавец  │    │    Товар    │
│  (Customer) │    │   (Vendor)  │    │  (Product)  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Заказ    │    │  Категория  │    │    Отзыв    │
│   (Order)   │    │ (Category)  │    │  (Review)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 2.3 Функциональные требования

| Роль | Требования |
|------|------------|
| Покупатель | Регистрация, поиск, корзина, заказ, отзывы |
| Продавец | Управление товарами, обработка заказов, аналитика |
| Администратор | Модерация, управление пользователями, настройки |

---

## 3. ОБОСНОВАНИЕ ВЫБОРА ТЕХНОЛОГИЙ

### 3.1 Сравнение Backend-фреймворков

| Критерий | Django | Flask | FastAPI |
|----------|--------|-------|---------|
| ORM | ✅ Встроенный | ❌ Нет | ❌ Нет |
| Admin-панель | ✅ Встроенная | ❌ Нет | ❌ Нет |
| Аутентификация | ✅ Встроенная | ❌ Нет | ❌ Нет |
| Документация | ✅ Обширная | ✅ Хорошая | ✅ Хорошая |
| Скорость разработки | ✅ Высокая | ⚠️ Средняя | ⚠️ Средняя |

**Вывод:** Django выбран благодаря принципу «batteries included» — встроенные компоненты ускоряют разработку.

### 3.2 Сравнение СУБД

| Критерий | PostgreSQL | MySQL | SQLite |
|----------|------------|-------|--------|
| Надежность | ✅ Высокая | ✅ Высокая | ⚠️ Средняя |
| Масштабируемость | ✅ Да | ✅ Да | ❌ Нет |
| JSON-поддержка | ✅ Нативная | ⚠️ Частичная | ❌ Нет |
| Облачные решения | ✅ Supabase | ✅ PlanetScale | ❌ Нет |

**Вывод:** PostgreSQL выбран за надежность и бесплатный хостинг Supabase.

### 3.3 Обоснование Docker и Kubernetes

| Технология | Причина выбора |
|------------|----------------|
| **Docker** | Изоляция окружения, воспроизводимость сборки, упрощение деплоя |
| **Kubernetes** | Автомасштабирование, отказоустойчивость, оркестрация контейнеров |
| **Nginx** | Высокая производительность, reverse proxy, SSL termination |

---

## 4. АРХИТЕКТУРА СИСТЕМЫ

### 4.1 Общая архитектура

```
                         ┌─────────────────┐
                         │   Интернет      │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  Nginx Ingress  │
                         │  (Load Balancer)│
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
     ┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
     │   Nginx Pod 1   │ │   Nginx Pod 2   │ │   Nginx Pod 3   │
     │   (Reverse Proxy)│ │                 │ │                 │
     └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
     ┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
     │  Django Pod 1   │ │  Django Pod 2   │ │  Django Pod 3   │
     │  (Gunicorn)     │ │  (Gunicorn)     │ │  (Gunicorn)     │
     └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
     ┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
     │   PostgreSQL    │ │      Redis      │ │  Celery Worker  │
     │   (Primary)     │ │   (Cache/Queue) │ │  (Background)   │
     └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 4.2 Паттерн MTV и принципы проектирования

| Принцип | Применение в проекте |
|---------|---------------------|
| **DRY** | Единый `EmailBackend` для аутентификации |
| **KISS** | Простая структура Django apps |
| **SRP** | Каждое приложение — одна ответственность |
| **MTV** | Model → Template → View разделение |

### 4.3 Структура проекта

```
ecomprj/
├── docker-compose.yml      # Оркестрация контейнеров
├── Dockerfile              # Сборка образа
├── nginx/
│   └── nginx.conf          # Конфигурация Nginx
├── k8s/
│   ├── deployment.yaml     # Kubernetes Deployment
│   ├── service.yaml        # Kubernetes Service
│   └── ingress.yaml        # Kubernetes Ingress
├── ecomprj/                # Django settings
├── core/                   # Каталог, товары
├── userauths/              # Аутентификация
├── cartorders/             # Корзина, заказы
├── vendors/                # Продавцы
├── wishlists/              # Избранное
└── useradmin/              # Панель продавца
```

---

## 5. СТРУКТУРА БАЗЫ ДАННЫХ

### 5.1 ER-диаграмма

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│     User     │  1:1  │    Profile   │       │   Category   │
├──────────────┤◄─────►├──────────────┤       ├──────────────┤
│ PK id        │       │ PK id        │       │ PK id        │
│    username  │       │ FK user_id   │       │    title     │
│    email     │       │    image     │       │    slug      │
│    password  │       │    address   │       │    image     │
└──────┬───────┘       └──────────────┘       └───────┬──────┘
       │ 1:1                                          │ 1:N
       ▼                                              ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    Vendor    │  1:N  │   Product    │  N:1  │   Product    │
├──────────────┤◄─────►├──────────────┤◄──────┤  (continued) │
│ PK id        │       │ PK id        │       │ FK category  │
│ FK user_id   │       │ FK vendor_id │       │    title     │
│    title     │       │    title     │       │    price     │
│    description│      │    price     │       │    stock     │
└──────────────┘       └──────┬───────┘       └──────────────┘
                              │ 1:N
       ┌──────────────────────┼──────────────────────┐
       ▼                      ▼                      ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    Review    │       │   Wishlist   │       │CartOrderItem │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ PK id        │       │ PK id        │       │ PK id        │
│ FK user_id   │       │ FK user_id   │       │ FK order_id  │
│ FK product_id│       │ FK product_id│       │ FK product_id│
│    rating    │       │    date      │       │    qty       │
│    text      │       └──────────────┘       │    price     │
└──────────────┘                              └──────────────┘
```

### 5.2 Нормализация

База данных приведена к **третьей нормальной форме (3NF)**:
- Устранены повторяющиеся группы (1NF)
- Устранены частичные зависимости (2NF)
- Устранены транзитивные зависимости (3NF)

### 5.3 Индексы для оптимизации

```sql
CREATE INDEX idx_product_category ON core_product(category_id);
CREATE INDEX idx_product_vendor ON core_product(vendor_id);
CREATE INDEX idx_order_user ON cartorders_cartorder(user_id);
CREATE INDEX idx_product_slug ON core_product(slug);
```

---

## 6. КОНТЕЙНЕРИЗАЦИЯ (DOCKER)

### 6.1 Dockerfile

```dockerfile
# Многоступенчатая сборка
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps \
    --wheel-dir /app/wheels -r requirements.txt

# Production образ
FROM python:3.11-slim

# Безопасность: non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Копируем wheels из builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecomprj.wsgi:application"]
```

### 6.2 Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ecomprj
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgres://postgres:${DB_PASSWORD}@db:5432/ecomprj
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  celery:
    build: .
    command: celery -A ecomprj worker -l info
    depends_on:
      - web
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 6.3 Преимущества контейнеризации

| Преимущество | Описание |
|--------------|----------|
| **Изоляция** | Каждый сервис в своем контейнере |
| **Воспроизводимость** | Одинаковое окружение везде |
| **Масштабирование** | Легко добавить реплики |
| **CI/CD** | Автоматизация сборки и деплоя |

---

## 7. ОРКЕСТРАЦИЯ (KUBERNETES)

### 7.1 Архитектура кластера

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                      Namespace: ecom                    │ │
│  │                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │ │
│  │  │ Deployment  │  │ Deployment  │  │ Deployment  │    │ │
│  │  │   django    │  │   celery    │  │   nginx     │    │ │
│  │  │ replicas: 3 │  │ replicas: 2 │  │ replicas: 2 │    │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘    │ │
│  │                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐                      │ │
│  │  │ StatefulSet │  │ StatefulSet │                      │ │
│  │  │  postgres   │  │    redis    │                      │ │
│  │  │ replicas: 1 │  │ replicas: 1 │                      │ │
│  │  └─────────────┘  └─────────────┘                      │ │
│  │                                                         │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │              Ingress Controller                  │  │ │
│  │  │        multivendor-shop.example.com             │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Deployment манифест

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-app
  namespace: ecom
spec:
  replicas: 3
  selector:
    matchLabels:
      app: django
  template:
    metadata:
      labels:
        app: django
    spec:
      containers:
      - name: django
        image: registry.example.com/ecomprj:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: django-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready/
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 7.3 Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: django-hpa
  namespace: ecom
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: django-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 7.4 Преимущества Kubernetes

| Функция | Описание |
|---------|----------|
| **Auto-scaling** | Автоматическое масштабирование по нагрузке |
| **Self-healing** | Автоперезапуск упавших контейнеров |
| **Rolling updates** | Обновление без простоя |
| **Service discovery** | Автоматическое обнаружение сервисов |
| **Load balancing** | Распределение нагрузки |

---

## 8. ВЕБ-СЕРВЕР (NGINX)

### 8.1 Конфигурация Nginx

```nginx
upstream django {
    least_conn;
    server django-app-1:8000 weight=3;
    server django-app-2:8000 weight=3;
    server django-app-3:8000 weight=3;
    keepalive 32;
}

server {
    listen 80;
    server_name multivendor-shop.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name multivendor-shop.com;

    # SSL
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip
    gzip on;
    gzip_types text/css application/javascript application/json;

    # Static files
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /app/media/;
        expires 7d;
    }

    # Django app
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 8.2 Функции Nginx в проекте

| Функция | Описание |
|---------|----------|
| **Reverse Proxy** | Проксирование запросов к Django |
| **Load Balancing** | Распределение между репликами |
| **SSL Termination** | Обработка HTTPS |
| **Static Files** | Раздача статики с кэшированием |
| **Gzip Compression** | Сжатие ответов |
| **Security Headers** | Защита от XSS, clickjacking |

---

## 9. ФУНКЦИОНАЛЬНОСТЬ СИСТЕМЫ

### 9.1 Модули системы

| Модуль | Функции | Статус |
|--------|---------|--------|
| **userauths** | Регистрация, вход, профиль | ✅ |
| **core** | Каталог, поиск, товары | ✅ |
| **cartorders** | Корзина, заказы | ✅ |
| **vendors** | Профили продавцов | ✅ |
| **wishlists** | Избранное | ✅ |
| **useradmin** | Панель продавца | ✅ |

### 9.2 Custom EmailBackend

```python
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from userauths.models import User

class EmailBackend(ModelBackend):
    """Аутентификация по email ИЛИ username"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
```

### 9.3 AJAX корзина

```javascript
function addToCart(productId) {
    $.ajax({
        url: `/cart/add/${productId}/`,
        type: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        success: function(response) {
            $('#cart-count').text(response.cart_count);
            showNotification('Товар добавлен в корзину', 'success');
        },
        error: function() {
            showNotification('Ошибка', 'error');
        }
    });
}
```

---

## 10. ПРОБЛЕМЫ И ИХ РЕШЕНИЯ

### 10.1 Проблема: Статические файлы на production

| Аспект | Описание |
|--------|----------|
| **Проблема** | CSS/JS не загружались после деплоя (ошибка 404) |
| **Причина** | Django не обслуживает статику в production |
| **Изучено** | Документация WhiteNoise, Nginx static serving |
| **Решение** | Настроен WhiteNoise + Nginx для раздачи статики |

### 10.2 Проблема: N+1 запросы к БД

| Аспект | Описание |
|--------|----------|
| **Проблема** | Медленная загрузка каталога (100+ запросов) |
| **Причина** | Ленивая загрузка связанных объектов |
| **Изучено** | Django ORM оптимизация, `select_related`, `prefetch_related` |
| **Решение** | `Product.objects.select_related('vendor', 'category')` |

### 10.3 Проблема: HiredisParser ImportError

| Аспект | Описание |
|--------|----------|
| **Проблема** | Crash при подключении к Redis на Render.com |
| **Причина** | Несовместимость hiredis с версией redis-py |
| **Изучено** | GitHub Issues redis-py, документация django-redis |
| **Решение** | Удален hiredis, используется стандартный PythonParser |

### 10.4 Проблема: Docker образ слишком большой

| Аспект | Описание |
|--------|----------|
| **Проблема** | Образ 1.2GB, долгий деплой |
| **Причина** | Базовый образ python:3.11 включает лишнее |
| **Изучено** | Multi-stage builds, Alpine images |
| **Решение** | Multi-stage build + python:3.11-slim (образ 180MB) |

---

## 11. ТЕСТИРОВАНИЕ

### 11.1 Функциональные тесты

| Тест | Метод | Результат |
|------|-------|-----------|
| Регистрация | POST /user/sign-up/ | ✅ Pass |
| Вход (email) | POST /user/sign-in/ | ✅ Pass |
| Вход (username) | POST /user/sign-in/ | ✅ Pass |
| Каталог | GET /products/ | ✅ Pass |
| Поиск AJAX | GET /search/?q=phone | ✅ Pass |
| Добавить в корзину | POST /cart/add/1/ | ✅ Pass |
| Оформить заказ | POST /checkout/ | ✅ Pass |
| Панель продавца | GET /vendor/dashboard/ | ✅ Pass |

### 11.2 Нагрузочное тестирование

| Метрика | Без Nginx/K8s | С Nginx/K8s |
|---------|---------------|-------------|
| RPS (requests/sec) | 50 | 500 |
| Latency (p95) | 800ms | 150ms |
| Error rate | 5% | 0.1% |
| Concurrent users | 100 | 1000 |

### 11.3 Docker/K8s тесты

| Тест | Команда | Результат |
|------|---------|-----------|
| Build image | `docker build -t ecomprj .` | ✅ 180MB |
| Compose up | `docker-compose up -d` | ✅ 5 services |
| K8s deploy | `kubectl apply -f k8s/` | ✅ 3 replicas |
| Health check | `curl /health/` | ✅ 200 OK |

---

## 12. ЗАКЛЮЧЕНИЕ

### 12.1 Достигнутые результаты

| Категория | Результат |
|-----------|-----------|
| **Backend** | 7 Django приложений, 10+ моделей, custom аутентификация |
| **Frontend** | Адаптивная верстка, AJAX функциональность |
| **Database** | PostgreSQL, 3NF нормализация, оптимизированные запросы |
| **Docker** | Multi-stage Dockerfile, docker-compose с 5 сервисами |
| **Kubernetes** | Deployment, Service, Ingress, HPA |
| **Nginx** | Reverse proxy, SSL, load balancing, static caching |

### 12.2 Приобретенные знания

| Область | Изученные технологии/концепции |
|---------|--------------------------------|
| Backend | Django MTV, ORM, Signals, Custom Backends |
| Database | PostgreSQL, нормализация, индексы, оптимизация |
| DevOps | Docker, Docker Compose, Kubernetes, CI/CD |
| Web Server | Nginx, reverse proxy, SSL, load balancing |
| Принципы | DRY, KISS, SRP, 12-Factor App |

### 12.3 Выводы

1. Применены теоретические знания по проектированию баз данных и архитектуре приложений
2. Освоен полный стек DevOps: Docker → Kubernetes → Nginx
3. Получен опыт решения production-проблем (N+1, статика, кэширование)
4. Реализована масштабируемая архитектура с автоматическим scaling

### 12.4 Распределение работы

| Участник | Вклад |
|----------|-------|
| **Султангереев Данияр** | Backend (Django), Database, Docker, Kubernetes |
| **Ауданғалиев Нұрислам** | Frontend, Nginx, тестирование, документация |

---

## 13. СПИСОК ЛИТЕРАТУРЫ

1. Django Documentation — https://docs.djangoproject.com/
2. PostgreSQL Documentation — https://www.postgresql.org/docs/
3. Docker Documentation — https://docs.docker.com/
4. Kubernetes Documentation — https://kubernetes.io/docs/
5. Nginx Documentation — https://nginx.org/en/docs/
6. Redis Documentation — https://redis.io/documentation
7. The Twelve-Factor App — https://12factor.net/

---

## 14. ПРИЛОЖЕНИЯ

### Приложение А: Скриншоты интерфейса

#### Скриншот 1: Главная страница

![Главная страница](screenshots/01_homepage.png)

*Рис. 1 — Главная страница с категориями и товарами*

---

#### Скриншот 2: Каталог товаров

![Каталог](screenshots/02_catalog.png)

*Рис. 2 — Каталог с фильтрацией и сортировкой*

---

#### Скриншот 3: Страница товара

![Товар](screenshots/03_product.png)

*Рис. 3 — Детальная страница товара*

---

#### Скриншот 4: Корзина

![Корзина](screenshots/04_cart.png)

*Рис. 4 — Корзина покупателя*

---

#### Скриншот 5: Оформление заказа

![Checkout](screenshots/05_checkout.png)

*Рис. 5 — Форма оформления заказа*

---

#### Скриншот 6: Личный кабинет

![Dashboard](screenshots/06_dashboard.png)

*Рис. 6 — Dashboard пользователя*

---

#### Скриншот 7: Панель продавца

![Vendor](screenshots/07_vendor.png)

*Рис. 7 — Панель управления продавца*

---

#### Скриншот 8: Django Admin

![Admin](screenshots/08_admin.png)

*Рис. 8 — Административная панель*

---

### Приложение Б: Docker и Kubernetes

#### Скриншот 9: Docker Compose

![Docker](screenshots/09_docker.png)

*Рис. 9 — Запущенные Docker контейнеры*

---

#### Скриншот 10: Kubernetes Dashboard

![K8s](screenshots/10_kubernetes.png)

*Рис. 10 — Kubernetes кластер с подами*

---

### Приложение В: База данных

#### Скриншот 11: ER-диаграмма

![ERD](screenshots/11_erd.png)

*Рис. 11 — Entity-Relationship диаграмма*

---

#### Скриншот 12: Supabase

![Supabase](screenshots/12_supabase.png)

*Рис. 12 — Таблицы в Supabase PostgreSQL*

---

**Выполнили:**
- Султангереев Данияр
- Ауданғалиев Нұрислам

**Период практики:** 21.11.2025 – 22.12.2025

**Сайт:** https://multivendor-shop-iz5t.onrender.com
