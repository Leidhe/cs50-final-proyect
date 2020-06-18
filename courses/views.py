from django.shortcuts import render, redirect
from .models import Category, Course


def index(request):
    if request.method == "GET":
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
    return render(request, "courses/index.html", context)

# For searches in the search bar by name or creator


def search(request):
    if request.method == "POST":
        text = request.POST.get("search")
        courses_by_name = Course.objects.filter(name__contains=text)
        courses_by_creator = Course.objects.filter(
            author__username__contains=text)
        context = {
            'courses_by_name': courses_by_name,
            'courses_by_creator': courses_by_creator,
            'text': text,
        }
        return render(request, "courses/search.html", context)
    render(request, "courses/error.html", {'error': "Method not allowed", })


def course(request, course_id):
    if request.method == "GET":
        try:
            print("hola")
            course = Course.objects.get(pk=course_id)
            context = {
                'course': course,
            }
            return render(request, "courses/course.html", context)
        except Course.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Course doesn't exist", })

    return render(request, "courses/error.html", {'error': "Method not allowed", })
