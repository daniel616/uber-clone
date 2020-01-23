# Generated by Django 3.0.2 on 2020-01-22 23:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=200)),
                ('arrival_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('start_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('confirmed', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type_registered', models.CharField(blank=True, max_length=200)),
                ('license_plate_number', models.CharField(blank=True, max_length=200)),
                ('max_capacity', models.IntegerField(blank=True, default=4)),
                ('special_requests_driver', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]