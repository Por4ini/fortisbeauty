from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class OptConfig(AppConfig):
    name = 'apps.opt'
    verbose_name = _("Опт")
