# Generated by Django 3.2.6 on 2022-08-27 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_course', '0028_auto_20220815_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyaction',
            name='action',
            field=models.CharField(choices=[('verify', 'verify'), ('accept', 'accept'), ('reject', 'reject'), ('pending', 'pending'), ('applied', 'applied'), ('payment_requested', 'payment_requested'), ('payment_verify', 'payment_verify')], default='applied', max_length=20),
        ),
        migrations.AlterField(
            model_name='instituteapply',
            name='action',
            field=models.CharField(choices=[('verify', 'verify'), ('accept', 'accept'), ('reject', 'reject'), ('pending', 'pending'), ('applied', 'applied'), ('payment_requested', 'payment_requested'), ('payment_verify', 'payment_verify')], default='applied', max_length=20),
        ),
    ]
