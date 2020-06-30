import json
from datetime import datetime
from django.db.models import Q

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.views import View
from users.forms import UserEditForm
from users.models import UserProfile

from .forms import (CorrectionForm, CourseEditForm, CourseForm,
                    HomeworkEditForm, HomeworkForm, SectionEditForm,
                    SectionForm, TaskEditForm, TaskForm, UnitEditForm,
                    UnitForm)
from .models import Attachment, Category, Course, Homework, Section, Task, Unit


def index(request):
    if request.method == "GET":
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
    return render(request, "courses/index.html", context)


@login_required(login_url='/login')
def account(request):
    # View your profile
    if request.method == "POST":
        categories = search_categories()
        render(request, "courses/error.html",
               {'error': "Method not allowed", 'categories': categories})

    # Method GET
    profile_picture = None
    profile_picture = UserProfile.objects.filter(user=request.user)

    if profile_picture:
        profile_picture = profile_picture[0]
    categories = search_categories()

    context = {
        'user': request.user,
        'categories': categories,
        'profile_picture': profile_picture
    }
    return render(request, "courses/account.html", context)


@login_required(login_url='/login')
def edit_account(request):
    # Edit your profile
    categories = search_categories()
    if request.method == "GET":
        instance = get_object_or_404(User, id=request.user.id)
        form = UserEditForm(instance=instance)
        return render(request, 'courses/edit_account.html', {'form': form, 'categories': categories})

    # Method POST
    else:
        instance = get_object_or_404(User, id=request.user.id)
        form = UserEditForm(request.POST or None,
                            request.FILES or None, instance=instance)

        if form.is_valid():
            form.save()

            # Get the new profile_picture (if any)
            profile_picture = request.FILES.get('picture_profile')
            user_picture = UserProfile.objects.filter(user=request.user)

            # If the user already has a profile picture one has been added
            if user_picture and profile_picture:
                user_picture = user_picture[0]
                user_picture.avatar = profile_picture
                user_picture.save()

            # If the user does not have a profile photo and a
            elif profile_picture:
                user_picture = UserProfile(
                    user=request.user, avatar=profile_picture)
                user_picture.save()

            return redirect(reverse('myaccount'))

        return render(request, 'courses/edit_account.html', {'form': form, 'categories': categories})

@login_required(login_url='/login')
def change_password(request):
    #Change the password
    categories = search_categories()

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('myaccount'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'courses/change_password.html', {
        'form': form, 'categories': categories})

def search(request):
    # For searches in the search bar by name or creator
    categories = search_categories()

    if request.method == "POST":
        render(request, "courses/error.html",
               {'error': "Method not allowed", 'categories': categories})

    # Method GET
    text = request.POST.get("search")
    
    #Search by name or creator
    courses_by_name_or_creator = Course.objects.filter(Q(name__contains=text) | Q(author__username__contains=text))

    context = {
        'courses_by_name_or_creator': courses_by_name_or_creator,
        'text': text,
        'categories': categories
    }
    return render(request, "courses/search.html", context)


def search_by_category(request, category_id):
    # Search by category buttons
    categories = search_categories()

    if request.method == "POST":
        render(request, "courses/error.html",
               {'error': "Method not allowed", 'categories': categories})

    #Method GET
    try:
        #Get the requested category
        category = Category.objects.get(pk=category_id)
        #Get all courses in the category
        courses = Course.objects.filter(categories=category)
        text = f'category {category.name}'
        context = {
            'courses_by_name_or_creator': courses,
            'text': text,
            'categories': categories
        }
        return render(request, "courses/search.html", context)
    except Category.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Category doesn't exist", 'categories': categories})


@login_required(login_url='/login')
def course(request, course_id):
    # Description of the selected course
    categories = search_categories()

    if request.method == "POST":
        render(request, "courses/error.html",
               {'error': "Method not allowed", 'categories': categories})

    #Method GET
    try:
        #Get the request course
        course = Course.objects.get(pk=course_id)
        # If the student is already enrolled in the course, the enrollment button is different
        student_enrolled = Course.objects.filter(
            id=course_id, students__id=request.user.id)

        context = {
            'student_enrolled': student_enrolled,
            'course': course,
            'categories': categories
        }
        return render(request, "courses/course.html", context)

    except Course.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Course doesn't exist", })

@login_required(login_url='/login')
def teacher(request):
    # Access to the view of a teacher
    categories = search_categories()


    if request.method == "POST":
        render(request, "courses/error.html",
               {'error': "Method not allowed", 'categories': categories})

    #Method GET
    courses_created = Course.objects.filter(author=request.user)
    context = {
        'categories': categories,
        'courses_created': courses_created
    }
    return render(request, "courses/teacher/teacher.html", context)


@login_required(login_url='/login')
def create_course(request):
    # When a teacher want to create a course
    categories = search_categories()

    if request.method == "GET":
        form = CourseForm()
        return render(request, 'courses/teacher/create_course.html', {'form': form, 'categories': categories})

    else:
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect(reverse('course', args=[course.pk]))
        return render(request, 'courses/teacher/create_course.html', {'form': form, 'categories': categories})


@login_required(login_url='/login')
def edit_course(request, course_id):
    # When a teacher wants to edit a course
    categories = search_categories()
    instance = get_object_or_404(Course, id=course_id)

    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories, 'course': instance})


    elif request.method == "GET":
        form = CourseEditForm(instance=instance)
        return render(request, 'courses/teacher/edit_course.html', {'form': form, 'categories': categories, 'course': instance})

    else:
        form = CourseEditForm(request.POST or None,
                              request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
            context = {
                'course': instance
            }
            return redirect(reverse('course_details', args=[instance.id]))
        return render(request, 'courses/teacher/edit_course.html', {'form': form, 'categories': categories, 'course': instance})


@login_required(login_url='/login')
def course_details(request, course_id):
    # Show the units, tasks, etc. that the course has
    categories = search_categories()

    try:
        course = Course.objects.get(pk=course_id)
        units = Unit.objects.filter(course__id=course_id)

    except Course.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Course doesn't exist", 'categories': categories})

    context = {
        'course': course,
        'units': units,
        'categories': categories
    }
    return render(request, 'courses/teacher/course_settings.html', context)

@login_required(login_url='/login')
def create_unit(request, course_id):
    # Create a unit inside of a course.
    course = get_object_or_404(Course, id=course_id)
    bool = check_date_course(request, course_id)

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})

    #If the request user is not the author of the course
    if request.user != course.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})
    
    categories = search_categories()

    if request.method == "GET":
        form = UnitForm(course_id=course_id)
        context = {
            'form': form,
            'course_id': course_id,
            'categories': categories

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
                        'error': error,
                        'categories': categories
                    }
                    return render(request, 'courses/teacher/create_unit.html', context)
                else:
                    unit = form.save(commit=False)
                    unit.author = request.user
                    unit.course = course
                    unit.save()
                    return redirect(reverse('course_details', args=[course_id]))

            context = {
                'form': form,
                'course_id': course_id,
                'categories': categories
            }
            return render(request, 'courses/teacher/create_unit.html', context)

        except Course.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Course doesn't exist", })

@login_required(login_url='/login')
def edit_unit(request, course_id, unit_id):
    # Edit a unit.
    instance = get_object_or_404(Unit, id=unit_id)
    categories = search_categories()
    bool = check_date_course(request, course_id)

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})


    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})
    

    if request.method == "GET":
        form = UnitEditForm(course_id=course_id, instance=instance)
        return render(request, 'courses/teacher/edit_unit.html', {'form': form, 'categories': categories, 'unit': instance})


    else:
        form = UnitEditForm(request.POST or None,
                            request.FILES or None, course_id=course_id, instance=instance)
        if form.is_valid():
            try:
                course = Course.objects.get(pk=course_id)

                #Check that the name of the unit exists
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
                
                form.save()
                return redirect(reverse('course_details', args=[course_id]))

            except Course.DoesNotExist:
                return render(request, "courses/error.html", {'error': "Course doesn't exist", 'categories':categories })

        return render(request, 'courses/teacher/edit_unit.html', {'form': form, 'categories': categories})

@login_required(login_url='/login')
def view_section(request, section_id):
    #See a section
    categories = search_categories()

    if request.method == "POST":
        render(request, "courses/error.html",
               {'error': "Method not allowed", 'categories': categories})

    #Method GET
    try:
        section = Section.objects.get(pk=section_id)
        course = section.unit.course
        context = {
            'section':  section,
            'course': course,
            'categories': categories
        }
        return render(request, "courses/section.html", context)

    except Section.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Section doesn't exist",'categories': categories})

@login_required(login_url='/login')
def view_task(request, task_id):
    #View a task
    categories = search_categories()
    now = timezone.now()

    if request.method == "GET":
        try:
            task = Task.objects.get(pk=task_id)
            course = task.unit.course
            homework = Homework.objects.filter(
                student=request.user, task=task_id)

            #If the task is still open or the request user is the author of the task
            if task.end_date > now or request.user == task.author:

                #If the task has already been delivered(student) it is redirected to review_task
                if homework:
                    homework_id = homework[0].id
                    return redirect('review_task', task_id=task_id, homework_id=homework_id)

                form = HomeworkForm(user_id=request.user.id, task_id=task_id)

                #List of students who have submitted homework (for teachers)
                list_students = Homework.objects.filter(task=task)
                list_files = []
                context = {
                    'form': form,
                    'task': task,
                    'students': list_students,
                    'course': course,
                    'categories': categories,
                    'list_files': list_files
                }
                return render(request, "courses/task.html", context)

            #If the task has been closed and the work has been submitted
            elif task.end_date < now and homework:
                unit = task.unit
                course = unit.course
                homework = homework[0]
                #The files attached to the work
                list_files = list(Attachment.objects.filter(
                    homework=homework).values())

                context = {
                    'course': course,
                    'list_files': list_files,
                    'homework': homework,
                    'task': task,
                    'categories': categories

                }
                return render(request, "courses/time_finish.html", context)

            #If the work has not been delivered on time
            else:
                unit = task.unit
                course = unit.course
                error = "You can't submit the task. Time's up."
                context = {
                    'course': course,
                    'task': task,
                    'error': error,
                    'categories': categories
                }
            return render(request, "courses/time_finish.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", 'categories': categories})

    else:
        try:
            task = Task.objects.get(pk=task_id)
            course_id = task.unit.course.id
            bool = check_date_course(request, course_id)

            if bool == False:
                return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})

            #If the task is still open
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
                    return redirect(reverse('course_details', args=[course_id]))
                
                list_students = Homework.objects.filter(task=task)
                course = task.unit.course

                context = {
                    'form': form,
                    'task': task,
                    'students': list_students,
                    'course': course,
                    'categories': categories
                }
                return render(request, "courses/task.html", context)


            else:
                #If the work has not been delivered on time

                unit = task.unit
                course = unit.course
                error = "You can't submit the task. Time's up."
                context = {
                    'course': course,
                    'task': task,
                    'error': error,
                    'categories': categories                    
                }
            return render(request, "courses/time_finish.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", 'categories': categories })


@login_required(login_url='/login')
def review_task(request, task_id, homework_id):
    #When the task has been sent once or more it is redirected here
    now = timezone.now()
    categories = search_categories()
    
    
    if request.method == "GET":
        try:
            task = Task.objects.get(pk=task_id)
            homework = Homework.objects.get(id=homework_id)
            unit = task.unit
            course = unit.course

            #If the task is open
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
                    'homework': homework,
                    'categories': categories,
                    'course': course
                }
                return render(request, "courses/task.html", context)

            else:
                #If the work has not been delivered on time

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
                    'error': error,
                    'categories': categories

                }
                return render(request, "courses/time_finish.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", 'categories': categories})

        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", 'categories': categories})

    else:
        try:
            homework = Homework.objects.get(id=homework_id)
            task = Task.objects.get(pk=task_id)
            instance = homework
            course_id = task.unit.course.id
            bool = check_date_course(request, course_id)

            if bool == False:
                return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})


            #If the task is open
            if task.end_date > now:

                form = HomeworkEditForm(
                    request.POST, request.FILES, user_id=request.user.id, task_id=task_id, instance=instance)

                list_files = list(Attachment.objects.filter(
                    homework=homework).values())

                if form.is_valid():
                    files = request.FILES.getlist('file_field')
                    homework = form.save(commit=False)
                    homework.student = request.user
                    homework.task = task
                    homework.save()
                    for f in files:
                        Attachment.objects.create(file=f, homework=homework)
                    return redirect(reverse('course_details', args=[course_id]))

                context = {
                    'form': form,
                    'task': task,
                    'list_files': list_files,
                    'homework': homework,
                    'categories': categories
                }
                return render(request, "courses/task.html", context)

            #If the work has not been delivered on time
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
                    'error': error,
                    'categories': categories
                }
                return render(request, "courses/time_finish.html", context)

        except Task.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Task doesn't exist", 'categories': categories})

        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", 'categories': categories})

@login_required(login_url='/login')
def correction(request, user_id, task_id, homework_id):
    #For the teacher to correct assignments
    instance = get_object_or_404(Task, id=task_id)
    categories = search_categories()
    now = timezone.now()


    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "GET":
        try:
            task = instance
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
                'homework': homework,
                'categories': categories
            }
            return render(request, "courses/teacher/correction.html", context)

        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", 'categories': categories})

    else:
        try:
            homework = Homework.objects.get(id=homework_id)
            task = instance
            unit = task.unit
            course = unit.course
            bool = check_date_course(request, course.id)

            if bool == False:
                return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})

            instance = homework
            form = CorrectionForm(
                request.POST, user_id=user_id, task_id=task_id, instance=instance)
            list_files = list(Attachment.objects.filter(
                homework=homework).values())
            list_files_json = json.dumps(list_files, cls=DjangoJSONEncoder)
            
            if task.end_date >= now:
                context = {
                    'form': form,
                    'task': task,
                    'error': 'The task is not yet concluded. You still cannot correct.',
                    'list_files': list_files,
                    'homework': homework,
                    'categories': categories
                }
                return render(request, "courses/teacher/correction.html", context)

            if form.is_valid():
                homework = form.save(commit=False)
                homework.graded = True
                #Send a email when the task has been graded.
                list_students = []
                list_students.append(homework.student.email)
                subject = "A new grade has been released"
                description = f'The task {task.name} of the course {course.name} has been graded. Your final score is {homework.grade}. Check the task for more details.'
                send_email(request, subject=subject, description=description, list_students_mails=list_students)
                homework.save()
                return redirect(reverse('course_details', args=[course.id]))
        
            context = {
                'form': form,
                'task': task,
                'list_files': list_files,
                'homework': homework,
                'categories': categories
            }
            return render(request, "courses/teacher/correction.html", context)

        except Homework.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Homework doesn't exist", 'categories': categories})

@login_required(login_url='/login')
def create_section(request, course_id, unit_id):
    
    #To create a section in a course unit
    categories = search_categories()
    instance = get_object_or_404(Unit, id=unit_id)
    bool = check_date_course(request, course_id)

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})


    #If the request user is not the author of the unit
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "GET":
        form = SectionForm(course_id=course_id, unit_id=unit_id)
        return render(request, 'courses/teacher/create_section.html', {'form': form, 'categories': categories})

    else:
        form = SectionForm(
            request.POST, course_id=course_id, unit_id=unit_id)
        unit = instance

        if form.is_valid():
            if Section.objects.filter(name=form.cleaned_data['name'], unit=unit).exists():
                error = 'A section already exists in the unit with that name'
                context = {
                    'form': form,
                    'course_id': course_id,
                    'error': error,
                    'categories': categories
                }
                return render(request, 'courses/teacher/create_section.html', context)
            else:
                section = form.save(commit=False)
                section.author = request.user
                section.unit = unit
                section.save()
                return redirect(reverse('course_details', args=[course_id]))

        return render(request, 'courses/teacher/create_section.html', {'form': form, 'categories': categories})

@login_required(login_url='/login')
def edit_section(request, section_id):
    #Edit a section
    instance = get_object_or_404(Section, id=section_id)
    categories = search_categories()
    bool = check_date_course(request, course_id)

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})

    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "GET":
        form = SectionEditForm(instance=instance)
        return render(request, 'courses/teacher/edit_section.html', {'form': form, 'categories': categories})

    else:
        form = SectionEditForm(request.POST, instance=instance)
        if form.is_valid():
            section_exists = Section.objects.filter(
                name=form.cleaned_data['name'], unit=instance.unit)
            if section_exists and section_exists[0].id != section_id:
                error = 'A section already exists in the unit with that name'
                context = {
                    'form': form,
                    'error': error,
                    'categories': categories
                }
                return render(request, 'courses/teacher/edit_section.html', context)
            else:
                form.save()
                return redirect(reverse('view_section', args=[section_id]))
        return render(request, 'courses/teacher/edit_section.html', {'form': form, 'categories': categories})

@login_required(login_url='/login')
def create_task(request, course_id, unit_id):
    #Create a task
    instance = get_object_or_404(Unit, id=unit_id)
    bool = check_date_course(request, course_id)
    categories = search_categories()

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})

    #If the request user is not the author of the unit
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})
    

    if request.method == "GET":
        form = TaskForm(course_id=course_id, unit_id=unit_id)
        return render(request, 'courses/teacher/create_task.html', {'form': form, 'categories': categories})
    else:
        
        form = TaskForm(request.POST, course_id=course_id, unit_id=unit_id)
        unit = Unit.objects.get(pk=unit_id)
        course = unit.course

        if form.is_valid():
            if Task.objects.filter(name=form.cleaned_data['name'], unit=unit).exists():
                error = 'A task already exists in the unit with that name'
                context = {
                    'form': form,
                    'course_id': course.id,
                    'error': error,
                    'categories': categories
                }
                return render(request, 'courses/teacher/create_task.html', context)
            end_date = request.POST.get('end_date')

            bool = check_date_course_task(request, course_id, end_date)
            if bool == False:
                error = 'The completion date of the course is earlier than the completion date of the task. Please enter a valid date.'
                context = {
                    'form': form,
                    'course_id': course.id,
                    'error': error,
                    'categories': categories
                }
                return render(request, 'courses/teacher/create_task.html', context)

            else:
                task = form.save(commit=False)
                list_students = all_students_mails(course_id=course.id)
                subject = "New Task has been opened"
                description = f'The task {task.name} of the course {course.name} has been opened. The task will be closed on the day {task.end_date}'
                #Send email to all students in the course advising that the task has been opened

                send_email(request, subject=subject, description=description, list_students_mails=list_students)
                task.author = request.user
                task.unit = unit
                task.save()

                return redirect(reverse('course_details', args=[course_id]))

        return render(request, 'courses/teacher/create_task.html', {'form': form, 'categories': categories})

@login_required(login_url='/login')
def edit_task(request, task_id):
    #Edit a task
    instance = get_object_or_404(Task, id=task_id)
    course_id=instance.unit.course.id
    categories = search_categories()
    bool = check_date_course(request, course_id)

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})

    #If the request user is not the author of the task
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "GET":
        form = TaskEditForm(instance=instance)
        return render(request, 'courses/teacher/edit_task.html', {'form': form, 'categories': categories})
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
                    'error': error,
                    'categories': categories
                }
                return render(request, 'courses/teacher/edit_task.html', context)

            end_date = request.POST.get('end_date')

            bool = check_date_course_task(request, course_id, end_date)
            if bool == False:
                error = 'The completion date of the course is earlier than the completion date of the task. Please enter a valid date.'
                context = {
                    'form': form,
                    'course_id': course_id,
                    'error': error,
                    'categories': categories
                }
                return render(request, 'courses/teacher/create_task.html', context)
            else:
                form.save()
                return redirect(reverse('view_task', args=[task_id]))

        return render(request, 'courses/teacher/edit_task.html', {'form': form, 'categories': categories})

@login_required(login_url='/login')
def enroll_course(request, course_id):
    #To enroll a course
    categories = search_categories()

    if request.method == "GET":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories })


    user = request.user
    try:
        course = Course.objects.get(pk=course_id)
        now = datetime.date(timezone.now())

        if course.end_date < now: 
            error = 'The course has ended. You cannot enroll in it.'
            context = {
                'course': course,
                'error': error,
                'categories': categories
            }
            return render(request, 'courses/course.html', context)

        if course.author != user:
            course.students.add(user)
            return redirect('course_details', course_id=course_id)

        else:
            error = 'You are the author of this course. You cannot enroll in it.'
            context = {
                'course': course,
                'error': error,
                'categories': categories
            }
            return render(request, 'courses/course.html', context)

    except Course.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Course doesn't exist", 'categories': categories})

@login_required(login_url='/login')
def list_students(request, course_id):
    #List all students of the course
    instance = get_object_or_404(Course, id=course_id)
    categories = search_categories()

    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "POST":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories })

    course = instance
    students = course.students
    context = {
        'course': course,
        'students': students,
        'categories': categories
    }
    return render(request, 'courses/teacher/list_students.html', context)

@login_required(login_url='/login')
def mycourses(request):
    #Show courses to which the user is enrolled
    categories = search_categories()

    if request.method == "POST":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories})

    # Method GET
    courses = Course.objects.filter(students__id=request.user.id)
    context = {
        'courses': courses,
        'categories': categories
    }
    return render(request, "courses/my_courses.html", context)

@login_required(login_url='/login')
def grades(request, course_id):
    categories = search_categories()
    instance = get_object_or_404(Course, id=course_id)

    #If the request user is not the author of the course
    if request.user == instance.author:
        return render(request, "courses/error.html", {'error': "You are the author", 'categories': categories})

    if request.method == "POST":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories})

    # Method GET
    units = Unit.objects.filter(course__id=course_id)
    context = {
        'units': units,
        'categories': categories
    }

    return render(request, "courses/grades.html", context)

@login_required(login_url='/login')
def delete_file(request):
    categories = search_categories()
    if request.method == "GET":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories})
    if request.is_ajax():
        try:
            file_id = request.POST.get('file_id')
            file = Attachment.objects.get(pk=file_id)
            file.delete()
            return JsonResponse({'message': 'OK'})

        except Attachment.DoesNotExist:
            return render(request, "courses/error.html", {'error': "File doesn't exist", 'categories': categories})
    else:
        return JsonResponse({'message': 'Failed'})

@login_required(login_url='/login')
def delete_course(request, course_id):
    categories = search_categories()
    instance = get_object_or_404(Course, id=course_id)

    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "GET":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories})
    
    instance.delete()
    return redirect("teacher")

@login_required(login_url='/login')
def delete_unit(request, unit_id):
    categories = search_categories()
    instance = get_object_or_404(Unit, id=unit_id)
    course_id = instance.course.id
    bool = check_date_course(request, course_id)

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})


    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "GET":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories})
    
    instance.delete()
    return redirect(reverse("course_details", args=[course_id]))

@login_required(login_url='/login')
def delete_section(request, section_id):
    categories = search_categories()
    instance = get_object_or_404(Section, id=section_id)
    unit = instance.unit
    course = unit.course
    bool = check_date_course(request, course_id)

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})
    

    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "GET":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories})
    
    instance.delete()
    return redirect(reverse("course_details", args=[course.id]))

@login_required(login_url='/login')
def delete_task(request, task_id):
    categories = search_categories()
    instance = get_object_or_404(Task, id=task_id)
    unit = instance.unit
    course = unit.course
    bool = check_date_course(request, course_id)

    if bool == False:
        return render(request, "courses/error.html", {'error': "You cannot change the course once it has been concluded.", 'categories': categories})

    #If the request user is not the author of the course
    if request.user != instance.author:
        return render(request, "courses/error.html", {'error': "You are not the author", 'categories': categories})

    if request.method == "GET":
        return render(request, "courses/error.html", {'error': "Method not allowed", 'categories': categories})
    
    instance.delete()
    return redirect(reverse("course_details", args=[course.id]))


def search_categories():
    # Collect the categories to display them in the navbar
    categories = Category.objects.all()
    return categories


def send_email(request, subject, description, list_students_mails):
    try:
        email = EmailMessage(
            subject,
            description,
            settings.EMAIL_HOST_USER,
            list_students_mails
        )
        email.send()

    except BadHeaderError:
        context = {
            'error': "An error has ocurred",
        }
        return render(request, "courses/error.html", context)

def all_students_mails(course_id):
    instance = get_object_or_404(Course, id=course_id)
    course = instance
    students = course.students
    list_mails = []
    for student in students.all():
        list_mails.append(student.email)
    return list_mails

def check_date_course(request, course_id):
    try:
        course_date = Course.objects.get(pk=course_id).end_date
        now = datetime.date(timezone.now())

        if course_date < now:
            return False
        else:
            pass
    except Course.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Course doesn't exist", 'categories': categories})
 
def check_date_course_task(request, course_id, task_date):
    try:
        task_date_obj = datetime.date(datetime.strptime(task_date, '%Y-%m-%d %H:%M:%S'))
        course_date = Course.objects.get(pk=course_id).end_date

        if course_date < task_date_obj:
            return False
        else:
            pass
    except Course.DoesNotExist:
            return render(request, "courses/error.html", {'error': "Course doesn't exist", 'categories': categories})
 