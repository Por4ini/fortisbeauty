from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class FiltersConfig(AppConfig):
    name = 'apps.filters'
    verbose_name = _("Фильтры")
