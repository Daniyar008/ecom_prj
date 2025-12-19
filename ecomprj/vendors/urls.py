from django import views
from django.urls import path, include
from .views import (
    vendor_list_view,
    vendor_detail_view,
    vendor_register_view,
    vendor_login_view,
    vendor_logout_view,
    vendor_dashboard,
    vendor_products,
    vendor_add_product,
    vendor_edit_product,
    vendor_delete_product,
    vendor_orders,
    vendor_reviews,
    vendor_settings,
)

app_name = "vendors"

urlpatterns = [
    # Public views
    path("", vendor_list_view, name="vendor-list"),
    # Vendor Auth
    path("register/", vendor_register_view, name="vendor-register"),
    path("login/", vendor_login_view, name="vendor-login"),
    path("logout/", vendor_logout_view, name="vendor-logout"),
    # Vendor Dashboard
    path("dashboard/", vendor_dashboard, name="vendor-dashboard"),
    path("dashboard/products/", vendor_products, name="vendor-products"),
    path("dashboard/products/add/", vendor_add_product, name="vendor-add-product"),
    path(
        "dashboard/products/edit/<pid>/",
        vendor_edit_product,
        name="vendor-edit-product",
    ),
    path(
        "dashboard/products/delete/<pid>/",
        vendor_delete_product,
        name="vendor-delete-product",
    ),
    path("dashboard/orders/", vendor_orders, name="vendor-orders"),
    path("dashboard/reviews/", vendor_reviews, name="vendor-reviews"),
    path("dashboard/settings/", vendor_settings, name="vendor-settings"),
    # Vendor detail - MUST BE LAST (catches all <vid>/)
    path("<vid>/", vendor_detail_view, name="vendor-detail"),
]
