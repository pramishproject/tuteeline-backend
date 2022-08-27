# Generated by Django 3.2.6 on 2022-08-27 12:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0011_alter_socialmedialink_name'),
        ('students', '0010_alter_studentaddress_student'),
        ('payment_method', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('payment_method', models.CharField(choices=[('KHALTI', 'KHALTI'), ('ESEWA', 'ESEWA'), ('CASH', 'CASH')], max_length=100)),
                ('data', models.TextField(blank=True, null=True)),
                ('amount', models.FloatField()),
                ('transaction_id', models.CharField(default='', max_length=200)),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='institute.institute')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='students.studentmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
