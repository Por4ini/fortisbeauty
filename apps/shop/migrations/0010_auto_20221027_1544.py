# Generated by Django 3.1.7 on 2022-10-27 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20221027_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variant',
            options={'ordering': ['-stock'], 'verbose_name': 'Продукт: Вариант', 'verbose_name_plural': 'Продукт: Варианты'},
        ),
    ]
