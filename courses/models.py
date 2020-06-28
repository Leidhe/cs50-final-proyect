from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import date
from django.core.validators import MaxValueValidator


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
    end_date = models.DateField(default=date.today)
    students = models.ManyToManyField(User, related_name="courses_students")

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
    content = RichTextUploadingField()

class Task(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_author")
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="unit_task")
    content = RichTextUploadingField()
    students = models.ManyToManyField(User, through='Homework')
    end_date = models.DateTimeField(default=date.today)

class Homework(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField(validators=[MaxValueValidator(10),], null=True)
    graded = models.BooleanField(default=False)
    answer = RichTextUploadingField()

class Attachment(models.Model):
    file = models.FileField(upload_to='uploads')
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name

