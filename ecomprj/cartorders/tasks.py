"""
Celery tasks for order processing.
Асинхронные задачи для обработки заказов.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_order_confirmation_email(self, order_id):
    """
    Отправка email подтверждения заказа.

    Args:
        order_id: ID заказа
    """
    from cartorders.models import CartOrder

    try:
        order = CartOrder.objects.get(id=order_id)

        subject = f"Order Confirmation #{order.oid}"
        message = f"""
        Thank you for your order!
        
        Order ID: {order.oid}
        Total: ${order.price}
        Status: {order.product_status}
        
        We will process your order shortly.
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )

        logger.info(f"Order confirmation email sent for order {order.oid}")
        return f"Email sent for order {order.oid}"

    except CartOrder.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        return f"Order {order_id} not found"
    except Exception as exc:
        logger.error(f"Error sending order email: {exc}")
        raise self.retry(exc=exc, countdown=300)


@shared_task
def update_order_status(order_id, new_status):
    """
    Обновление статуса заказа.

    Args:
        order_id: ID заказа
        new_status: Новый статус
    """
    from cartorders.models import CartOrder

    try:
        order = CartOrder.objects.get(id=order_id)
        order.product_status = new_status
        order.save()

        logger.info(f"Order {order.oid} status updated to {new_status}")

        # Отправляем уведомление клиенту
        send_order_confirmation_email.delay(order_id)

        return f"Order {order.oid} updated to {new_status}"

    except CartOrder.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        return f"Order {order_id} not found"
    except Exception as exc:
        logger.error(f"Error updating order status: {exc}")
        raise


@shared_task
def process_abandoned_carts():
    """
    Обработка брошенных корзин.
    Отправка напоминаний пользователям.
    """
    from cartorders.models import CartOrder
    from django.utils import timezone
    from datetime import timedelta

    try:
        # Находим заказы старше 24 часов со статусом pending
        cutoff_time = timezone.now() - timedelta(hours=24)
        abandoned_orders = CartOrder.objects.filter(
            product_status="pending", order_date__lte=cutoff_time
        )

        count = 0
        for order in abandoned_orders:
            # Отправляем напоминание
            subject = f"Complete Your Order #{order.oid}"
            message = f"""
            You have an incomplete order.
            
            Order ID: {order.oid}
            Total: ${order.price}
            
            Click here to complete your purchase.
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=True,
            )
            count += 1

        logger.info(f"Processed {count} abandoned carts")
        return f"Sent {count} reminders"

    except Exception as exc:
        logger.error(f"Error processing abandoned carts: {exc}")
        raise
