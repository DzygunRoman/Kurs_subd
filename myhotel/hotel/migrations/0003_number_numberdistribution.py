# Generated by Django 4.2.7 on 2023-11-21 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Number',
            fields=[
                ('number_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_index=True, default=0, unique=True, verbose_name='Номер')),
                ('numberOfPlaces', models.IntegerField(default=0, verbose_name='Количество мест в номере')),
                ('description', models.TextField(blank=True, verbose_name='Описание номера')),
                ('pricePerDay', models.IntegerField(default=0, verbose_name='Стоимость номера в сутки')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hotel.category', verbose_name='Категории')),
            ],
        ),
        migrations.CreateModel(
            name='NumberDistribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_arrival', models.DateField(null=True, verbose_name='Дата заезда')),
                ('time_departure', models.DateField(null=True, verbose_name='Дата выезда')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.client', verbose_name='Клиент')),
                ('number', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.number', verbose_name='Номер гостиницы')),
            ],
        ),
    ]
