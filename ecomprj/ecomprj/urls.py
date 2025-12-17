"""ecomprj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static


# URL для переключения языка (не требует языкового префикса)
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # set_language view
]

# Основные URL с языковым префиксом (/en/, /kk/, /ru/)
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("user/", include("userauths.urls")),
    path(
        "admin-panel/", include("useradmin.urls")
    ),  # Переименовал чтобы не конфликтовать с admin/
    path("catalog/", include("goods.urls", namespace="catalog")),
    path("vendors/", include("vendors.urls", namespace="vendors")),
    path("wishlists/", include("wishlists.urls", namespace="wishlist")),
    path("cartorders/", include("cartorders.urls", namespace="cartorder")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    prefix_default_language=False,  # Не добавлять /en/ для языка по умолчанию
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
