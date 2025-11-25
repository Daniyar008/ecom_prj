from django import views
from django.urls import path, include
from .views import ajax_contact_form, customer_dashboard, index, contact, about_us, purchase_guide, privacy_policy, terms_of_service

app_name = "core"

urlpatterns = [

    path("", index, name="index"),
    path("about_us/", about_us, name="about_us"),
    path("purchase_guide/", purchase_guide, name="purchase_guide"),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    path("terms_of_service/", terms_of_service, name="terms_of_service"),
    
    path("dashboard/", customer_dashboard, name="dashboard"),
    path("contact/", contact, name="contact"),
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),

]