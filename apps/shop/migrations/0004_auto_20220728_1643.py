# Generated by Django 3.1.7 on 2022-07-28 13:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_categories_descendants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='descendants',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1024), blank=True, default=list, size=None),
        ),
    ]
