from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("search_category/<int:category_id>", views.search_by_category, name="search_category"),
    path('course/<int:course_id>', views.course, name="course"),
    path('teacher/', views.teacher, name="teacher"),
    path('teacher/create_course', views.create_course, name='create_course'),
    path('teacher/course_details/<int:course_id>', views.course_details, name='course_details'),
    path('teacher/edit_course/<int:course_id>', views.edit_course, name='edit_course'),

]