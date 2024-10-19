# Generated by Django 5.0 on 2024-10-18 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxcare_patient', '0034_alter_patient_allergy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='marital_status',
            field=models.CharField(choices=[('UM', 'Unmarrid'), ('MA', 'Married'), ('DI', 'Divorced'), ('W', 'Widowed')], default='UM', max_length=2),
        ),
    ]
