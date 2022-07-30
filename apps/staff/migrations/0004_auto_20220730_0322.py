# Generated by Django 3.2.6 on 2022-07-30 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0010_alter_institutestaff_role'),
        ('consultancy', '0010_consultancy_brochure'),
        ('staff', '0003_auto_20220730_0319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rolebase',
            old_name='name',
            new_name='role_name',
        ),
        migrations.AlterUniqueTogether(
            name='rolebase',
            unique_together={('institute', 'consultancy', 'portal', 'role_name')},
        ),
    ]