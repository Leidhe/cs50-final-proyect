from django.contrib import admin
from .models import Category, Course, Unit, Section, Homework
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Section)
admin.site.register(Homework)



