# Generated by Django 3.2.6 on 2022-06-13 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institute_course', '0013_remove_instituteapply_action_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applyaction',
            name='consultancy_user',
        ),
    ]
