from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("search_category/<int:category_id>", views.search_by_category, name="search_category"),
    path('mycourses/', views.mycourses, name="mycourses"),
    path('myaccount/', views.account, name="myaccount"),
    path('password/', views.change_password, name="password"),

    path('edit_account/', views.edit_account, name="edit_account"),
    path('course/<int:course_id>', views.course, name="course"),
    path('enroll_course/<int:course_id>', views.enroll_course, name="enroll_course"),
    path('teacher/', views.teacher, name="teacher"),
    path('grades/<int:course_id>', views.grades, name="grades"),


    #Courses
    path('create_course', views.create_course, name='create_course'),
    path('course_details/<int:course_id>', views.course_details, name='course_details'),
    path('edit_course/<int:course_id>', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),


    #Units
    path('create_unit/<int:course_id>', views.create_unit, name='create_unit'),
    path('edit_unit/<int:course_id>/<int:unit_id>', views.edit_unit, name='edit_unit'),
    path('delete_unit/<int:unit_id>', views.delete_unit, name="delete_unit"),

    
    #Sections
    path('view_section/<int:section_id>', views.view_section, name="view_section"),
    path('create_section/<int:course_id>/<int:unit_id>', views.create_section, name='create_section'),
    path('edit_section/<int:section_id>', views.edit_section, name='edit_section'),
    path('delete_section/<int:section_id>', views.delete_section, name="delete_section"),


    #Tasks
    path('view_task/<int:task_id>', views.view_task, name="view_task"),
    path('review_task/<int:task_id>/<int:homework_id>', views.review_task, name="review_task"),
    path('create_task/<int:course_id>/<int:unit_id>', views.create_task, name='create_task'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('correction/<int:user_id>/<int:task_id>/<int:homework_id>', views.correction, name='correction'),
    path('delete_file/', views.delete_file, name="delete_file"),
    path('delete_task/<int:task_id>', views.delete_task, name="delete_task"),




    path('list_students/<int:course_id>', views.list_students, name="list_students"),

]