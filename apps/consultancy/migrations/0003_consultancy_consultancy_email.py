# Generated by Django 3.2.6 on 2022-06-06 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy', '0002_consultancystaff_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultancy',
            name='consultancy_email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]
