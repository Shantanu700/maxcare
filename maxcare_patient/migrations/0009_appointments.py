# Generated by Django 5.0 on 2024-10-11 06:26

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0008_alter_patient_med_issue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptoms', models.TextField(max_length=510)),
                ('symptoms_date', models.DateField()),
                ('request_date', models.DateField(default=datetime.date.today)),
                ('prefered_date', models.DateField()),
                ('appointment_date', models.DateField()),
                ('status', models.CharField(choices=[('PND', 'Pending'), ('RID', 'Request initiated'), ('CNF', 'Confirmed'), ('RJT', 'Rejected')], default='PND', max_length=3)),
                ('transaction_id', models.CharField(max_length=15, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='maxcare_patient.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='maxcare_patient.patient')),
            ],
        ),
    ]
