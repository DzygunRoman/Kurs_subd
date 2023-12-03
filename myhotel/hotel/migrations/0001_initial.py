# Generated by Django 4.2.7 on 2023-11-21 06:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, null=True, verbose_name='Клиенты')),
                ('famille', models.CharField(db_index=True, max_length=20, null=True, verbose_name='Фамилия')),
                ('firstName', models.CharField(max_length=20, null=True, verbose_name='Имя')),
                ('lastName', models.CharField(max_length=20, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(null=True, verbose_name='Дата рождения')),
                ('passport', models.IntegerField(default=0, verbose_name='Серия и номер паспорта')),
                ('city', models.CharField(max_length=20, null=True, verbose_name='Город проживания')),
                ('street', models.CharField(max_length=20, null=True, verbose_name='Улица')),
                ('home', models.IntegerField(default=0, verbose_name='номер дома')),
                ('apartment', models.IntegerField(default=0, verbose_name='Номер квартиры')),
                ('current_date', models.DateTimeField(null=True, verbose_name=django.utils.timezone.now)),
            ],
        ),
    ]