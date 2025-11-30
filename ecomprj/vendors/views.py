from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from requests import session
import stripe
from taggit.models import Tag

from .models import Vendor
from goods.models import Product



def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request, "vendors/vendor-list.html", context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published").order_by("-id")

    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "vendors/vendor-detail.html", context)
















