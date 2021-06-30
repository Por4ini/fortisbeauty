from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from apps.core.models import NameSlug, Translation, Images
from ckeditor.fields import RichTextField
import re



class Phones(Images):
    name =       models.CharField(max_length=50, verbose_name=_("Оператор"))
    phone =      models.CharField(max_length=50, verbose_name=_("Телефон"))
    phone_nums = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = _('Номера телефонов')
        verbose_name_plural = _('Номера телефонов')

    def save(self):
        self.phone_nums = re.sub("[^0-9]", "", self.phone) 
        return super().save()

    

class MainData(models.Model):
    email =  models.EmailField(default='office.fortisbeauty@gmail.com')
    adress = models.CharField(max_length=255, default='', blank=True)
    
    
    class Meta:
        verbose_name = _('Основная информация')
        verbose_name_plural = _('Основная информация')




class Slogan(Translation):
    text =  RichTextField(blank=True, null=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = _('Слоган на гоавной странице')
        verbose_name_plural = _('Слоган на гоавной странице')



class OurAdvantages(Translation):
    num =   models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255)
    text =  models.TextField()
    
    class Meta:
        ordering = ['num']
        verbose_name = _('Наши преимущества')
        verbose_name_plural = _('Наши преимущества')



class Message(models.Model):
    subject =    models.CharField(blank=False,  max_length=255, verbose_name=_("Тема письма"))
    date =       models.DateTimeField(auto_now=True, verbose_name=_("Время отправки"))
    first_name = models.CharField(blank=False, max_length=255, verbose_name=_("Имя"))
    email =      models.CharField(blank=False, max_length=255, verbose_name=_("Email"))
    phone =      models.CharField(blank=True,  max_length=255, verbose_name=_("Телефон"))
    text =       models.TextField(blank=False,    verbose_name=_("Текст письма"))
    
    class Meta:
        verbose_name = _('Сообщения')
        verbose_name_plural = _('Сообщения')

    def __str__(self):
        fields = []
        for field in [self.subject, self.email, self.phone]:
            if field != None:
                fields.append(field)
        return ' - '.join(fields)
