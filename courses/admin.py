from django.contrib import admin
from .models import Category, Course, Unit, Section, Homework, Attachment, Task
from users.models import UserProfile
js = ('ckeditor.js', 'configuration-ckeditor.js')

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(Section)
admin.site.register(Homework)
admin.site.register(Attachment)




