# =============================================================================
# Currency Template Tags
# =============================================================================
from decimal import Decimal
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def convert_price(context, price):
    """
    Convert price to the current currency.
    Usage: {% convert_price product.price %}
    """
    if price is None:
        return Decimal("0.00")

    request = context.get("request")
    if request:
        currency = request.session.get("currency", settings.DEFAULT_CURRENCY)
    else:
        currency = settings.DEFAULT_CURRENCY

    rate = settings.CURRENCIES.get(currency, {}).get("rate", 1.0)
    converted = Decimal(str(price)) * Decimal(str(rate))
    return converted.quantize(Decimal("0.01"))


@register.simple_tag(takes_context=True)
def price_with_symbol(context, price):
    """
    Convert price and add currency symbol.
    Usage: {% price_with_symbol product.price %}
    """
    if price is None:
        return "0.00"

    request = context.get("request")
    if request:
        currency = request.session.get("currency", settings.DEFAULT_CURRENCY)
    else:
        currency = settings.DEFAULT_CURRENCY

    currency_info = settings.CURRENCIES.get(currency, settings.CURRENCIES["KZT"])
    rate = currency_info.get("rate", 1.0)
    symbol = currency_info.get("symbol", "₸")

    converted = Decimal(str(price)) * Decimal(str(rate))
    formatted = converted.quantize(Decimal("0.01"))

    # Format based on currency
    if currency == "USD":
        return f"{symbol}{formatted:,.2f}"
    else:
        return f"{formatted:,.2f} {symbol}"


@register.filter
def multiply(value, arg):
    """
    Multiply value by arg (for currency conversion).
    Usage: {{ product.price|multiply:currency_rate }}
    """
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return value


@register.simple_tag(takes_context=True)
def get_currency_symbol(context):
    """
    Get the current currency symbol.
    Usage: {% get_currency_symbol %}
    """
    request = context.get("request")
    if request:
        currency = request.session.get("currency", settings.DEFAULT_CURRENCY)
    else:
        currency = settings.DEFAULT_CURRENCY

    return settings.CURRENCIES.get(currency, {}).get("symbol", "₸")
