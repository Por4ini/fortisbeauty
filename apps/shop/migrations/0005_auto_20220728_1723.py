# Generated by Django 3.1.7 on 2022-07-28 14:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20220728_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='descendants',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), blank=True, default=list, size=None),
        ),
    ]
