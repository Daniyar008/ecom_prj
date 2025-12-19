from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from requests import session
import stripe
from taggit.models import Tag
import datetime

from .models import Vendor
from .forms import (
    VendorRegisterForm,
    VendorLoginForm,
    VendorProfileForm,
    VendorProductForm,
)
from .decorators import vendor_required
from goods.models import Product, Category, ProductReview
from cartorders.models import CartOrder, CartOrderProducts
from userauths.models import User


# ========== Public Views ==========


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request, "vendors/vendor-list.html", context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = (
        Product.objects.filter(vendor=vendor, product_status="published")
        .select_related("category")
        .order_by("-id")
    )

    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "vendors/vendor-detail.html", context)


# ========== Vendor Auth Views ==========


def vendor_register_view(request):
    """Регистрация нового вендора"""
    if request.user.is_authenticated and request.user.is_vendor:
        return redirect("vendors:vendor-dashboard")

    if request.method == "POST":
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            try:
                # Создаем пользователя
                user = form.save(commit=False)
                user.is_vendor = True
                user.save()

                # Создаем профиль вендора
                vendor = Vendor.objects.create(
                    user=user,
                    title=form.cleaned_data["shop_name"],
                    description=form.cleaned_data.get("shop_description", ""),
                    contact=form.cleaned_data["contact"],
                    address=form.cleaned_data["address"],
                )

                # Авторизуем пользователя
                new_user = authenticate(
                    request,
                    username=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                )

                if new_user is not None:
                    login(request, new_user)
                    messages.success(
                        request,
                        f"Добро пожаловать, {vendor.title}! Ваш магазин создан.",
                    )
                    return redirect("vendors:vendor-dashboard")

            except Exception as e:
                messages.error(request, f"Ошибка регистрации: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = VendorRegisterForm()

    context = {"form": form}
    return render(request, "vendors/vendor-register.html", context)


def vendor_login_view(request):
    """Вход для вендора"""
    if request.user.is_authenticated and request.user.is_vendor:
        return redirect("vendors:vendor-dashboard")

    if request.method == "POST":
        form = VendorLoginForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, "Вы вошли в панель продавца.")
                return redirect("vendors:vendor-dashboard")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = VendorLoginForm()

    context = {"form": form}
    return render(request, "vendors/vendor-login.html", context)


def vendor_logout_view(request):
    """Выход вендора"""
    logout(request)
    messages.success(request, "Вы вышли из системы.")
    return redirect("vendors:vendor-login")


# ========== Vendor Dashboard Views ==========


@vendor_required
def vendor_dashboard(request):
    """Главная страница дашборда вендора"""
    vendor = Vendor.objects.get(user=request.user)

    # Получаем товары этого вендора
    products = Product.objects.filter(vendor=vendor)
    products_count = products.count()
    published_count = products.filter(product_status="published").count()
    in_review_count = products.filter(product_status="in_review").count()

    # Получаем названия товаров вендора для поиска в заказах
    vendor_product_titles = list(products.values_list("title", flat=True))

    # Получаем заказы с товарами этого вендора (по названию товара)
    order_items = CartOrderProducts.objects.filter(item__in=vendor_product_titles)
    total_orders = order_items.values("order").distinct().count()

    # Доход (сумма всех проданных товаров)
    revenue = (
        order_items.filter(order__paid_status=True).aggregate(total=Sum("total"))[
            "total"
        ]
        or 0
    )

    # Последние заказы
    recent_order_items = order_items.select_related("order").order_by(
        "-order__order_date"
    )[:10]

    # Отзывы на товары вендора
    reviews = ProductReview.objects.filter(product__vendor=vendor).select_related(
        "product", "user"
    )
    reviews_count = reviews.count()
    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    context = {
        "vendor": vendor,
        "products_count": products_count,
        "published_count": published_count,
        "in_review_count": in_review_count,
        "total_orders": total_orders,
        "revenue": revenue,
        "recent_order_items": recent_order_items,
        "reviews_count": reviews_count,
        "avg_rating": round(avg_rating, 1),
    }
    return render(request, "vendors/dashboard/dashboard.html", context)


@vendor_required
def vendor_products(request):
    """Список товаров вендора"""
    vendor = Vendor.objects.get(user=request.user)
    products = (
        Product.objects.filter(vendor=vendor).select_related("category").order_by("-id")
    )

    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "vendors/dashboard/products.html", context)


@vendor_required
def vendor_add_product(request):
    """Добавление нового товара"""
    vendor = Vendor.objects.get(user=request.user)

    if request.method == "POST":
        form = VendorProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.vendor = vendor
            product.product_status = "in_review"  # Товар на модерацию
            product.save()
            form.save_m2m()  # Сохраняем теги

            messages.success(request, "Товар добавлен и отправлен на модерацию.")
            return redirect("vendors:vendor-products")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = VendorProductForm()

    context = {
        "vendor": vendor,
        "form": form,
    }
    return render(request, "vendors/dashboard/add-product.html", context)


@vendor_required
def vendor_edit_product(request, pid):
    """Редактирование товара"""
    vendor = Vendor.objects.get(user=request.user)
    product = get_object_or_404(Product, pid=pid, vendor=vendor)

    if request.method == "POST":
        form = VendorProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            # При редактировании отправляем на повторную модерацию
            if product.product_status == "published":
                product.product_status = "in_review"
                messages.info(request, "Товар отправлен на повторную модерацию.")
            product.save()
            form.save_m2m()

            messages.success(request, "Товар обновлён.")
            return redirect("vendors:vendor-products")
    else:
        form = VendorProductForm(instance=product)

    context = {
        "vendor": vendor,
        "form": form,
        "product": product,
    }
    return render(request, "vendors/dashboard/edit-product.html", context)


@vendor_required
def vendor_delete_product(request, pid):
    """Удаление товара"""
    vendor = Vendor.objects.get(user=request.user)
    product = get_object_or_404(Product, pid=pid, vendor=vendor)

    product.delete()
    messages.success(request, "Товар удалён.")
    return redirect("vendors:vendor-products")


@vendor_required
def vendor_orders(request):
    """Заказы с товарами вендора"""
    vendor = Vendor.objects.get(user=request.user)

    # Получаем все заказы, содержащие товары этого вендора
    order_items = (
        CartOrderProducts.objects.filter(product_obj__vendor=vendor)
        .select_related("order", "product_obj")
        .order_by("-order__order_date")
    )

    context = {
        "vendor": vendor,
        "order_items": order_items,
    }
    return render(request, "vendors/dashboard/orders.html", context)


@vendor_required
def vendor_reviews(request):
    """Отзывы на товары вендора"""
    vendor = Vendor.objects.get(user=request.user)

    reviews = (
        ProductReview.objects.filter(product__vendor=vendor)
        .select_related("product", "user")
        .order_by("-date")
    )

    context = {
        "vendor": vendor,
        "reviews": reviews,
    }
    return render(request, "vendors/dashboard/reviews.html", context)


@vendor_required
def vendor_settings(request):
    """Настройки профиля вендора"""
    vendor = Vendor.objects.get(user=request.user)

    if request.method == "POST":
        form = VendorProfileForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect("vendors:vendor-settings")
    else:
        form = VendorProfileForm(instance=vendor)

    context = {
        "vendor": vendor,
        "form": form,
    }
    return render(request, "vendors/dashboard/settings.html", context)
