# Generated by Django 3.1.7 on 2022-10-07 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20221007_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ouradvantagespc',
            name='parent',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='main.ouradvantages'),
        ),
        migrations.DeleteModel(
            name='OurAdvantagesMobile',
        ),
    ]
