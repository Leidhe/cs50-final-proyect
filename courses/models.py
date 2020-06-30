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
    LEVEL=(
        ('beginner', 'Beginner'),
        ('medium', 'Medium'),
        ('advanced', 'Advanced'),
    )
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="course_author")
    duration = models.PositiveIntegerField(help_text="Specify the time in hours")
    level = models.CharField(max_length=64, choices=LEVEL, default='beginner')
    language = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images/courses/%Y/%m/%d/')
    categories = models.ManyToManyField(
        Category, related_name="course_category")
    description = models.CharField(
        max_length=100, help_text="Write a description")
    content = RichTextUploadingField()
    end_date = models.DateField()
    students = models.ManyToManyField(User, related_name="courses_students")

    def __str__(self):
        return f"Course {self.id}: {self.name}"

class Unit(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="unit_author")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_unit")

    def __str__(self):
        return f"Unit {self.id}: {self.name}"


class Section(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="section_author")
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="unit_section")
    content = RichTextUploadingField()

    def __str__(self):
        return f"Section {self.id}: {self.name}"

class Task(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_author")
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="unit_task")
    content = RichTextUploadingField()
    students = models.ManyToManyField(User, through='Homework')
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Task {self.id}: {self.name}"


class Homework(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField(validators=[MaxValueValidator(10),], null=True)
    graded = models.BooleanField(default=False)
    answer = RichTextUploadingField()

    def __str__(self):
        return f"Homework {self.id}: Student:{self.student}"

class Attachment(models.Model):
    file = models.FileField(upload_to='uploads')
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.file.name}"

