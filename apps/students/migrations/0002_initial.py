# Generated by Django 3.2.6 on 2022-05-30 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institute', '0002_initial'),
        ('students', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.studentuser'),
        ),
        migrations.AddField(
            model_name='studentaddress',
            name='student',
            field=models.OneToOneField(error_messages={'unique': 'address of the user already exist'}, on_delete=django.db.models.deletion.CASCADE, related_name='address_relation', to='students.studentmodel'),
        ),
        migrations.AddField(
            model_name='instituteviewers',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute.institute'),
        ),
        migrations.AddField(
            model_name='instituteviewers',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.studentmodel'),
        ),
        migrations.AddField(
            model_name='favouriteinstitute',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='institute.institute'),
        ),
        migrations.AddField(
            model_name='favouriteinstitute',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='students.studentmodel'),
        ),
        migrations.AddField(
            model_name='completeprofiletracker',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='application_tracker', to='students.studentmodel'),
        ),
        migrations.AlterUniqueTogether(
            name='instituteviewers',
            unique_together={('student', 'institute')},
        ),
        migrations.AlterUniqueTogether(
            name='favouriteinstitute',
            unique_together={('student', 'institute')},
        ),
    ]
