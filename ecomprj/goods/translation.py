# =============================================================================
# Model Translation Configuration for Goods App
# =============================================================================
from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product


class CategoryTranslationOptions(TranslationOptions):
    """
    Translation options for Category model.
    Only title field needs translation.
    """

    fields = ("title",)


class ProductTranslationOptions(TranslationOptions):
    """
    Translation options for Product model.
    Vendor name is NOT translated - it stays as-is.
    Note: description and specifications are CKEditor5Field which is not supported by modeltranslation
    """

    fields = (
        "title",  # Product name
        "type",  # Product type (e.g., "Organic")
        "life",  # Shelf life
    )


# Register translations
translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
