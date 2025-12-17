from modeltranslation.translator import register, TranslationOptions
from .models import CartOrder, CartOrderProducts, Address, Coupon


@register(CartOrder)
class CartOrderTranslationOptions(TranslationOptions):
    fields = ("shipping_method", "tracking_website_address", "product_status")


@register(CartOrderProducts)
class CartOrderProductsTranslationOptions(TranslationOptions):
    fields = ("item", "product_status")


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ("address",)


@register(Coupon)
class CouponTranslationOptions(TranslationOptions):
    fields = ("code",)
