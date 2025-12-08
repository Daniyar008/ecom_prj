from django import views
from django.urls import path, include
from .views import create_checkout_session, save_checkout_info, add_to_cart, cart_view, checkout, delete_item_from_cart, make_address_default, order_detail, payment_completed_view, payment_failed_view, update_cart

app_name = "cartorder"

urlpatterns = [

    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("cart/", cart_view, name="cart"),
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    path("update-cart/", update_cart, name="update-cart"),
    path("api/create_checkout_session/<oid>/", create_checkout_session, name="api_checkout_session"),
    path("save_checkout_info/", save_checkout_info, name="save_checkout_info"),
    path("checkout/<oid>/", checkout, name="checkout"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path("payment-completed/<oid>/", payment_completed_view, name="payment-completed"),
    path("payment-failed/", payment_failed_view, name="payment-failed"),
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),
    path("make-default-address/", make_address_default, name="make-default-address"),
]