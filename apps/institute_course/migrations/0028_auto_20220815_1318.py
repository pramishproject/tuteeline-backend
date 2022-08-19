# Generated by Django 3.2.6 on 2022-08-15 13:18

import apps.institute_course.utils
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0010_alter_institutestaff_role'),
        ('institute_course', '0027_instituteapply_request_for_application_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteapply',
            name='approve_application_fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='staff_approve_application', to='institute.institutestaff'),
        ),
        migrations.AddField(
            model_name='institutecourse',
            name='course_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instituteapply',
            name='institute_staff_assign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff_assign_application', to='institute.institutestaff'),
        ),
        migrations.CreateModel(
            name='VoucherFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, upload_to=apps.institute_course.utils.upload_voucher_file, validators=[apps.institute_course.utils.ImageAndPdfValidator])),
                ('doc_type', models.CharField(blank=True, max_length=100, null=True)),
                ('apply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute_course.instituteapply')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]