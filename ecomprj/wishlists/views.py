from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from requests import session
import stripe
from taggit.models import Tag
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import Wishlist
from goods.models import Product


@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {"w": wishlist}
    return render(request, "wishlists/wishlist.html", context)


@login_required(login_url="userauths:sign-in")
def add_to_wishlist(request):
    try:
        product_id = request.GET.get("id", "")
        if not product_id:
            return JsonResponse({"error": "Product ID is required"}, status=400)

        product = Product.objects.get(id=product_id)

        # Check if already in wishlist
        wishlist_exists = Wishlist.objects.filter(
            product=product, user=request.user
        ).exists()

        if not wishlist_exists:
            Wishlist.objects.create(
                user=request.user,
                product=product,
            )

        return JsonResponse({"bool": True, "message": "Added to wishlist"})

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# def remove_wishlist(request):
#     pid = request.GET['id']
#     wishlist = wishlist_model.objects.filter(user=request.user).values()

#     product = wishlist_model.objects.get(id=pid)
#     h = product.delete()

#     context = {
#         "bool": True,
#         "wishlist":wishlist
#     }
#     t = render_to_string("core/async/wishlist-list.html", context)
#     return JsonResponse({"data": t, "w":wishlist})


@login_required(login_url="userauths:sign-in")
def remove_wishlist(request):
    try:
        wishlist_id = request.GET.get("id", "")
        if not wishlist_id:
            return JsonResponse({"error": "Wishlist ID is required"}, status=400)

        wishlist_item = Wishlist.objects.get(id=wishlist_id, user=request.user)
        wishlist_item.delete()

        # Get remaining wishlist items
        wishlist = Wishlist.objects.filter(user=request.user)
        wishlist_json = serializers.serialize("json", wishlist)
        context = {"bool": True, "w": wishlist}

        t = render_to_string("wishlists/async/wishlist-list.html", context)
        return JsonResponse({"data": t, "w": wishlist_json})

    except Wishlist.DoesNotExist:
        return JsonResponse({"error": "Wishlist item not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
