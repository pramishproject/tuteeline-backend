# Generated by Django 3.2.6 on 2022-07-29 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0007_alter_role_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Role',
        ),
    ]