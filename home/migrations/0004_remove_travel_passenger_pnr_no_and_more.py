# Generated by Django 4.1.4 on 2023-04-23 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_passenger_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_passenger',
            name='Pnr_no',
        ),
        migrations.RemoveField(
            model_name='travel_passenger',
            name='Total_price',
        ),
    ]
