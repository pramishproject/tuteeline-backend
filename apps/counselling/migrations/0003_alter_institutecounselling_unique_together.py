# Generated by Django 3.2.6 on 2022-05-31 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0002_initial'),
        ('students', '0002_initial'),
        ('counselling', '0002_auto_20220531_0245'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='institutecounselling',
            unique_together={('student', 'institute')},
        ),
    ]
