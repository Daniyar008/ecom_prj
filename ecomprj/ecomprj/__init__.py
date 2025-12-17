"""
Инициализация Celery для Django проекта.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
