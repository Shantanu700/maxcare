# Generated by Django 5.0 on 2024-10-14 23:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0026_alter_appointments_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Precription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=100)),
                ('valid_date', models.DateField()),
                ('frequency', models.IntegerField(validators=[django.core.validators.MaxValueValidator(3)])),
                ('appoint', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='maxcare_patient.appointments')),
            ],
        ),
    ]
