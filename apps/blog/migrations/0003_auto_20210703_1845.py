# Generated by Django 3.1.7 on 2021-07-03 15:45

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogposttranslation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='blogposttranslation',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Текст'),
        ),
    ]