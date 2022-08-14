# Generated by Django 3.2.6 on 2022-08-14 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0007_applicationcomments_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationcomments',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_application_comment', to='comment.applicationcomments'),
        ),
    ]
