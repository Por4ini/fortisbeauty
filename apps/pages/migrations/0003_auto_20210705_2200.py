# Generated by Django 3.1.7 on 2021-07-05 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20210705_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetermsofuse',
            name='title',
            field=models.CharField(default='Условия использования', max_length=255, verbose_name='Заголовок'),
        ),
    ]
