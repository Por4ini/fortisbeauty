# Generated by Django 3.1.7 on 2021-07-03 12:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate_childs', models.BooleanField(default=False, verbose_name='Перевод')),
                ('title', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('link', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Ссылка')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='BannerPC',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.PositiveIntegerField(default=0, verbose_name='№')),
                ('image_thmb', models.JSONField(blank=True, default=dict, null=True)),
                ('image', models.FileField(max_length=1024, upload_to='', verbose_name='Изображение PC')),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pc', to='banners.banner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BannerMobile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.PositiveIntegerField(default=0, verbose_name='№')),
                ('image_thmb', models.JSONField(blank=True, default=dict, null=True)),
                ('image', models.FileField(max_length=1024, upload_to='', verbose_name='Изображение Мобильный')),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mobile', to='banners.banner')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
