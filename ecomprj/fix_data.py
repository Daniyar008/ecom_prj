# Fix category data script
import os
import sys
import django

# Setup Django
sys.path.insert(0, r"F:\Deploy proj\ecom_prj\ecomprj")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecomprj.settings")
django.setup()

from goods.models import Category, Product

# Correct category data by ID
categories_data = {
    1: {"en": "Electronics", "kk": "Электроника", "ru": "Электроника"},
    2: {"en": "Mens Fashion", "kk": "Ерлер сәні", "ru": "Мужская мода"},
    3: {"en": "Womens Fashion", "kk": "Әйелдер сәні", "ru": "Женская мода"},
    4: {"en": "Furniture", "kk": "Жиһаз", "ru": "Мебель"},
    5: {"en": "Home Decor", "kk": "Үй безендіру", "ru": "Декор для дома"},
    6: {
        "en": "Fruits and Vegetables",
        "kk": "Жемістер мен көкөністер",
        "ru": "Фрукты и овощи",
    },
    7: {
        "en": "Organic Foods",
        "kk": "Органикалық тағам",
        "ru": "Органические продукты",
    },
    8: {
        "en": "Beauty and Makeup",
        "kk": "Сұлулық және макияж",
        "ru": "Красота и макияж",
    },
    9: {"en": "Skincare", "kk": "Тері күтімі", "ru": "Уход за кожей"},
    10: {"en": "Sports and Fitness", "kk": "Спорт және фитнес", "ru": "Спорт и фитнес"},
    11: {"en": "Books and Media", "kk": "Кітаптар мен медиа", "ru": "Книги и медиа"},
    12: {"en": "Jewelry", "kk": "Зергерлік бұйымдар", "ru": "Ювелирные изделия"},
    13: {"en": "Auto Parts", "kk": "Авто бөлшектер", "ru": "Автозапчасти"},
    14: {
        "en": "Toys and Games",
        "kk": "Ойыншықтар мен ойындар",
        "ru": "Игрушки и игры",
    },
    15: {
        "en": "Pet Supplies",
        "kk": "Үй жануарларына арналған",
        "ru": "Товары для животных",
    },
}

print("Fixing categories...")
for cat_id, translations in categories_data.items():
    try:
        cat = Category.objects.get(id=cat_id)
        cat.title_en = translations["en"]
        cat.title_kk = translations["kk"]
        cat.title_ru = translations["ru"]
        cat.save()
        print(f"  Updated category {cat_id}: {translations['en']}")
    except Category.DoesNotExist:
        print(f"  Category {cat_id} not found")

print("\nFixing products - restoring English titles...")
# Fix products - the issue is they all say "Fresh Pear"
# Need to restore from fixture or original data
products_fixed = 0
for product in Product.objects.all():
    # Copy the original title to all language fields
    if product.title_en and product.title_en != "Fresh Pear":
        # Already has correct English title
        if not product.title_kk or product.title_kk == "Fresh Pear":
            product.title_kk = product.title_en
        if not product.title_ru or product.title_ru == "Fresh Pear":
            product.title_ru = product.title_en
        product.save()
        products_fixed += 1

print(f"  Fixed {products_fixed} products")
print("\nDone!")
