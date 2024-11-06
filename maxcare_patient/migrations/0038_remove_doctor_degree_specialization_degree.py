# Generated by Django 5.0 on 2024-11-05 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0037_specialization_alter_doctor_degree_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='degree',
        ),
        migrations.AddField(
            model_name='specialization',
            name='degree',
            field=models.CharField(default='MBBS', max_length=50),
        ),
    ]
