# Generated by Django 5.1.7 on 2025-05-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_properties', '0008_unit_unit_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit_type',
            field=models.CharField(choices=[('studio', 'Studio'), ('1bed', '1 Bedroom')], max_length=50),
        ),
    ]
