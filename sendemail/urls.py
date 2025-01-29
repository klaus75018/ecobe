from django.urls import path

from . import views

app_name = "sendemail"

urlpatterns = [
    path("form1/", views.form1, name="form1"),
    path("success1/", views.success1, name="success1"),
]