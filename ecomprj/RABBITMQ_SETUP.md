# Настройка RabbitMQ (CloudAMQP) для Celery на Render.com

## Что такое RabbitMQ?

RabbitMQ - это брокер сообщений для асинхронной обработки задач через Celery. Используется для:
- Отправки email уведомлений
- Обработки заказов в фоне
- Генерации отчетов
- Периодических задач (очистка, бэкапы)

## Настройка CloudAMQP (Бесплатный RabbitMQ)

### Шаг 1: Создание CloudAMQP аккаунта

1. Перейдите на https://www.cloudamqp.com/
2. Нажмите **Sign Up** и создайте аккаунт
3. Подтвердите email

### Шаг 2: Создание RabbitMQ инстанса

1. В CloudAMQP Dashboard нажмите **Create New Instance**
2. Выберите:
   - **Name**: ecomprj-rabbitmq
   - **Plan**: Little Lemur (Free) - 1 Million messages/month
   - **Region**: Выберите ближайший к вашему Render региону
     - US-East-1 (Virginia) - для us-east-1 на Render
     - EU-West-1 (Ireland) - для europe-west на Render
   - **Tags**: production (опционально)
3. Нажмите **Create Instance**

### Шаг 3: Получение URL подключения

1. Откройте созданный инстанс
2. На вкладке **Details** найдите **AMQP URL**
3. Скопируйте URL (формат: `amqp://username:password@host.cloudamqp.com/vhost`)

Пример URL:
```
amqp://gzkxwmly:Abc123XyzPassword@possum.lmq.cloudamqp.com/gzkxwmly
```

### Шаг 4: Добавление переменной на Render

1. Откройте **Render Dashboard** → ваш Web Service
2. Перейдите на вкладку **Environment**
3. Нажмите **Add Environment Variable**
4. Добавьте:
   - **Key**: `RABBITMQ_URL`
   - **Value**: Вставьте скопированный AMQP URL
5. Нажмите **Save Changes**
6. Render автоматически перезапустит сервис

### Шаг 5: Создание Celery Worker на Render

Celery Worker - это отдельный процесс для выполнения асинхронных задач.

1. В Render Dashboard нажмите **New** → **Background Worker**
2. Подключите тот же GitHub репозиторий
3. Настройте:
   - **Name**: ecomprj-celery-worker
   - **Region**: Тот же что и Web Service
   - **Branch**: daniyar
   - **Root Directory**: ecomprj
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     celery -A ecomprj worker --loglevel=info
     ```
4. В **Environment Variables** добавьте все переменные из Web Service:
   - `DATABASE_URL` (из Supabase)
   - `REDIS_URL` (из Redis instance)
   - `RABBITMQ_URL` (из CloudAMQP)
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`
   - `CSRF_TRUSTED_ORIGINS`
5. Нажмите **Create Background Worker**

### Шаг 6 (Опционально): Celery Beat для периодических задач

Celery Beat - для запуска задач по расписанию (ежедневные отчеты, очистка и т.д.).

1. Создайте еще один **Background Worker**
2. Настройте:
   - **Name**: ecomprj-celery-beat
   - **Start Command**: 
     ```bash
     celery -A ecomprj beat --loglevel=info
     ```
3. Добавьте те же Environment Variables
4. **ВАЖНО**: Запускайте только ОДИН инстанс Celery Beat!

## Проверка работы

### 1. Проверка через эндпоинт

Откройте в браузере:
```
https://your-app.onrender.com/celery-stats/
```

Должен показать:
```json
{
  "broker_url": "amqp://***@***",
  "result_backend": "redis://***@***",
  "celery_connected": true,
  "workers": ["celery@worker-name"],
  "active_tasks_count": 0,
  "test_task_sent": true,
  "test_task_id": "uuid-here"
}
```

### 2. Проверка через Render логи

**Web Service логи** должны показать:
```
Celery worker starting...
Connected to amqp://***@possum.lmq.cloudamqp.com//***
```

**Celery Worker логи** должны показать:
```
[tasks]
  . core.tasks.cleanup_old_sessions
  . core.tasks.generate_daily_report
  . core.tasks.send_email_notification
  . core.tasks.test_celery_task
  . cartorders.tasks.process_abandoned_carts
  . cartorders.tasks.send_order_confirmation_email

celery@worker ready
```

### 3. Проверка через CloudAMQP Dashboard

1. Откройте CloudAMQP Dashboard → ваш инстанс
2. Вкладка **RabbitMQ Manager**
3. **Connections**: Должно быть 1-2 активных подключения (Worker + Beat)
4. **Queues**: Должна быть очередь `celery`
5. **Messages**: Количество обработанных сообщений должно расти

## Использование Celery в коде

### Отправка асинхронной задачи

```python
from core.tasks import send_email_notification

# Отправить задачу в очередь
result = send_email_notification.delay(
    subject="Test Email",
    message="Hello from Celery!",
    recipient_list=["user@example.com"]
)

# Получить ID задачи
task_id = result.id
```

### Проверка результата задачи

```python
from celery.result import AsyncResult

result = AsyncResult(task_id)
if result.ready():
    print(f"Task completed: {result.result}")
else:
    print(f"Task status: {result.status}")
```

## Мониторинг и отладка

### CloudAMQP Dashboard
- **Overview**: Общая статистика (сообщения/сек, подключения)
- **RabbitMQ Manager**: Детальная информация по очередям
- **Alarms**: Уведомления о проблемах

### Render Logs
```bash
# Web Service logs
tail -f logs/web.log

# Celery Worker logs  
tail -f logs/celery-worker.log

# Celery Beat logs
tail -f logs/celery-beat.log
```

## Лимиты бесплатного плана CloudAMQP

- **Сообщений в месяц**: 1 миллион
- **Подключений**: До 20 одновременных
- **Очередей**: Без ограничений
- **Хранение сообщений**: 10 MB

Этого достаточно для:
- ~33,000 сообщений в день
- Обработка заказов для небольшого магазина
- Email уведомления
- Периодические задачи

## Troubleshooting

### Ошибка: "Connection refused"
- Проверьте RABBITMQ_URL в Environment Variables
- Убедитесь что CloudAMQP инстанс активен
- Проверьте регион (должен быть близко к Render)

### Ошибка: "No active workers"
- Запустите Celery Worker на Render
- Проверьте логи Worker на ошибки
- Убедитесь что все Environment Variables скопированы

### Задачи не выполняются
- Проверьте CloudAMQP Dashboard → Messages
- Посмотрите Celery Worker логи на ошибки
- Убедитесь что Worker запущен: `celery_connected: true`

### Превышен лимит сообщений
- Уменьшите частоту периодических задач
- Оптимизируйте код задач
- Рассмотрите платный план CloudAMQP

## Стоимость

- **CloudAMQP Free**: $0/месяц (1M сообщений)
- **CloudAMQP Bunny**: $9/месяц (10M сообщений)
- **Render Background Worker**: $7/месяц (512MB RAM)

Альтернатива: Redis как брокер (уже настроен), но RabbitMQ надежнее для продакшена.
