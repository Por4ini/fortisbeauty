# Generated by Django 3.1.7 on 2023-01-11 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerOpt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate_childs', models.BooleanField(default=False, verbose_name='Перевод')),
                ('title', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры Opt',
            },
        ),
        migrations.CreateModel(
            name='BannerOptPC',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.PositiveIntegerField(default=0, verbose_name='№')),
                ('image_thmb', models.JSONField(blank=True, default=dict, null=True)),
                ('image', models.FileField(max_length=1024, upload_to='', verbose_name='Изображение PC')),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pc', to='banners.banneropt')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BannerOptMobile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.PositiveIntegerField(default=0, verbose_name='№')),
                ('image_thmb', models.JSONField(blank=True, default=dict, null=True)),
                ('image', models.FileField(max_length=1024, upload_to='', verbose_name='Изображение Мобильный')),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mobile', to='banners.banneropt')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]