# Generated by Django 3.2.6 on 2022-06-27 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_course', '0017_alter_actionapplybyconsultancy_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutecourse',
            name='qualification',
            field=models.CharField(choices=[('school', 'school'), ('high_school', 'high_school'), ('undergraduate', 'undergraduate'), ('graduate', 'graduate'), ('post_graduate', 'post_graduate')], default='', max_length=100),
        ),
    ]