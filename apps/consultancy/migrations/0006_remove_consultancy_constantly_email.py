# Generated by Django 3.2.6 on 2022-06-10 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy', '0005_consultancy_constantly_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultancy',
            name='constantly_email',
        ),
    ]