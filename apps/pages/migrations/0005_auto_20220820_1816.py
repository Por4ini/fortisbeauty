# Generated by Django 3.1.7 on 2022-08-20 15:16

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20220728_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageabout',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, max_length=500, null=True, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='pagepayment',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, max_length=500, null=True, verbose_name='Текст'),
        ),
    ]
