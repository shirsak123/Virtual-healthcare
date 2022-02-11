# Generated by Django 3.2.4 on 2021-07-16 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_patient_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='education1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='education2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='fromYear1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='from_year2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='professtion_from_year1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='professtion_from_year2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='professtion_title1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='professtion_title2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='professtion_to_year1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='professtion_to_year2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='toYear1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='to_year2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='university1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='university2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]