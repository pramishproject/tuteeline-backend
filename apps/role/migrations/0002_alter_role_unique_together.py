# Generated by Django 3.2.6 on 2022-07-26 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0005_institute_verification_status'),
        ('consultancy', '0010_consultancy_brochure'),
        ('role', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('institute', 'consultancy', 'portal', 'name')},
        ),
    ]
