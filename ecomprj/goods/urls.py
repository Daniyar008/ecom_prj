from django.shortcuts import render

from django import views
from django.urls import path, include
from .views import product_list_view, product_detail_view, category_list_view, category_product_list__view, tag_list, ajax_add_review, search_view

app_name = "catalog"

urlpatterns = [

    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list__view, name="category-product-list"),
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),
    path("search/", search_view, name="search"),

]
