# Generated by Django 3.2.6 on 2022-07-30 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0010_alter_institutestaff_role'),
        ('institute_course', '0022_alter_institutecourse_qualification'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteapply',
            name='institute_staff_assign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institute.institutestaff'),
        ),
    ]