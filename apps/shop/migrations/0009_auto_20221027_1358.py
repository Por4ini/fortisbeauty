# Generated by Django 3.1.7 on 2022-10-27 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20221027_1356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variant',
            options={'ordering': ['-price'], 'verbose_name': 'Продукт: Вариант', 'verbose_name_plural': 'Продукт: Варианты'},
        ),
    ]
