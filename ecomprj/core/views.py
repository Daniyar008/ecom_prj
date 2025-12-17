from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from userauths.models import ContactUs, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.cache import cache

import calendar
from django.db.models import Count, Avg
from django.db.models.functions import ExtractMonth

from goods.models import Product
from cartorders.models import CartOrder, Address


def index(request):
    # Оптимизированный запрос с select_related для избежания N+1
    try:
        products = (
            Product.objects.filter(product_status="published", featured=True)
            .select_related("category", "vendor")
            .prefetch_related("reviews")
            .order_by("-id")[:20]
        )
    except Exception:
        products = []

    context = {"products": products}

    return render(request, "core/index.html", context)


@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)

    orders = (
        CartOrder.objects.annotate(month=ExtractMonth("order_date"))
        .values("month")
        .annotate(count=Count("id"))
        .values("month", "count")
    )
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])

    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully.")
        return redirect("core:dashboard")
    else:
        print("Error")

    user_profile = Profile.objects.get(user=request.user)
    print("user profile is: #########################", user_profile)

    context = {
        "user_profile": user_profile,
        "orders": orders,
        "orders_list": orders_list,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, "core/dashboard.html", context)


def contact(request):
    return render(request, "core/contact.html")


def ajax_contact_form(request):
    full_name = request.GET["full_name"]
    email = request.GET["email"]
    phone = request.GET["phone"]
    subject = request.GET["subject"]
    message = request.GET["message"]

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {"bool": True, "message": "Message Sent Successfully"}

    return JsonResponse({"data": data})


def about_us(request):
    return render(request, "core/about_us.html")


def redis_stats(request):
    """Проверка статистики Redis для отладки"""
    import datetime
    from django.conf import settings

    stats = {}

    # Проверяем подключение к Redis
    try:
        today = datetime.date.today().isoformat()
        cache_key = f"requests_count_{today}"
        requests_count = cache.get(cache_key, 0)
        last_request = cache.get("last_request_time", "No data")

        stats["redis_connected"] = True
        stats["requests_today"] = requests_count
        stats["last_request_time"] = last_request
        stats["redis_url"] = bool(settings.CACHES["default"]["LOCATION"])
        stats["cache_backend"] = settings.CACHES["default"]["BACKEND"]

        # Тестируем set/get
        cache.set("test_key", "test_value", 60)
        test_value = cache.get("test_key")
        stats["test_passed"] = test_value == "test_value"

    except Exception as e:
        stats["redis_connected"] = False
        stats["error"] = str(e)

    return JsonResponse(stats)


def celery_stats(request):
    """Проверка статистики Celery и режима работы"""
    from django.conf import settings
    from celery import current_app

    stats = {}

    try:
        # Определяем режим работы Celery
        is_eager = getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False)
        stats["mode"] = "EAGER (synchronous)" if is_eager else "ASYNC (requires worker)"
        stats["is_eager"] = is_eager

        # Проверяем настройки Celery
        broker_url = settings.CELERY_BROKER_URL
        if "@" in broker_url:
            stats["broker_url"] = broker_url.split("@")[0] + "@***"
        else:
            stats["broker_url"] = broker_url

        result_backend = str(settings.CELERY_RESULT_BACKEND)
        if "@" in result_backend:
            stats["result_backend"] = result_backend.split("@")[0] + "@***"
        else:
            stats["result_backend"] = result_backend

        # В EAGER режиме worker не нужен
        if is_eager:
            stats["celery_connected"] = True
            stats["workers"] = None
            stats["message"] = "Tasks execute immediately without worker (FREE mode)"
        else:
            # Проверяем подключение к брокеру в ASYNC режиме
            try:
                inspect = current_app.control.inspect()
                active_tasks = inspect.active()
                if active_tasks:
                    stats["celery_connected"] = True
                    stats["workers"] = list(active_tasks.keys())
                    stats["active_tasks_count"] = sum(
                        len(tasks) for tasks in active_tasks.values()
                    )
                else:
                    stats["celery_connected"] = False
                    stats["message"] = (
                        "No active workers found - need Background Worker ($7/month on Render)"
                    )
            except Exception as e:
                stats["celery_connected"] = False
                stats["broker_error"] = str(e)
                stats["message"] = "Worker not running - using EAGER mode instead"

        # Тестируем отправку задачи
        from core.tasks import test_celery_task

        try:
            result = test_celery_task.delay()
            stats["test_task_sent"] = True
            stats["test_task_id"] = (
                str(result.id) if hasattr(result, "id") else "executed-immediately"
            )
            if is_eager:
                stats["test_task_result"] = (
                    result.get() if hasattr(result, "get") else "Task completed"
                )
        except Exception as e:
            stats["test_task_sent"] = False
            stats["test_task_error"] = str(e)

    except Exception as e:
        stats["error"] = str(e)

    return JsonResponse(stats)


def purchase_guide(request):
    return render(request, "core/purchase_guide.html")


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def terms_of_service(request):
    return render(request, "core/terms_of_service.html")
