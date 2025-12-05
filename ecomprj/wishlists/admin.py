from django.contrib import admin

from .models import Wishlist


@admin.register(Wishlist)
class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']