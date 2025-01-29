from django.urls import path, include

from . import views

from django_email_verification import urls as email_urls  # include the urls

urlpatterns = [
    path('login_user', views.login_user, name = "login"),
    path('register_user', views.register_user, name = "register_user"),
    path('logout_view', views.logout_view, name = "logout"),
    path('homeai', views.homeai, name = "homeai"),
    path('verification/', include('verify_email.urls')),
    path('password', views.password, name = "password"),
    path('email/', include(email_urls)),  # connect them to an arbitrary path
]