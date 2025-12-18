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
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),
    # Vendor Auth
    path("vendor/register/", vendor_register_view, name="vendor-register"),
    path("vendor/login/", vendor_login_view, name="vendor-login"),
    path("vendor/logout/", vendor_logout_view, name="vendor-logout"),
    # Vendor Dashboard
    path("vendor/dashboard/", vendor_dashboard, name="vendor-dashboard"),
    path("vendor/dashboard/products/", vendor_products, name="vendor-products"),
    path(
        "vendor/dashboard/products/add/", vendor_add_product, name="vendor-add-product"
    ),
    path(
        "vendor/dashboard/products/edit/<pid>/",
        vendor_edit_product,
        name="vendor-edit-product",
    ),
    path(
        "vendor/dashboard/products/delete/<pid>/",
        vendor_delete_product,
        name="vendor-delete-product",
    ),
    path("vendor/dashboard/orders/", vendor_orders, name="vendor-orders"),
    path("vendor/dashboard/reviews/", vendor_reviews, name="vendor-reviews"),
    path("vendor/dashboard/settings/", vendor_settings, name="vendor-settings"),
]
