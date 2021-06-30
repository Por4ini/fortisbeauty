from django.db import models
from ckeditor.fields import RichTextField



class WhoosaleText(models.Model):
    text = RichTextField(verbose_name="Текст")

    class Meta:
        verbose_name = 'Текст для оптовго покупателя'
        verbose_name_plural = 'Текст для оптовго покупателя'



class Quiz(models.Model):
    user =         models.ForeignKey('user.CustomUser', blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    business =     models.CharField(blank=True, max_length=255, verbose_name="Тип бизнеса")
    business_custom = models.CharField(blank=True, max_length=255, verbose_name="Тип бизнеса (свой вариант)")
    brand_work =   models.CharField(blank=True, max_length=255, verbose_name="Бренды с которыми работаю")
    brand_i_want = models.CharField(blank=True, max_length=255, verbose_name="Бренды с которыми хочу работать")
    budjet_clien = models.CharField(blank=True, max_length=255, verbose_name="Бюджет клиента")
    budjet_month = models.CharField(blank=True, max_length=255, verbose_name="Бюджет на закупку")
    gift =         models.CharField(blank=True, max_length=255, verbose_name="Подарок")
    gift_custom =  models.CharField(blank=True, max_length=255, verbose_name="Подарок (свой вариант)")
    name =         models.CharField(blank=True, max_length=255, verbose_name="Имя")
    phone =        models.CharField(blank=True, max_length=255, verbose_name="Телефон")
    email =        models.EmailField(blank=True, verbose_name="Email")
    
    def __str__(self):
        return self.name + ' ' + self.phone
