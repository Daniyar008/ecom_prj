"""
Celery Beat schedule configuration.
Настройка периодических задач.
"""

from celery.schedules import crontab

# Расписание для периодических задач
CELERY_BEAT_SCHEDULE = {
    # Очистка старых сессий каждую ночь в 3:00
    "cleanup-sessions": {
        "task": "core.tasks.cleanup_old_sessions",
        "schedule": crontab(hour=3, minute=0),
    },
    # Ежедневный отчет каждое утро в 9:00
    "daily-report": {
        "task": "core.tasks.generate_daily_report",
        "schedule": crontab(hour=9, minute=0),
    },
    # Обработка брошенных корзин каждые 6 часов
    "process-abandoned-carts": {
        "task": "cartorders.tasks.process_abandoned_carts",
        "schedule": crontab(minute=0, hour="*/6"),
    },
}
