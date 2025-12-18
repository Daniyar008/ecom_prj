from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps


def vendor_required(view_func):
    """Декоратор для проверки, что пользователь является вендором"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Пожалуйста, войдите в систему")
            return redirect("vendors:vendor-login")

        if not request.user.is_vendor:
            messages.warning(request, "У вас нет прав доступа к панели продавца")
            return redirect("core:index")

        # Проверяем, есть ли у пользователя профиль вендора
        from vendors.models import Vendor

        if not Vendor.objects.filter(user=request.user).exists():
            messages.warning(request, "Профиль продавца не найден")
            return redirect("core:index")

        return view_func(request, *args, **kwargs)

    return wrapper


def vendor_or_admin_required(view_func):
    """Декоратор для вендора или администратора"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Пожалуйста, войдите в систему")
            return redirect("vendors:vendor-login")

        if not (request.user.is_vendor or request.user.is_superuser):
            messages.warning(request, "У вас нет прав доступа")
            return redirect("core:index")

        return view_func(request, *args, **kwargs)

    return wrapper
