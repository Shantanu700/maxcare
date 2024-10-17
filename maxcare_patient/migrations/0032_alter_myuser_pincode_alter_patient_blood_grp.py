# Generated by Django 5.0 on 2024-10-17 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0031_doctor_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='pincode',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='blood_grp',
            field=models.CharField(choices=[('a+', 'A+'), ('b+', 'B+'), ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-'), ('ab+', 'AB+'), ('o+', 'O+')], max_length=3, null=True),
        ),
    ]
