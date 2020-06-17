from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search_bar", views.search_bar, name="search_bar"),
]