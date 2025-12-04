from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone

from vendors.models import Vendor



STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)


RATING = (
    (1,  "★☆☆☆☆"),
    (2,  "★★☆☆☆"),
    (3,  "★★★☆☆"),
    (4,  "★★★★☆"),
    (5,  "★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def product_count(self):
        return Product.objects.filter(category=self).count()

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass



class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10,
                         max_length=20, alphabet="abcdefgh12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, related_name="product")

    title = models.CharField(max_length=100, default="Fresh Pear")
    image = models.ImageField(
        upload_to=user_directory_path, default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="This is the product")
    description = CKEditor5Field(config_name='extends', null=True, blank=True)

    price = models.DecimalField(
        max_digits=12, decimal_places=2, default="0.00")
    old_price = models.DecimalField(
        max_digits=12, decimal_places=2, default="2.99")

    specifications = CKEditor5Field(config_name='extends', null=True, blank=True)
    # specifications = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=100, default="Organic", null=True, blank=True)
    stock_count = models.CharField(
        max_length=100, default="10", null=True, blank=True)
    life = models.CharField(
        max_length=100, default="100 Days", null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    tags = TaggableManager(blank=True)

    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10,
                         prefix="sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(
        upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(
        Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"



class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        if self.product:
            return self.product.title
        else:
            return f"review - {self.pk}"

    def get_rating(self):
        return self.rating