# Generated by Django 3.2.6 on 2022-06-09 13:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0002_initial'),
        ('institute_course', '0006_auto_20220609_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckedStudentEssay',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checked_student_essay', to='institute_course.instituteapply')),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.personalessay')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckedStudentSop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checked_student_sop', to='institute_course.instituteapply')),
                ('sop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.studentsop')),
            ],
            options={
                'unique_together': {('application', 'sop')},
            },
        ),
    ]
