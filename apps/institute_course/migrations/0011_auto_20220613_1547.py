# Generated by Django 3.2.6 on 2022-06-13 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0002_initial'),
        ('consultancy', '0008_consultancy_rating'),
        ('institute_course', '0010_instituteapply_action_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyaction',
            name='consultancy_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='consultancy.consultancystaff'),
        ),
        migrations.AlterField(
            model_name='applyaction',
            name='institute_use',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='institute.institutestaff'),
        ),
    ]
