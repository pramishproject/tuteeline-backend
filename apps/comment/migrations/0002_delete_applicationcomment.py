# Generated by Django 3.2.6 on 2022-08-09 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApplicationComment',
        ),
    ]
