from django import template
from courses.models import Category, Course, Unit, Section, Task

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