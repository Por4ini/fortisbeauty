# Generated by Django 3.1.7 on 2022-09-09 13:31

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20220909_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageabout',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Текст'),
        ),
    ]