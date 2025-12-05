from django import views
from django.urls import path, include
from .views import add_to_wishlist, wishlist_view, remove_wishlist


app_name = "wishlist"
urlpatterns = [
    path("wishlist/", wishlist_view, name="wishlist"),
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),
]