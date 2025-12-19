from ast import Add
from decimal import Decimal
from django.db.models import Min, Max
from django.contrib import messages
from django.conf import settings

from goods.models import Product, Category
from wishlists.models import Wishlist
from vendors.models import Vendor
from cartorders.models import CartOrder, Address


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except:
            messages.warning(
                request, "You need to login before accessing your wishlist."
            )
            wishlist = 0
    else:
        wishlist = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None

    # Currency handling
    current_currency = request.session.get("currency", settings.DEFAULT_CURRENCY)
    currencies = settings.CURRENCIES
    currency_info = currencies.get(current_currency, currencies["KZT"])

    return {
        "categories": categories,
        "wishlist": wishlist,
        "address": address,
        "vendors": vendors,
        "min_max_price": min_max_price,
        # Currency context
        "current_currency": current_currency,
        "currency_symbol": currency_info["symbol"],
        "currency_rate": currency_info["rate"],
        "currencies": currencies,
    }


def convert_price(price, rate):
    """Helper function to convert price based on currency rate"""
    if price is None:
        return Decimal("0.00")
    return (Decimal(str(price)) * Decimal(str(rate))).quantize(Decimal("0.01"))
