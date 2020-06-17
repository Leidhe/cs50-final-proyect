from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_author")
    categories = models.ManyToManyField(Category, related_name="course_category")
    description = models.CharField(max_length=100, help_text="Write a description")


