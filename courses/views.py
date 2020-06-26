from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Category, Course, Unit, Section, Task, Homework, Attachment
from users.models import UserProfile
from django.contrib.auth.models import User
from .forms import CourseForm, CourseEditForm, UnitForm, UnitEditForm, SectionForm, SectionEditForm, TaskForm, TaskEditForm, HomeworkForm, HomeworkEditForm, CorrectionForm
from users.forms import UserEditForm
from django.views import View
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.forms.models import model_to_dict
from datetime import datetime
from django.utils import timezone


def index(request):
    if request.method == "GET":
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
    return render(request, "courses/index.html", context)

def account(request):
    if request.method == "POST":
        render(request, "courses/error.html", {'error': "Method not allowed", })

    #Method GET
    try:
        profile_picture = None
        user = User.objects.get(id=request.user.id)
        profile_picture = UserProfile.objects.filter(user=request.user)
        if profile_picture:
            profile_picture = profile_picture[0]
        categories = search_categories()

        context = {
            'user': user,
            'categories': categories,
            'profile_picture': profile_picture
        }
        return render(request, "courses/account.html", context)

    except User.DoesNotExist:
            return render(request, "courses/error.html", {'error': "User doesn't exist", })

def edit_account(request):
    if request.method == "GET":
        instance = get_object_or_404(User, id=request.user.id)
        form = UserEditForm(instance=instance)
        return render(request, 'courses/edit_account.html', {'form': form})
    else:
        instance = get_object_or_404(User, id=request.user.id)
        form = UserEditForm(request.POST or None,
                              request.FILES or None, instance=instance)
        if form.is_valid():
            profile_picture = request.FILES.get('picture_profile')
            form.save()
            user_picture = UserProfile.objects.filter(user=request.user)
            if user_picture and profile_picture:
                user_picture = user_picture[0]
                user_picture.avatar = profile_picture
                user_picture.save()

            elif profile_picture:
                user_picture = UserProfile(user=request.user, avatar=profile_picture)
                user_picture.save()

            return redirect(reverse('myaccount'))
        return render(request, "courses/error.html", {'error': "Method not allowed", })


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
            #If the student is already enrolled in the course, the enrollment button is different
            student_enrolled = Course.objects.filter(id=course_id, students__id = request.user.id)
            context = {
                'student_enrolled': student_enrolled,
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
                    unit = form.save(commit=False)
                    unit.author = request.user
                    unit.course = course
                    unit.save()
                    return redirect(reverse('course_details', args=[course_id]))

        except Course.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Course doesn't exist", })

        return render(request, "courses/error.html", {'error': "Method not allowed", })

# Edit a unit.


def edit_unit(request, course_id, unit_id):
    if request.method == "GET":
        instance = get_object_or_404(Unit, id=unit_id)
        form = UnitEditForm(course_id=course_id, instance=instance)
        return render(request, 'courses/teacher/edit_unit.html', {'form': form})
    else:
        instance = get_object_or_404(Unit, id=unit_id)
        form = UnitEditForm(request.POST or None,
                            request.FILES or None, course_id=course_id, instance=instance)
        if form.is_valid():
            try:
                course = Course.objects.get(pk=course_id)
                unit_exists = Unit.objects.filter(
                    name=form.cleaned_data['name'], course=course)
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
            now = timezone.now()
            task = Task.objects.get(pk=task_id)
            homework = Homework.objects.filter(
                student=request.user, task=task_id)

            if task.end_date > now or request.user == task.author:

                if homework:
                    homework_id = homework[0].id
                    return redirect('review_task', task_id=task_id, homework_id=homework_id)

                form = HomeworkForm(user_id=request.user.id, task_id=task_id)
                list_students = Homework.objects.filter(task=task)
                context = {
                    'form': form,
                    'task': task,
                    'students': list_students,
                }
                return render(request, "courses/task.html", context)

            elif task.end_date < now and homework:
                unit = task.unit
                course = unit.course
                homework = homework[0]
                list_files = list(Attachment.objects.filter(
                    homework=homework).values())
                context = {
                    'course': course,
                    'list_files': list_files,
                    'homework': homework,
                    'task': task,
                }
                return render(request, "courses/time_finish.html", context)
            else:
                unit = task.unit
                course = unit.course
                error = "You can't submit the task. Time's up."
                context = {
                    'course': course,
                    'task': task,
                    'error': error
                }
            return render(request, "courses/time_finish.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", })

    else:
        try:
            now = timezone.now()
            task = Task.objects.get(pk=task_id)

            if task.end_date > now:

                form = HomeworkForm(request.POST, request.FILES,
                                    user_id=request.user.id, task_id=task_id)

                if form.is_valid():
                    files = request.FILES.getlist('file_field')
                    homework = form.save(commit=False)
                    homework.student = request.user
                    homework.task = task
                    homework.save()
                    for f in files:
                        Attachment.objects.create(file=f, homework=homework)
                    return redirect('index')

            else:
                unit = task.unit
                course = unit.course
                error = "You can't submit the task. Time's up."
                context = {
                    'course': course,
                    'task': task,
                    'error': error
                }
            return render(request, "courses/time_finish.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", })


def review_task(request, task_id, homework_id):
    if request.method == "GET":
        try:
            now = timezone.now()
            task = Task.objects.get(pk=task_id)
            homework = Homework.objects.get(id=homework_id)

            if task.end_date > now:

                instance = homework

                list_files = list(Attachment.objects.filter(
                    homework=homework).values())
                form = HomeworkEditForm(
                    user_id=request.user.id, task_id=task_id, instance=instance)
                context = {
                    'form': form,
                    'task': task,
                    'list_files': list_files,
                    'homework': homework
                }
                return render(request, "courses/task.html", context)
            else:
                unit = task.unit
                course = unit.course
                error = "You can't submit the task. Time's up."
                list_files = list(Attachment.objects.filter(
                    homework=homework).values())
                context = {
                    'course': course,
                    'list_files': list_files,
                    'homework': homework,
                    'task': task,
                    'error': error
                }
                return render(request, "courses/time_finish.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", })

        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", })

    else:
        try:
            now = timezone.now()
            homework = Homework.objects.get(id=homework_id)
            task = Task.objects.get(pk=task_id)
            instance = homework
            if task.end_date > now:
                form = HomeworkEditForm(
                    request.POST, request.FILES, user_id=request.user.id, task_id=task_id, instance=instance)
                if form.is_valid():
                    files = request.FILES.getlist('file_field')
                    homework = form.save(commit=False)
                    homework.student = request.user
                    homework.task = task
                    homework.save()
                    for f in files:
                        Attachment.objects.create(file=f, homework=homework)
                    return redirect('index')

            else:
                error = "You can't submit the task. Time's up."
                unit = task.unit
                course = unit.course
                list_files = list(Attachment.objects.filter(
                    homework=homework).values())
                context = {
                    'course': course,
                    'list_files': list_files,
                    'homework': homework,
                    'task': task,
                    'error': error

                }
                return render(request, "courses/time_finish.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", })

        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", })


def correction(request, user_id, task_id, homework_id):
    if request.method == "GET":
        try:
            task = Task.objects.get(pk=task_id)
            homework = Homework.objects.get(pk=homework_id)
            instance = homework
            list_files = list(Attachment.objects.filter(
                homework=homework).values())
            list_files_json = json.dumps(list_files, cls=DjangoJSONEncoder)
            form = CorrectionForm(
                user_id=user_id, task_id=task_id, instance=instance)
            context = {
                'form': form,
                'task': task,
                'list_files': list_files,
                'homework': homework
            }
            return render(request, "courses/correction.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", })

        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", })

    else:
        try:
            homework = Homework.objects.get(id=homework_id)
            task = Task.objects.get(pk=task_id)
            instance = homework
            form = CorrectionForm(
                request.POST, user_id=user_id, task_id=task_id, instance=instance)
            if form.is_valid():
                homework = form.save(commit=False)
                homework.graded = True
                homework.save()
                return redirect('index')

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", })

        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", })


def create_section(request, course_id, unit_id):
    if request.method == "GET":
        form = SectionForm(course_id=course_id, unit_id=unit_id)
        return render(request, 'courses/teacher/create_section.html', {'form': form})
    else:
        try:
            form = SectionForm(
                request.POST, course_id=course_id, unit_id=unit_id)
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
                    section = form.save(commit=False)
                    section.author = request.user
                    section.unit = unit
                    section.save()
                    return redirect(reverse('course_details', args=[course_id]))

        except Unit.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Unit doesn't exist", })

        return render(request, "courses/error.html", {'error': "Method not allowed", })


def edit_section(request, section_id):
    if request.method == "GET":
        instance = get_object_or_404(Section, id=section_id)
        form = SectionEditForm(instance=instance)
        return render(request, 'courses/teacher/edit_section.html', {'form': form})
    else:
        instance = get_object_or_404(Section, id=section_id)
        form = SectionEditForm(request.POST, instance=instance)
        if form.is_valid():
            section_exists = Section.objects.filter(
                name=form.cleaned_data['name'], unit=instance.unit)
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
                    task = form.save(commit=False)
                    task.author = request.user
                    task.unit = unit
                    task.save()
                    return redirect(reverse('course_details', args=[course_id]))

        except Unit.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Unit doesn't exist", })

        return render(request, "courses/error.html", {'error': "Method not allowed", })


def edit_task(request, task_id):
    if request.method == "GET":
        instance = get_object_or_404(Task, id=task_id)
        form = TaskEditForm(instance=instance)
        return render(request, 'courses/teacher/edit_task.html', {'form': form})
    else:
        instance = get_object_or_404(Task, id=task_id)
        form = TaskEditForm(request.POST, instance=instance)
        if form.is_valid():
            task_exists = Task.objects.filter(
                name=form.cleaned_data['name'], unit=instance.unit)
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


def mycourses(request):
    if request.method == "POST":
        return render(request, "courses/error.html", {'error': "Method not allowed", })

    #Method GET
    courses = Course.objects.filter(students__id = request.user.id)
    categories = search_categories()
    context = {
        'courses': courses,
        'categories': categories
    }
    return render(request, "courses/my_courses.html", context)

def grades(request, course_id):
    if request.method == "POST":
        return render(request, "courses/error.html", {'error': "Method not allowed", })

    #Method GET
    units = Unit.objects.filter(course__id=course_id)
    categories = search_categories()
    context = {
        'units': units,
        'categories': categories
    }

    return render(request, "courses/grades.html", context)
 


# Collect the categories to display them in the navbar


def search_categories():
    categories = Category.objects.all()
    return categories
