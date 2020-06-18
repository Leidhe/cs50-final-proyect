from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path('course/<int:course_id>', views.course, name="course"),

]