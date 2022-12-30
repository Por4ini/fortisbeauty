from django.db import models
from django.utils import timezone 
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer
import uuid
import json




# Create your models here.
class Order(models.Model):
    ORDER_STATUS = [
        ('new',        'Новый заказ'),
        ('created',    'Создан, ожидает оплаты'),
        ('payed',      'Оплачен, в обработке'),
        ('prepered',   'Собран, ожидает передачи на доставку'),
        ('at_delivry', 'Передан на доставку'),
        ('delivring',  'Доставляется'),
        ('delivred',   'Доставлен'),
        ('declined',   'Отменен'),
    ]
    PAY_TYPE = [
        ('np',    'Наложеный платежь'),
        ('card',  'Оплата картой на сайте'),
        ('cash',  'Наличными при получении'),
        ('prepayment', 'Передоплата 200 грн'),
    ]
    DELIVWERTY_TYPE = [
        ('newpost', 'Новая почта'),
        ('curier',  'Адресная доставка'),
    ]


    id =          models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference =   models.PositiveIntegerField(null=True, blank=True)
    status_old =  models.CharField(max_length=255, editable=False, blank=True, null=True, choices=ORDER_STATUS, verbose_name=_("Статус заказа"))
    status =      models.CharField(max_length=255, choices=ORDER_STATUS, verbose_name=_("Статус заказа"))
    pay_type =    models.CharField(max_length=255, choices=PAY_TYPE, verbose_name=_("Способ оплаты"))
    delivery_type =  models.CharField(max_length=255, choices=DELIVWERTY_TYPE, verbose_name=_("Способ доставки"))
    delivery_cost =  models.CharField(max_length=255, verbose_name=_("Стоисомть доставки"), default=0)
    user =        models.ForeignKey('user.CustomUser', blank=True, on_delete=models.SET_NULL, null=True, verbose_name=_("Пользователь"), related_name="orders")
    name =        models.CharField(max_length=50, blank=True, verbose_name=_("Имя"))
    surname =     models.CharField(max_length=50, blank=True, verbose_name=_("Фамилия"))
    patronymic =  models.CharField(max_length=50, blank=True, verbose_name=_("Отчество"))
    phone =       models.CharField(max_length=40, blank=True, verbose_name=_("Номер телефона"))
    email =       models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    created =     models.DateTimeField(blank=True, null=True, verbose_name=_("Время заказа"), default=timezone.now)
    payed =       models.DateTimeField(blank=True, null=True, verbose_name=_("Время оплаты"), default=None)
    whoosale =    models.BooleanField(default=False, verbose_name=_("Оптовый заказ"))

    class Meta:
        ordering = ['-created']
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def get_total(self):
        total = 0
        for product in self.products.all():
            total += product.total
        return total

    def save(self):
        if self.delivery_type == 'newpost':
            self.delivery_cost = 'По тарифам перевозчика'
        elif self.delivery_type == 'curier':
            if self.get_total() < 2000:
                self.delivery_cost = '70 грн.'
            else:
                self.delivery_cost = 'бесплатно'
        
        super(Order, self).save()


class OrderProduct(models.Model):
    parent =    models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Продукт"), related_name='products')
    variant =   models.ForeignKey('shop.Variant', on_delete=models.CASCADE, verbose_name=_("Продукт"))
    quantity =  models.PositiveIntegerField(default=1, verbose_name=_("Количество"))
    price =     models.PositiveIntegerField(default=0, verbose_name=_("Цена"))
    price_ua =  models.PositiveIntegerField(default=0, verbose_name=_("Цена, грн."))
    total =     models.PositiveIntegerField(default=0, verbose_name=_("Всего"))
    total_ua =  models.PositiveIntegerField(default=0, verbose_name=_("Всего, грн."))

    class Meta:
        verbose_name = _("Товар в заказе")
        verbose_name_plural = _("Товар в заказе")

    def __str__(self):
        return f"{self.variant.parent.name}, артикул: {str(self.variant.code)}, {str(self.quantity)} шт., всего: {str(int(self.total))}, грн."
   


    def save(self):
        if self.parent.whoosale:
            if self.variant.discount_whoosale_price > 0 and self.variant.discount_whoosale_price < self.variant.whoosale_price:
                price =  self.variant.discount_whoosale_price
            else:
                price =  self.variant.whoosale_price
        else:
            if self.variant.discount_price > 0 and self.variant.discount_price < self.variant.price:
                price =  self.variant.discount_price
            else:
                price =  self.variant.price
          


        self.price =  price
        self.total =  price * self.quantity
        super(OrderProduct, self).save()
    

class OrderDeliveryNP(models.Model):
    parent = models.OneToOneField(Order, on_delete=models.CASCADE)
    city =   models.CharField(max_length=50, blank=True, verbose_name=_("Город"))
    branch = models.CharField(max_length=50, blank=True, verbose_name=_("Номер отделения"))

    class Meta:
        verbose_name = _("Доставка Новой почтой")
        verbose_name_plural = _("Доставка Новой почтой")


    def __str__(self):
        return f'{self.city} {self.branch}'
    

class OrderDeliveryCurier(models.Model):
    parent =     models.OneToOneField(Order, on_delete=models.CASCADE)
    city =       models.CharField(max_length=50, blank=True, verbose_name=_("Город"))
    street =     models.CharField(max_length=50, blank=True, verbose_name=_("Улица"))
    house =      models.CharField(max_length=50, blank=True, verbose_name=_("Дом"))
    appartment = models.CharField(max_length=50, blank=True, verbose_name=_("Квартира"))
    
    class Meta:
        verbose_name = _("Доставка курьером")
        verbose_name_plural = _("Доставка курьером")


    def __str__(self):
        return f'{self.city} {self.street} {self.house} {self.appartment}'


class PaymentResponses(models.Model):
    response = models.JSONField(default=dict)

    class Meta:
        verbose_name = _("Подтверждение оплты")
        verbose_name_plural = _("Подтверждения оплт")

    def detail_json_formatted(self):
        data = json.dumps(self.response, indent=2)
        formatter = HtmlFormatter(style='colorful')
        response = highlight(data, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br/>"
        return mark_safe(style + response)

    detail_json_formatted.short_description = 'Details Formatted'

    def save(self):
        for key in self.response.keys():
            if type(key) == str:
                self.response = json.loads(key)
            break

        if self.response.get('orderReference'):
            reference = int(self.response['orderReference'])
            Order.objects.filter(reference=reference).update(payed=True)
        super(PaymentResponses, self).save()