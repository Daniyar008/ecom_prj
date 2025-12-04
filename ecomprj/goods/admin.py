from django.contrib import admin

from .models import Product, Category, ProductImages, ProductReview


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_editable = ['title', 'price', 'featured', 'product_status']
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'vendor', 'featured', 'product_status', 'pid']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']