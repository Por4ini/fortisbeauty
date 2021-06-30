from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


def create_staticpages():
    from .models import PageContacts, PageAbout, PagePaymentAndDelivery

    if PageContacts.objects.all().count() == 0:
        page_constacts = PageContacts()
        page_constacts.save()

    if PageAbout.objects.all().count() == 0:
        page_about = PageContacts()
        page_about.save()

    if PagePaymentAndDelivery.objects.all().count() == 0:
        page_payment = PagePaymentAndDelivery()
        page_payment.save()

   


class PagesConfig(AppConfig):
    name = 'apps.pages'
    verbose_name = _("Страницы")

    def ready(self):
        try: create_staticpages()
        except: pass
        

       
