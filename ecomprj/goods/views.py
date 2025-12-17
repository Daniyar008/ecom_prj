from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from taggit.models import Tag
from django.template.loader import render_to_string
from django.db.models import Count, Avg
from django.db.models import Q, F

from .models import Product, Category, ProductImages, ProductReview
from django.utils.translation import gettext_lazy as _
from cartorders.models import Address
from .forms import ProductReviewForm


def product_list_view(request, category_cid=None):
    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", "-date")
    query = request.GET.get("q", None)
    min_price = request.GET.get("min_price", None)
    max_price = request.GET.get("max_price", None)
    category_filter = request.GET.getlist("category[]")
    vendor_filter = request.GET.getlist("vendor[]")

    if category_cid == "all" or not category_cid:
        products = Product.objects.filter(product_status="published")
    elif query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            product_status="published",
        )
    else:
        # Фильтрация по категории
        category = get_object_or_404(Category, cid=category_cid)
        products = Product.objects.filter(category=category, product_status="published")

    # Применяем дополнительные фильтры
    if on_sale:
        products = products.filter(old_price__gt=F("price"))

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass

    if category_filter:
        products = products.filter(category__id__in=category_filter)

    if vendor_filter:
        products = products.filter(vendor__id__in=vendor_filter)

    valid_order_fields = ["-date", "date", "price", "-price", "title", "-title"]
    if order_by in valid_order_fields:
        products = products.order_by(order_by)
    else:
        products = products.order_by("-date")

    categories = Category.objects.all()

    tags = Tag.objects.all().order_by("-id")[:6]

    from django.db.models import Min, Max

    price_range = products.aggregate(min_price=Min("price"), max_price=Max("price"))

    context = {
        "products": products,
        "tags": tags,
        "categories": categories,
        "current_category": category_cid if category_cid else None,
        "query": query,
        "on_sale": on_sale,
        "order_by": order_by,
        "min_price_filter": min_price,
        "max_price_filter": max_price,
        "selected_categories": category_filter,
        "selected_vendors": vendor_filter,
        "price_range": price_range,
        "title": _("Product Catalog"),
    }

    return render(request, "goods/product-list.html", context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {"categories": categories}
    return render(request, "goods/category-list.html", context)


def category_product_list__view(request, cid):

    category = Category.objects.get(cid=cid)  # food, Cosmetics
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "goods/category-product-list.html", context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    # product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    # Product Review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        # address = Address.objects.get(status=True, user=request.user)
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product
        ).count()

        if user_review_count > 0:
            make_review = False

    address = "Login To Continue"

    p_image = product.p_images.all()

    context = {
        "p": product,
        # "address": address,
        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products": products,
    }

    return render(request, "goods/product-detail.html", context)


def tag_list(request, tag_slug=None):

    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {"products": products, "tag": tag}

    return render(request, "goods/tag.html", context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )

    context = {
        "user": user.username,
        "review": request.POST["review"],
        "rating": request.POST["rating"],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    return JsonResponse(
        {"bool": True, "context": context, "average_reviews": average_reviews}
    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "goods/search.html", context)


# def filter_product(request):
#     categories = request.GET.getlist("category[]")
#     vendors = request.GET.getlist("vendor[]")


#     min_price = request.GET['min_price']
#     max_price = request.GET['max_price']

#     products = Product.objects.filter(product_status="published").order_by("-id").distinct()

#     products = products.filter(price__gte=min_price)
#     products = products.filter(price__lte=max_price)


#     if len(categories) > 0:
#         products = products.filter(category__id__in=categories).distinct()
#     else:
#         products = Product.objects.filter(product_status="published").order_by("-id").distinct()
#     if len(vendors) > 0:
#         products = products.filter(vendor__id__in=vendors).distinct()
#     else:
#         products = Product.objects.filter(product_status="published").order_by("-id").distinct()


#     data = render_to_string("goods/async/product-list.html", {"products": products})
#     return JsonResponse({"data": data})
