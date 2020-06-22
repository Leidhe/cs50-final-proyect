from django import template
from courses.models import Category, Course, Unit, Section

register = template.Library()

@register.filter
def in_unit(sections, unit_id):
    try:
        unit= Unit.objects.get(pk=unit_id)
        sections = Section.objects.filter(unit=unit)
        return sections
    except Unit.DoesNotExist:
        return render(request, "courses/error.html", {'error': "Unit doesn't exist", })
