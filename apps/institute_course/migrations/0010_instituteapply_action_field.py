# Generated by Django 3.2.6 on 2022-06-13 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute_course', '0009_applyaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteapply',
            name='action_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='institute_course.applyaction'),
        ),
    ]
