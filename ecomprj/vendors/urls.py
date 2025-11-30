from django import views
from django.urls import path, include
from .views import vendor_list_view, vendor_detail_view

app_name = "vendors"

urlpatterns = [
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),
]