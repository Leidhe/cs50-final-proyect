from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Category, Course
from .forms import CourseForm, CourseEditForm


def index(request):
    if request.method == "GET":
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
    return render(request, "courses/index.html", context)

# For searches in the search bar by name or creator

# Search courses with the search engine


def search(request):
    if request.method == "POST":
        categories = search_categories()
        text = request.POST.get("search")
        courses_by_name = Course.objects.filter(name__contains=text)
        courses_by_creator = Course.objects.filter(
            author__username__contains=text)

        context = {
            'courses_by_name': courses_by_name,
            'courses_by_creator': courses_by_creator,
            'text': text,
            'categories': categories
        }
        return render(request, "courses/search.html", context)
    render(request, "courses/error.html", {'error': "Method not allowed", })

# Search by category button


def search_by_category(request, category_id):
    if request.method == "GET":
        try:
            categories = search_categories()
            category = Category.objects.get(pk=category_id)
            courses = Course.objects.filter(categories=category)
            text = f'category {category.name}'
            context = {
                'courses_by_name': courses,
                'text': text,
                'categories': categories

            }
            return render(request, "courses/search.html", context)
        except Category.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Category doesn't exist", })

    render(request, "courses/error.html", {'error': "Method not allowed", })


# Description of the selected course
def course(request, course_id):
    if request.method == "GET":
        try:
            categories = search_categories()
            course = Course.objects.get(pk=course_id)
            context = {
                'course': course,
                'categories': categories
            }
            return render(request, "courses/course.html", context)
        except Course.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Course doesn't exist", })

    return render(request, "courses/error.html", {'error': "Method not allowed", })

# Access to the view of a teacher


def teacher(request):
    if request.method == "GET":
        categories = search_categories()
        courses_created = Course.objects.filter(author=request.user)
        context = {
            'categories': categories,
            'courses_created': courses_created
        }
        return render(request, "courses/teacher.html", context)
    return render(request, "courses/error.html", {'error': "Method not allowed", })


def create_course(request):
    if request.method == "GET":
        form = CourseForm()
        return render(request, 'courses/createcourse.html', {'form': form})
    else:
        form = CourseForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect(reverse('course', args=[course.pk]))
        return render(request, "courses/error.html", {'error': "Method not allowed", })


def edit_course(request, course_id):
    if request.method == "GET":
        instance = get_object_or_404(Course, id=course_id)
        form = CourseEditForm(instance=instance)
        return render(request, 'courses/editcourse.html', {'form': form})
    else:
        instance = get_object_or_404(Course, id=course_id)
        form = CourseEditForm(request.POST or None,
                              request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
            context = {
                'course': instance
            }
            return render(request, 'courses/course_settings.html', context)
        return render(request, "courses/error.html", {'error': "Method not allowed", })


def course_details(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Course doesn't exist", })

    context = {
        'course': course
    }
    return render(request, 'courses/course_settings.html', context)


def search_categories():
    categories = Category.objects.all()
    return categories
