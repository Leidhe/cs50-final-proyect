# Generated by Django 3.0.7 on 2020-06-28 15:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20200626_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='end_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
