# Generated by Django 4.2.7 on 2023-11-21 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_roomservice_dutyschedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='client_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='number',
            old_name='number_id',
            new_name='id',
        ),
    ]