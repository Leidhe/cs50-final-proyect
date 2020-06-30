from django.contrib import admin
from .models import Category, Course, Unit, Section, Homework, Attachment, Task
js = ('ckeditor.js', 'configuration-ckeditor.js')

# Register your models here.
class UnitInline(admin.TabularInline):
    model = Unit
    
class TaskInline(admin.TabularInline):
    model = Task

class SectionInline(admin.TabularInline):
    model = Section

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'duration', 'level', 'language']
    inlines = [UnitInline,]

class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'course']
    inlines = [TaskInline, SectionInline]

class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'unit']

class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'unit']

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['student', 'task', 'grade']

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['student', 'task', 'grade']

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['file.file.name', 'homework.student']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Attachment)




