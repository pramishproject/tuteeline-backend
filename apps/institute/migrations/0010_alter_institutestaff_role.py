# Generated by Django 3.2.6 on 2022-07-30 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20220730_0319'),
        ('institute', '0009_alter_institutestaff_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutestaff',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staffposition'),
        ),
    ]
