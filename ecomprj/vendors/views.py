from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from requests import session
import stripe
from taggit.models import Tag

from .models import Vendor
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from goods.models import Product


def vendor_list_view(request):
    # Search and pagination parameters
    q = request.GET.get("q", "").strip()
    per_page = request.GET.get("per_page", "50")
    try:
        per_page_int = int(per_page)
    except (ValueError, TypeError):
        per_page_int = 50

    vendors_qs = Vendor.objects.all().order_by("-id")
    if q:
        vendors_qs = vendors_qs.filter(Q(title__icontains=q) | Q(vid__icontains=q))

    page = request.GET.get("page", 1)
    # If per_page <= 0 use all items
    if per_page_int <= 0:
        per_page_int = max(1, vendors_qs.count() or 1)

    paginator = Paginator(vendors_qs, per_page_int)
    try:
        vendors = paginator.page(page)
    except PageNotAnInteger:
        vendors = paginator.page(1)
    except EmptyPage:
        vendors = paginator.page(paginator.num_pages)

    context = {
        "vendors": vendors,
        "vendors_count": vendors_qs.count(),
        "q": q,
        "per_page": per_page_int,
    }
    return render(request, "vendors/vendor-list.html", context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    # products pagination and per_page selector
    per_page = request.GET.get("per_page", "50")
    try:
        per_page_int = int(per_page)
    except (ValueError, TypeError):
        per_page_int = 50

    products_qs = Product.objects.filter(
        vendor=vendor, product_status="published"
    ).order_by("-id")
    page = request.GET.get("page", 1)
    if per_page_int <= 0:
        per_page_int = max(1, products_qs.count() or 1)
    paginator = Paginator(products_qs, per_page_int)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "vendor": vendor,
        "products": products,
        "per_page": per_page_int,
    }
    return render(request, "vendors/vendor-detail.html", context)
