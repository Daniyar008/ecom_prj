"""
Celery tasks for core application.
Асинхронные задачи для фоновой обработки.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_notification(self, subject, message, recipient_list):
    """
    Асинхронная отправка email уведомлений.

    Args:
        subject: Тема письма
        message: Текст письма
        recipient_list: Список получателей
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_list}")
        return f"Email sent to {len(recipient_list)} recipients"
    except Exception as exc:
        logger.error(f"Error sending email: {exc}")
        # Повторная попытка через 5 минут
        raise self.retry(exc=exc, countdown=300)


@shared_task
def cleanup_old_sessions():
    """
    Очистка старых сессий из БД.
    Запускается периодически через Celery Beat.
    """
    from django.core.management import call_command

    try:
        call_command("clearsessions")
        logger.info("Old sessions cleaned successfully")
        return "Sessions cleaned"
    except Exception as exc:
        logger.error(f"Error cleaning sessions: {exc}")
        raise


@shared_task
def generate_daily_report():
    """
    Генерация ежедневного отчета по заказам.
    """
    from cartorders.models import CartOrder
    from django.utils import timezone
    from datetime import timedelta

    try:
        yesterday = timezone.now() - timedelta(days=1)
        orders_count = CartOrder.objects.filter(order_date__gte=yesterday).count()

        logger.info(f"Daily report: {orders_count} orders yesterday")
        return f"Report generated: {orders_count} orders"
    except Exception as exc:
        logger.error(f"Error generating report: {exc}")
        raise


@shared_task(bind=True)
def test_celery_task(self):
    """
    Тестовая задача для проверки работы Celery.
    """
    logger.info("Test Celery task started")
    return f"Task executed successfully. Task ID: {self.request.id}"
