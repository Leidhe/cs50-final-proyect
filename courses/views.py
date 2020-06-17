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


def search_bar(request):
    if request.method == "POST":
        text = request.POST.get("search")
        courses_by_name = Course.objects.filter(name__contains=text)
        courses_by_creator = Course.objects.filter(author__username__contains=text)
        context = {
            'courses_by_name': courses_by_name,
            'courses_by_creator': courses_by_creator,
            'text': text,
        }
    return render(request, "courses/search.html", context)
