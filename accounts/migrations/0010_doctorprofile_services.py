# Generated by Django 3.2.4 on 2021-07-17 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210716_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='services',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]