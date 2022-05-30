# Generated by Django 3.2.6 on 2022-05-30 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('portal', '0001_initial'),
        ('institute', '0001_initial'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portalblog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.portalstaff'),
        ),
        migrations.AddField(
            model_name='instituteblog',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute.institute'),
        ),
        migrations.AddField(
            model_name='instituteblog',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.relation'),
        ),
    ]
