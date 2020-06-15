from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.sign_in, name="sign_in"),
    path("logout/", views.fun_logout, name="logout"),
]