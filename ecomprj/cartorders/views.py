from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
import stripe
from django.template.loader import render_to_string
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Coupon, CartOrder, CartOrderProducts, Address
from django.utils.translation import gettext as _
from goods.models import Product


def add_to_cart(request):
    cart_product = {}
    product_id = str(request.GET.get("id", ""))

    if not product_id:
        return JsonResponse({"error": _("Product ID is required")}, status=400)

    cart_product[product_id] = {
        "title": request.GET.get("title", ""),
        "qty": int(request.GET.get("qty", 1)),
        "price": float(request.GET.get("price", 0)),
        "image": request.GET.get("image", ""),
        "pid": request.GET.get("pid", ""),
    }

    if "cart_data_obj" in request.session:
        if product_id in request.session["cart_data_obj"]:
            # Update quantity if product already in cart
            current_qty = int(request.session["cart_data_obj"][product_id]["qty"])
            new_qty = int(request.GET.get("qty", 1))
            request.session["cart_data_obj"][product_id]["qty"] = current_qty + new_qty
        else:
            # Add new product to cart
            request.session["cart_data_obj"].update(cart_product)
    else:
        request.session["cart_data_obj"] = cart_product

    # CRITICAL: Mark session as modified so Django saves it
    request.session.modified = True

    return JsonResponse(
        {
            "data": request.session["cart_data_obj"],
            "totalcartitems": len(request.session["cart_data_obj"]),
        }
    )


def cart_view(request):
    cart_total_amount = 0
    if "cart_data_obj" in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            cart_total_amount += int(item["qty"]) * float(item["price"])
        return render(
            request,
            "cartorders/cart.html",
            {
                "cart_data": request.session["cart_data_obj"],
                "totalcartitems": len(request.session["cart_data_obj"]),
                "cart_total_amount": cart_total_amount,
            },
        )
    else:
        messages.warning(request, _("Your cart is empty"))
        return redirect("core:index")


def delete_item_from_cart(request):
    product_id = str(request.GET.get("id", ""))

    if "cart_data_obj" in request.session:
        if product_id in request.session["cart_data_obj"]:
            del request.session["cart_data_obj"][product_id]
            # Mark session as modified
            request.session.modified = True

    cart_total_amount = 0
    if "cart_data_obj" in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            cart_total_amount += int(item["qty"]) * float(item["price"])

    context = render_to_string(
        "cartorders/async/cart-list.html",
        {
            "cart_data": request.session["cart_data_obj"],
            "totalcartitems": len(request.session["cart_data_obj"]),
            "cart_total_amount": cart_total_amount,
        },
    )
    return JsonResponse(
        {"data": context, "totalcartitems": len(request.session["cart_data_obj"])}
    )


def update_cart(request):
    product_id = str(request.GET.get("id", ""))
    try:
        product_qty = int(request.GET.get("qty", 1))
        # Ensure quantity is at least 1
        if product_qty < 1:
            product_qty = 1
    except (ValueError, TypeError):
        product_qty = 1

    if "cart_data_obj" in request.session:
        if product_id in request.session["cart_data_obj"]:
            request.session["cart_data_obj"][product_id]["qty"] = product_qty
            # Mark session as modified
            request.session.modified = True

    cart_total_amount = 0
    if "cart_data_obj" in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            cart_total_amount += int(item["qty"]) * float(item["price"])

    context = render_to_string(
        "cartorders/async/cart-list.html",
        {
            "cart_data": request.session["cart_data_obj"],
            "totalcartitems": len(request.session["cart_data_obj"]),
            "cart_total_amount": cart_total_amount,
        },
    )
    return JsonResponse(
        {"data": context, "totalcartitems": len(request.session["cart_data_obj"])}
    )


def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        print(full_name)
        print(email)
        print(mobile)
        print(address)
        print(city)
        print(state)
        print(country)

        request.session["full_name"] = full_name
        request.session["email"] = email
        request.session["mobile"] = mobile
        request.session["address"] = address
        request.session["city"] = city
        request.session["state"] = state
        request.session["country"] = country

        if "cart_data_obj" in request.session:

            # Getting total amount for Paypal Amount
            for p_id, item in request.session["cart_data_obj"].items():
                total_amount += int(item["qty"]) * float(item["price"])

            full_name = request.session["full_name"]
            email = request.session["email"]
            phone = request.session["mobile"]
            address = request.session["address"]
            city = request.session["city"]
            state = request.session["state"]
            country = request.session["country"]

            # Create ORder Object
            order = CartOrder.objects.create(
                user=request.user,
                price=total_amount,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                country=country,
            )

            del request.session["full_name"]
            del request.session["email"]
            del request.session["mobile"]
            del request.session["address"]
            del request.session["city"]
            del request.session["state"]
            del request.session["country"]

            # Getting total amount for The Cart
            for p_id, item in request.session["cart_data_obj"].items():
                cart_total_amount += int(item["qty"]) * float(item["price"])

                cart_order_products = CartOrderProducts.objects.create(
                    order=order,
                    invoice_no="INVOICE_NO-" + str(order.id),  # INVOICE_NO-5,
                    item=item["title"],
                    image=item["image"],
                    qty=item["qty"],
                    price=item["price"],
                    total=float(item["qty"]) * float(item["price"]),
                )

        return redirect("cartorder:checkout", order.oid)
    return redirect("cartorder:checkout", order.oid)


@csrf_exempt
def create_checkout_session(request, oid):
    order = CartOrder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=order.email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "USD",
                    "product_data": {"name": order.full_name},
                    "unit_amount": int(order.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("cartorder:payment-completed", args=[order.oid])
        )
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse(":payment-completed", args=[order.oid])
        ),
    )

    order.paid_status = False
    order.stripe_payment_intent = checkout_session["id"]
    order.save()

    print("checkkout session", checkout_session)
    return JsonResponse({"sessionId": checkout_session.id})


@login_required
def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderProducts.objects.filter(order=order)

    if request.method == "POST":
        code = request.POST.get("code")
        print("code ========", code)
        coupon = Coupon.objects.filter(code=code, active=True).first()
        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request, _("Coupon already activated"))
                return redirect("cartorder:checkout", order.oid)
            else:
                discount = order.price * coupon.discount / 100

                order.coupons.add(coupon)
                order.price -= discount
                order.saved += discount
                order.save()

                messages.success(request, _("Coupon Activated"))
                return redirect("cartorder:checkout", order.oid)
        else:
            messages.error(request, _("Coupon Does Not Exists"))

    context = {
        "order": order,
        "order_items": order_items,
        "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, "cartorders/checkout.html", context)


@login_required
def payment_completed_view(request, oid):
    order = CartOrder.objects.get(oid=oid)

    if order.paid_status == False:
        order.paid_status = True
        order.save()

    context = {
        "order": order,
        "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, "cartorders/payment-completed.html", context)


@login_required
def payment_failed_view(request):
    return render(request, "cartorders/payment-failed.html")


def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderProducts.objects.filter(order=order)

    context = {
        "order_items": order_items,
    }
    return render(request, "cartorders/order-detail.html", context)


def make_address_default(request):
    id = request.GET["id"]
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})
