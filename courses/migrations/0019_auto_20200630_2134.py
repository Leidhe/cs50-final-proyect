# Generated by Django 3.0.7 on 2020-06-30 19:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_auto_20200630_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='Format %Y-%m-%d %H:%M:%S'),
        ),
    ]
