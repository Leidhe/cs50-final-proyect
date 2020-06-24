from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Category, Course, Unit, Section, Task, Homework, Attachment
from .forms import CourseForm, CourseEditForm, UnitForm, UnitEditForm, SectionForm, SectionEditForm, TaskForm, TaskEditForm, HomeworkForm
from django.views import View
from django.http import JsonResponse


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
        return render(request, "courses/teacher/teacher.html", context)
    return render(request, "courses/error.html", {'error': "Method not allowed", })

# When a teacher wants to create a course
def create_course(request):
    if request.method == "GET":
        form = CourseForm()
        return render(request, 'courses/teacher/create_course.html', {'form': form})
    else:
        form = CourseForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect(reverse('course', args=[course.pk]))
        return render(request, "courses/error.html", {'error': "Method not allowed", })

# When a teacher wants to edit a course
def edit_course(request, course_id):
    if request.method == "GET":
        instance = get_object_or_404(Course, id=course_id)
        form = CourseEditForm(instance=instance)
        return render(request, 'courses/teacher/edit_course.html', {'form': form})
    else:
        instance = get_object_or_404(Course, id=course_id)
        form = CourseEditForm(request.POST or None,
                              request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
            context = {
                'course': instance
            }
            return render(request, 'courses/teacher/course_settings.html', context)
        return render(request, "courses/error.html", {'error': "Method not allowed", })

# Show the units, tasks, etc. that the course has
def course_details(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        units = Unit.objects.filter(course__id=course_id)

    except Course.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Course doesn't exist", })

    context = {
        'course': course,
        'units': units
    }
    return render(request, 'courses/teacher/course_settings.html', context)

# Create a unit inside of a course.
def create_unit(request, course_id):
    if request.method == "GET":
        form = UnitForm(course_id=course_id)
        context = {
            'form': form,
            'course_id': course_id
        }
        return render(request, 'courses/teacher/create_unit.html', context)
    else:
        try:
            form = UnitForm(request.POST, course_id=course_id)
            course = Course.objects.get(pk=course_id)

            if form.is_valid():
                if Unit.objects.filter(name=form.cleaned_data['name'], course=course).exists():
                    error = 'A unit already exists in the course with that name'
                    context = {
                    'form': form,
                    'course_id': course_id,
                    'error': error
                    }
                    return render(request, 'courses/teacher/create_unit.html', context)
                else:
                    unit=form.save(commit=False)
                    unit.author=request.user
                    unit.course=course
                    unit.save()
                    return redirect(reverse('course_details', args=[course_id]))

        except Course.DoesNotExist:
                    return render(request, "courses/error.html", {'error': "Course doesn't exist", })

        return render(request, "courses/error.html", {'error': "Method not allowed", })

# Edit a unit.
def edit_unit(request, course_id, unit_id):
    if request.method == "GET":
        instance=get_object_or_404(Unit, id=unit_id)
        form=UnitEditForm(course_id=course_id, instance=instance)
        return render(request, 'courses/teacher/edit_unit.html', {'form': form})
    else:
        instance=get_object_or_404(Unit, id=unit_id)
        form=UnitEditForm(request.POST or None,
                              request.FILES or None, course_id=course_id, instance=instance)
        if form.is_valid():
            try:
                course = Course.objects.get(pk=course_id)
                unit_exists = Unit.objects.filter(name=form.cleaned_data['name'], course=course)
                if unit_exists and unit_exists[0].id != unit_id:
                    error = 'A unit already exists in the course with that name'
                    context = {
                    'form': form,
                    'course_id': course_id,
                    'unit_id': unit_id,
                    'error': error
                    }
                    return render(request, 'courses/teacher/edit_unit.html', context)
                else:
                    form.save()
                    return redirect(reverse('course_details', args=[course_id]))
            except Course.DoesNotExist:
                    return render(request, "courses/error.html", {'error': "Course doesn't exist", })

            
        return render(request, "courses/error.html", {'error': "Method not allowed", })

def view_section(request, section_id):
    if request.method == "GET":
        try:
            section = Section.objects.get(pk=section_id)
            context = {
                'section':  section
            }
            return render(request, "courses/section.html", context)

        except Section.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Section doesn't exist", })


def view_task(request, task_id):
    if request.method == "GET":
        try:
            task = Task.objects.get(pk=task_id)
            homework = Homework.objects.filter(student=request.user, task=task_id).exists()

            form = HomeworkForm(user_id=request.user.id, task_id=task_id)
            context = {
                'form': form,
                'task': task,
            }
            return render(request, "courses/task.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", })
            
        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", })   
    else:
        try:
            task = Task.objects.get(pk=task_id)
            form = HomeworkForm(request.POST, request.FILES, user_id=request.user.id, task_id=task_id)
            
            print(form.errors)
            if form.is_valid():
                files = request.FILES.getlist('file_field')
                homework=form.save(commit=False)
                homework.student=request.user
                homework.task=task
                homework.save()
                for f in files:
                    Attachment.objects.create(file=f, homework=homework)
                return redirect('index')

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", })

def create_section(request, course_id, unit_id):
    if request.method == "GET":
        form = SectionForm(course_id=course_id, unit_id=unit_id)
        return render(request, 'courses/teacher/create_section.html', {'form': form})
    else:
        try:
            form = SectionForm(request.POST, course_id=course_id, unit_id=unit_id)
            unit = Unit.objects.get(pk=unit_id)

            if form.is_valid():
                if Section.objects.filter(name=form.cleaned_data['name'], unit=unit).exists():
                    error = 'A section already exists in the unit with that name'
                    context = {
                    'form': form,
                    'course_id': course_id,
                    'error': error
                    }
                    return render(request, 'courses/teacher/create_section.html', context)
                else:
                    section=form.save(commit=False)
                    section.author=request.user
                    section.unit=unit
                    section.save()
                    return redirect(reverse('course_details', args=[course_id]))

        except Unit.DoesNotExist:
                    return render(request, "courses/error.html", {'error': "Unit doesn't exist", })

        return render(request, "courses/error.html", {'error': "Method not allowed", })

def edit_section(request, section_id):
    if request.method == "GET":
        instance=get_object_or_404(Section, id=section_id)
        form=SectionEditForm(instance=instance)
        return render(request, 'courses/teacher/edit_section.html', {'form': form})
    else:
        instance=get_object_or_404(Section, id=section_id)
        form = SectionEditForm(request.POST,  instance=instance)
        if form.is_valid():
            section_exists = Section.objects.filter(name=form.cleaned_data['name'], unit=instance.unit)
            if section_exists and section_exists[0].id != section_id:
                error = 'A section already exists in the unit with that name'
                context = {
                'form': form,
                'error': error
                }
                return render(request, 'courses/teacher/edit_section.html', context)
            else:
                form.save()
                return redirect(reverse('view_section', args=[section_id]))
    

        return render(request, "courses/error.html", {'error': "Method not allowed", })


def create_task(request, course_id, unit_id):
    if request.method == "GET":
        form = TaskForm(course_id=course_id, unit_id=unit_id)
        return render(request, 'courses/teacher/create_task.html', {'form': form})
    else:
        try:
            form = TaskForm(request.POST, course_id=course_id, unit_id=unit_id)
            unit = Unit.objects.get(pk=unit_id)

            if form.is_valid():
                if Task.objects.filter(name=form.cleaned_data['name'], unit=unit).exists():
                    error = 'A task already exists in the unit with that name'
                    context = {
                    'form': form,
                    'course_id': course_id,
                    'error': error
                    }
                    return render(request, 'courses/teacher/create_task.html', context)
                else:
                    task=form.save(commit=False)
                    task.author=request.user
                    task.unit=unit
                    task.save()
                    return redirect(reverse('course_details', args=[course_id]))

        except Unit.DoesNotExist:
                    return render(request, "courses/error.html", {'error': "Unit doesn't exist", })

        return render(request, "courses/error.html", {'error': "Method not allowed", })

def edit_task(request, task_id):
    if request.method == "GET":
        instance=get_object_or_404(Task, id=task_id)
        form=TaskEditForm(instance=instance)
        return render(request, 'courses/teacher/edit_task.html', {'form': form})
    else:
        instance=get_object_or_404(Task, id=task_id)
        form = TaskEditForm(request.POST, instance=instance)
        if form.is_valid():
            task_exists = Task.objects.filter(name=form.cleaned_data['name'], unit=instance.unit)
            if task_exists and task_exists[0].id != task_id:
                error = 'A task already exists in the unit with that name'
                context = {
                'form': form,
                'error': error
                }
                return render(request, 'courses/teacher/edit_task.html', context)
            else:
                form.save()
                return redirect(reverse('view_task', args=[task_id]))
    

        return render(request, "courses/error.html", {'error': "Method not allowed", })

def enroll_course(request, course_id):
    if request.method == "POST":
        user = request.user
        try:
            course = Course.objects.get(pk=course_id)
            if course.author != user:
                course.students.add(user)
                return redirect('course_details', course_id=course_id)
            else:
                error = 'You are the author of this course. You cannot enroll in it.'
                context = {
                'course': course,
                'error': error
                }
                return render(request, 'courses/course.html', context)

        except Course.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Course doesn't exist", })
    return render(request, "courses/error.html", {'error': "Method not allowed", })

def list_students(request, course_id):
    if request.method == "GET":
        try:
            course = Course.objects.get(pk=course_id)
            students = course.students
            context = {
                'students': students
            }
            return render(request, 'courses/teacher/list_students.html', context)
        except Course.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Course doesn't exist", })



# Collect the categories to display them in the navbar
def search_categories():
    categories=Category.objects.all()
    return categories


