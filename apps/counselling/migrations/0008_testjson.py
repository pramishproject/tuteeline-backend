# Generated by Django 3.2.6 on 2022-06-30 13:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('counselling', '0007_consultancycounselling'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestJson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('jsonData', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
