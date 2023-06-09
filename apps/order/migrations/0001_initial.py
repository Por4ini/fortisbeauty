# Generated by Django 3.1.7 on 2021-07-03 12:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status_old', models.CharField(blank=True, choices=[('new', 'Новый заказ'), ('created', 'Создан, ожидает оплаты'), ('payed', 'Оплачен, в обработке'), ('prepered', 'Собран, ожидает передачи на доставку'), ('at_delivry', 'Передан на доставку'), ('delivring', 'Доставляется'), ('delivred', 'Доставлен'), ('declined', 'Отменен')], editable=False, max_length=255, null=True, verbose_name='Статус заказа')),
                ('status', models.CharField(choices=[('new', 'Новый заказ'), ('created', 'Создан, ожидает оплаты'), ('payed', 'Оплачен, в обработке'), ('prepered', 'Собран, ожидает передачи на доставку'), ('at_delivry', 'Передан на доставку'), ('delivring', 'Доставляется'), ('delivred', 'Доставлен'), ('declined', 'Отменен')], max_length=255, verbose_name='Статус заказа')),
                ('pay_type', models.CharField(choices=[('np', 'Наложеный платежь'), ('card', 'Оплата картой на сайте'), ('cash', 'Наличными при получении')], max_length=255, verbose_name='Способ оплаты')),
                ('delivery_type', models.CharField(choices=[('newpost', 'Новая почта'), ('curier', 'Адресная доставка')], max_length=255, verbose_name='Способ доставки')),
                ('delivery_cost', models.CharField(max_length=255, verbose_name='Стоисомть доставки')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=50, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=50, verbose_name='Отчество')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='Номер телефона')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Время заказа')),
                ('payed', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время оплаты')),
                ('whoosale', models.BooleanField(default=False, verbose_name='Оптовый заказ')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderDeliveryCurier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=50, verbose_name='Улица')),
                ('house', models.CharField(blank=True, max_length=50, verbose_name='Дом')),
                ('appartment', models.CharField(blank=True, max_length=50, verbose_name='Квартира')),
            ],
            options={
                'verbose_name': 'Доставка курьером',
                'verbose_name_plural': 'Доставка курьером',
            },
        ),
        migrations.CreateModel(
            name='OrderDeliveryNP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='Город')),
                ('branch', models.CharField(blank=True, max_length=50, verbose_name='Номер отделения')),
            ],
            options={
                'verbose_name': 'Доставка Новой почтой',
                'verbose_name_plural': 'Доставка Новой почтой',
            },
        ),
        migrations.CreateModel(
            name='PaymentResponses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Подтверждение оплты',
                'verbose_name_plural': 'Подтверждения оплт',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена')),
                ('price_ua', models.PositiveIntegerField(default=0, verbose_name='Цена, грн.')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='Всего')),
                ('total_ua', models.PositiveIntegerField(default=0, verbose_name='Всего, грн.')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='order.order', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товар в заказе',
            },
        ),
    ]
