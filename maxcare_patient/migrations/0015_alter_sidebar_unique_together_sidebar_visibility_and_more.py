# Generated by Django 5.0 on 2024-10-11 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0014_sidebar'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sidebar',
            unique_together={('url', 'priority')},
        ),
        migrations.AddField(
            model_name='sidebar',
            name='visibility',
            field=models.CharField(choices=[('PATIENT', 'patient'), ('DOCTOR', 'doctor'), ('ADMIN', 'admin')], default='ADMIN', max_length=8),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='icon',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='priority',
            field=models.IntegerField(),
        ),
        migrations.RemoveField(
            model_name='sidebar',
            name='admin_visibility',
        ),
        migrations.RemoveField(
            model_name='sidebar',
            name='doctor_visibility',
        ),
        migrations.RemoveField(
            model_name='sidebar',
            name='patient_visibility',
        ),
    ]
