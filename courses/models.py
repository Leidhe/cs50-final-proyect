from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="course_author")
    duration = models.IntegerField()
    level = models.CharField(max_length=64)
    language = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images/courses/%Y/%m/%d/')
    categories = models.ManyToManyField(
        Category, related_name="course_category")
    description = models.CharField(
        max_length=100, help_text="Write a description")
    content = RichTextUploadingField()

class Unit(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="unit_author")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_unit")

class Section(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="section_author")
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="unit_section")
    content = RichTextUploadingField(
        
    )

class Task(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_author")
    #grade = models.IntegerField(default=0)
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="unit_task")
    content = RichTextUploadingField()

class File(models.Model):
    title = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="file_author")
    file = models.FileField(upload_to='upload/files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="files_section", blank=True)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="files_task", blank=True)


