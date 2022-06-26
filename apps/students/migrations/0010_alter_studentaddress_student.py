# Generated by Django 3.2.6 on 2022-06-26 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_alter_studentmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentaddress',
            name='student',
            field=models.ForeignKey(error_messages={'unique': 'address of the user already exist'}, on_delete=django.db.models.deletion.CASCADE, related_name='address_relation', to='students.studentmodel'),
        ),
    ]
