# Fix images in database - update paths to actual files
import os
import sys
import django

sys.path.insert(0, r"F:\Deploy proj\ecom_prj\ecomprj")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecomprj.settings")
django.setup()

from goods.models import Product, Category

# Map category titles to image files
category_images = {
    "Electronics": "category/Electronics.jfif",
    "Mens Fashion": "category/Mens_Fashion.jfif",
    "Womens Fashion": "category/Womens_Fashion.jfif",
    "Furniture": "category/Furniture.jfif",
    "Home Decor": "category/Home_Decor.jfif",
    "Fruits and Vegetables": "category/Fruits__Vegetables.jfif",
    "Organic Foods": "category/Organic_Foods.jfif",
    "Beauty and Makeup": "category/Beauty__Makeup.jfif",
    "Skincare": "category/Skincare.jfif",
    "Sports and Fitness": "category/Sports__Fitness.jfif",
    "Books and Media": "category/Books__Media.jfif",
    "Jewelry": "category/Jewelry.jfif",
    "Auto Parts": "category/Auto_Parts.jfif",
    "Toys and Games": "category/Toys__Games.jfif",
    "Pet Supplies": "category/Pet_Supplies.jfif",
}

print("Fixing category images...")
for cat in Category.objects.all():
    title = cat.title_en
    if title in category_images:
        cat.image = category_images[title]
        cat.save()
        print(f"  Updated: {title} -> {category_images[title]}")
    else:
        print(f"  No image mapping for: {title}")

print("\nFixing product images...")
media_path = r"F:\Deploy proj\ecom_prj\ecomprj\media\product-images"

for product in Product.objects.all():
    pid = product.pid
    product_folder = os.path.join(media_path, pid)

    if os.path.exists(product_folder):
        # Find first image in folder
        images = [
            f
            for f in os.listdir(product_folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".jfif", ".webp"))
        ]
        if images:
            image_path = f"product-images/{pid}/{images[0]}"
            product.image = image_path
            product.save()
            print(f"  Updated: {product.title_en[:30]} -> {image_path}")
        else:
            print(f"  No images in folder for: {pid}")
    else:
        print(f"  Folder not found for: {pid}")

print("\nDone!")
