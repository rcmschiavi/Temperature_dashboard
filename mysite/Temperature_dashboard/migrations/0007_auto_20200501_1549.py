# Generated by Django 3.0.5 on 2020-05-01 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Temperature_dashboard', '0006_auto_20200501_1529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temperature',
            old_name='register_date',
            new_name='REGISTERED_AT',
        ),
        migrations.RenameField(
            model_name='temperature',
            old_name='temperature',
            new_name='TEMPERATURE',
        ),
        migrations.AlterModelTable(
            name='temperature',
            table='TEMPERATURE',
        ),
    ]
