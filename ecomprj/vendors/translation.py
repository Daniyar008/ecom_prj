from modeltranslation.translator import register, TranslationOptions
from .models import Vendor


@register(Vendor)
class VendorTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )
