# Generated by Django 3.1.7 on 2022-10-12 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20221012_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=255, verbose_name='Тема листа'),
        ),
    ]
