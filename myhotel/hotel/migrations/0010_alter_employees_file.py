# Generated by Django 4.2.7 on 2023-11-24 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0009_delete_dutyschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='file',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='uploads_model/%Y%m%d/', verbose_name='Фото'),
        ),
    ]
