# Generated by Django 3.2.6 on 2022-08-09 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_applicationcomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationcomments',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.applicationcomments'),
        ),
    ]