# Generated by Django 4.2.7 on 2023-11-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0007_employees_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomservice',
            name='work_day',
            field=models.DateField(null=True, verbose_name='День рабочей смены'),
        ),
    ]
