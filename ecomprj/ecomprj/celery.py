"""
Celery configuration for ecomprj project.
"""

import os
from celery import Celery
from django.conf import settings

# Устанавливаем настройки Django для celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecomprj.settings")

app = Celery("ecomprj")

# Загружаем конфигурацию из Django settings с префиксом CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим tasks.py во всех приложениях
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Загружаем расписание для периодических задач (Celery Beat)
try:
    from ecomprj.celery_beat_schedule import CELERY_BEAT_SCHEDULE

    app.conf.beat_schedule = CELERY_BEAT_SCHEDULE
except ImportError:
    pass


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Отладочная задача для проверки работы Celery"""
    print(f"Request: {self.request!r}")
