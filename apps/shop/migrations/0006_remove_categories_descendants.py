# Generated by Django 3.1.7 on 2022-07-28 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20220728_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='descendants',
        ),
    ]
