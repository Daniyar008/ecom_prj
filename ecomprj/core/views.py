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


@cache_page(60 * 5)  # Кешируем на 5 минут
def index(request):
    # Пробуем получить из кеша
    cache_key = 'homepage_products'
    products = cache.get(cache_key)
    
    if products is None:
        # Если нет в кеше, запрашиваем из БД
        products = Product.objects.filter(product_status="published", featured=True).order_by("-id")
        # Сохраняем в кеш на 5 минут
        cache.set(cache_key, products, 60 * 5)

    context = {
        "products":products
    }

    return render(request, 'core/index.html', context)





@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)


    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
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
    print("user profile is: #########################",  user_profile)

    context = {
        "user_profile": user_profile,
        "orders": orders,
        "orders_list": orders_list,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, 'core/dashboard.html', context)




def contact(request):
    return render(request, "core/contact.html")


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data":data})


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
        cache_key = f'requests_count_{today}'
        requests_count = cache.get(cache_key, 0)
        last_request = cache.get('last_request_time', 'No data')
        
        stats['redis_connected'] = True
        stats['requests_today'] = requests_count
        stats['last_request_time'] = last_request
        stats['redis_url'] = bool(settings.CACHES['default']['LOCATION'])
        stats['cache_backend'] = settings.CACHES['default']['BACKEND']
        
        # Тестируем set/get
        cache.set('test_key', 'test_value', 60)
        test_value = cache.get('test_key')
        stats['test_passed'] = test_value == 'test_value'
        
    except Exception as e:
        stats['redis_connected'] = False
        stats['error'] = str(e)
    
    return JsonResponse(stats)


def purchase_guide(request):
    return render(request, "core/purchase_guide.html")

def privacy_policy(request):
    return render(request, "core/privacy_policy.html")

def terms_of_service(request):
    return render(request, "core/terms_of_service.html")


