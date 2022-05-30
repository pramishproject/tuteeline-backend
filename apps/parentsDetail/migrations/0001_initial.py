# Generated by Django 3.2.6 on 2022-05-30 12:29

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HouseHold',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('maritial_status', models.CharField(choices=[('never_married', 'never_married'), ('seperated', 'seperated'), ('divorced', 'divorced'), ('widowed', 'widowed'), ('domestic_parents', 'domestic_parents')], max_length=100)),
                ('children', models.BooleanField(default=False)),
                ('no_of_childrents', models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinLengthValidator(0)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Siblings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('full_name', models.CharField(max_length=100)),
                ('age', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinLengthValidator(1)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentParents',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('relation', models.CharField(choices=[('father', 'father'), ('mother', 'mother'), ('limited_information', 'limited_information')], max_length=20)),
                ('fullname', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('country_code', models.CharField(blank=True, max_length=20, null=True)),
                ('contact', models.CharField(blank=True, max_length=20)),
                ('nationality', models.CharField(max_length=200)),
                ('occupation', models.CharField(max_length=200)),
                ('education', models.CharField(max_length=200)),
                ('annual_income', models.FloatField(blank=True, default=0.0)),
                ('currency', models.CharField(default='USD', max_length=50)),
            ],
        ),
    ]
