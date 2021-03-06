# Generated by Django 3.0.7 on 2020-06-30 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20200628_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('medium', 'Medium'), ('advanced', 'Advanced')], default='beginner', max_length=64),
        ),
    ]
