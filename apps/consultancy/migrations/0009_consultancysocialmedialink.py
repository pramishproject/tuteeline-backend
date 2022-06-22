# Generated by Django 3.2.6 on 2022-06-18 03:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy', '0008_consultancy_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultancySocialMediaLink',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('name', models.CharField(choices=[('facebook', 'facebook'), ('youtube', 'youtube'), ('linkdin', 'linkdin'), ('instagram', 'instagram')], max_length=100)),
                ('link', models.URLField()),
                ('consultancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultancy_social_media', to='consultancy.consultancy')),
            ],
            options={
                'unique_together': {('consultancy', 'name')},
            },
        ),
    ]