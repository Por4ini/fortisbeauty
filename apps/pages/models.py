from django.db import models
from django.urls import reverse
from apps.core.models import NameSlug, Translation, Images
from ckeditor.fields import RichTextField
from django.utils.translation import gettext as _



class PageContacts(Translation):
    text =  RichTextField( null=True, blank=True, verbose_name=_("Текст"))
    phone = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Номер телефона'))
    email = models.EmailField(max_length=500, null=True, blank=True, verbose_name=_('Email'))
    
    class Meta:
        verbose_name = _("Страница: Котнакты")
        verbose_name_plural = _("Страница: Котнакты")

  




class PageAbout(Translation):
    title = models.CharField(max_length=255, default=_("О нас"), verbose_name=_("Заголовок"))
    text =  RichTextField(null=True, blank=True, verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Страница: О нас")
        verbose_name_plural = _("Страница: О нас")
    
    def __str__(self):
        return self.title


class PageReturnProd(Translation):
    title = models.CharField(max_length=255, default=_("Повернення"), verbose_name=_("Заголовок"))
    text = RichTextField(null=True, blank=True, verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Страница: Повернення")
        verbose_name_plural = _("Страница: Повернення ")

    def __str__(self):
        return self.title



class PagePayment(Translation):
    title = models.CharField(max_length=255, default=_("Оплата"), verbose_name=_("Заголовок"))
    text =  RichTextField(null=True, blank=True, verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Страница: Оплата")
        verbose_name_plural = _("Страница: Оплата")
    
    def __str__(self):
        return self.title


class PageDelivery(Translation):
    title = models.CharField(max_length=255, default=_("Доставка"), verbose_name=_("Заголовок"))
    text =  RichTextField(null=True, blank=True, verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Страница: Доставка")
        verbose_name_plural = _("Страница: Доставка ")
    
    def __str__(self):
        return self.title


class PageTermsOfUse(Translation):
    title = models.CharField(max_length=255, default=_("Условия использования"), verbose_name=_("Заголовок"))
    text =  RichTextField(null=True, blank=True, verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Страница: Условия использования")
        verbose_name_plural = _("Страница: Условия использования ")
    
    def __str__(self):
        return self.title


class PageGroup(Translation, NameSlug):
    class Meta:
        verbose_name = _("Статичная страница | Группа")
        verbose_name_plural = _("Статичные страницы | Группы")


class Page(Translation, Images, NameSlug):
    parent = models.ForeignKey(PageGroup, on_delete=models.CASCADE, verbose_name=_("Группа"), related_name="pages")
    text =   RichTextField(verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Статичная страница")
        verbose_name_plural = _("Статичные страницы")

    def get_absolute_url(self):
        return reverse('pages:page', kwargs={'slug':self.slug})