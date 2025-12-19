# =============================================================================
# Fix translations for categories and products
# =============================================================================
from django.core.management.base import BaseCommand
from goods.models import Category, Product


class Command(BaseCommand):
    help = "Fix translations for categories and products"

    def handle(self, *args, **options):
        self.stdout.write("Fixing category translations...")

        # Category translations (EN -> KK, RU)
        category_translations = {
            "Electronics": {"kk": "Электроника", "ru": "Электроника"},
            "Men's Fashion": {"kk": "Ерлер сәні", "ru": "Мужская мода"},
            "Women's Fashion": {"kk": "Әйелдер сәні", "ru": "Женская мода"},
            "Furniture": {"kk": "Жиһаз", "ru": "Мебель"},
            "Home Decor": {"kk": "Үй безендіру", "ru": "Декор для дома"},
            "Fruits & Vegetables": {
                "kk": "Жемістер мен көкөністер",
                "ru": "Фрукты и овощи",
            },
            "Organic Foods": {"kk": "Органикалық тағам", "ru": "Органические продукты"},
            "Beauty & Makeup": {"kk": "Сұлулық және макияж", "ru": "Красота и макияж"},
            "Skincare": {"kk": "Тері күтімі", "ru": "Уход за кожей"},
            "Sports & Fitness": {"kk": "Спорт және фитнес", "ru": "Спорт и фитнес"},
            "Books & Media": {"kk": "Кітаптар мен медиа", "ru": "Книги и медиа"},
            "Jewelry": {"kk": "Зергерлік бұйымдар", "ru": "Ювелирные изделия"},
            "Auto Parts": {"kk": "Авто бөлшектер", "ru": "Автозапчасти"},
            "Toys & Games": {"kk": "Ойыншықтар мен ойындар", "ru": "Игрушки и игры"},
            "Pet Supplies": {
                "kk": "Үй жануарларына арналған",
                "ru": "Товары для животных",
            },
            "Food": {"kk": "Тағам", "ru": "Еда"},
        }

        for cat in Category.objects.all():
            # Get original English title
            original_title = cat.title_en or cat.title

            if original_title in category_translations:
                trans = category_translations[original_title]
                cat.title_en = original_title
                cat.title_kk = trans["kk"]
                cat.title_ru = trans["ru"]
                cat.save()
                self.stdout.write(
                    f"  Updated: {original_title} -> KK: {trans['kk']}, RU: {trans['ru']}"
                )
            else:
                # If no translation found, at least copy English to other fields
                cat.title_en = original_title
                cat.title_kk = original_title
                cat.title_ru = original_title
                cat.save()
                self.stdout.write(
                    f"  No translation for: {original_title}, kept English"
                )

        self.stdout.write(self.style.SUCCESS("Category translations fixed!"))

        # Fix product translations - copy title_en to other fields if they match wrong data
        self.stdout.write("\nFixing product translations...")

        products_fixed = 0
        for product in Product.objects.all():
            original_title = product.title_en or product.title

            # If all language fields have same wrong value, reset to English
            if (
                product.title_kk == product.title_ru
                and product.title_kk != original_title
            ):
                product.title_en = original_title
                product.title_kk = original_title  # Keep English for now
                product.title_ru = original_title  # Keep English for now
                product.save()
                products_fixed += 1

        self.stdout.write(
            self.style.SUCCESS(f"Fixed {products_fixed} product translations!")
        )
