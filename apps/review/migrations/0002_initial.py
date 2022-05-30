# Generated by Django 3.2.6 on 2022-05-30 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('review', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutereview',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='students.studentmodel'),
        ),
        migrations.AlterUniqueTogether(
            name='institutereview',
            unique_together={('student', 'institute')},
        ),
    ]
