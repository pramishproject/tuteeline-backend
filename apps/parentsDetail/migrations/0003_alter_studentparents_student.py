# Generated by Django 3.2.6 on 2022-06-15 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_initial'),
        ('parentsDetail', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentparents',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='students.studentmodel'),
        ),
    ]
