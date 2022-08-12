# Generated by Django 3.2.6 on 2022-08-07 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0010_alter_institutestaff_role'),
        ('affiliation', '0002_affiliation_verify'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliation',
            name='university_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='institute.institute'),
        ),
    ]