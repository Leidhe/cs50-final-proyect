# Generated by Django 3.0.7 on 2020-06-25 21:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_homework_graded'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='end_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
