# Generated by Django 3.2.4 on 2021-07-18 11:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0002_auto_20210718_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pharmacy',
            name='rating',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
