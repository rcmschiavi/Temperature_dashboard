# Generated by Django 3.0.5 on 2020-05-01 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Temperature_dashboard', '0003_auto_20200501_1527'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='temperature',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='temperature',
            table='temperature',
        ),
    ]