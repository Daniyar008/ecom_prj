from django.contrib import admin

from .models import CartOrder, CartOrderProducts, Coupon, Address


admin.site.register(Coupon)


@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status', 'sku']
    list_display = ['user',  'price', 'paid_status', 'order_date','product_status', 'sku']


@admin.register(CartOrderProducts)
class CartOrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image','qty', 'price', 'total']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']