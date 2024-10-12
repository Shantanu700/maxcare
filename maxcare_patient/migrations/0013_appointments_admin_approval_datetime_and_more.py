# Generated by Django 5.0 on 2024-10-11 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0012_alter_appointments_request_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='admin_approval_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='appointments',
            name='admin_verf',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='appointments',
            name='doc_verf',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='appointments',
            name='doctor_approval_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
