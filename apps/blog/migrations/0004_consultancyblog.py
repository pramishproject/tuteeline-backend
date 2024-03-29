# Generated by Django 3.2.6 on 2022-06-14 12:03

import apps.blog.utils
import apps.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy', '0008_consultancy_rating'),
        ('blog', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultancyBlog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('author_name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(default='portel/blog/default_logo.png', upload_to=apps.blog.utils.upload_blog_image_to, validators=[apps.core.validators.ImageValidator()])),
                ('verified', models.BooleanField(default=False)),
                ('consultancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultancy.consultancy')),
                ('relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.relation')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='consultancy.consultancystaff')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
