# Generated by Django 5.0 on 2024-10-12 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0022_alter_appointments_status_alter_myuser_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]
