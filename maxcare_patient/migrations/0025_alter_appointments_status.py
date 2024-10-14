# Generated by Django 5.0 on 2024-10-13 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0024_appointments_rejection_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='status',
            field=models.CharField(choices=[('Pending', 'PENDING'), ('Request Initiated', 'REQUEST INITIATED'), ('Paid', 'PAID'), ('Confirmed', 'CONFIRMED'), ('Rejected', 'REJECTED')], default='Pending', max_length=20),
        ),
    ]
