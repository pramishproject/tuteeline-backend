# Generated by Django 3.2.6 on 2022-06-14 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_course', '0016_rename_institute_use_applyaction_institute_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionapplybyconsultancy',
            name='action',
            field=models.CharField(choices=[('verify', 'verify'), ('not_verify', 'not_verify')], default='applied', max_length=20),
        ),
    ]