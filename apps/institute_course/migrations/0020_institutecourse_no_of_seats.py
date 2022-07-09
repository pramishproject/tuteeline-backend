# Generated by Django 3.2.6 on 2022-07-09 05:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_course', '0019_institutecourse_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutecourse',
            name='no_of_seats',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8000)]),
        ),
    ]
