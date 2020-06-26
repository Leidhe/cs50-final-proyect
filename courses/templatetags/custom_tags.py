from django import template
from courses.models import Category, Course, Unit, Section, Task, Homework
from users.models import UserProfile

register = template.Library()

@register.filter
def sections_in_unit(sections, unit_id):
    try:
        unit= Unit.objects.get(pk=unit_id)
        sections = Section.objects.filter(unit=unit)
        return sections
    except Unit.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Unit doesn't exist", })

@register.filter
def tasks_in_unit(tasks, unit_id):
    try:
        unit= Unit.objects.get(pk=unit_id)
        tasks = Task.objects.filter(unit=unit)
        return tasks
    except Unit.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Unit doesn't exist", })

@register.filter
def avatar(students, student_id):
    avatar = UserProfile.objects.filter(user__id=student_id)
    if avatar:
        avatar = avatar[0]
        return avatar.avatar.url
    else:
        return None
        
@register.filter
def grade_task(grade, task_id):
    homework = Homework.objects.filter(task__id=task_id)
    if homework:
        grade = homework[0].grade
    else:
        grade = 0
    return grade

   