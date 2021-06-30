from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _

class ShopConfig(AppConfig):
    name = 'apps.shop'
    verbose_name = _("Магазин")

    def ready(self):
        try:
            from apps.shop.models import GoogleTaxonomy

            taxonomy = GoogleTaxonomy.objects.last()
            if not taxonomy:
                taxonomy = GoogleTaxonomy()
                taxonomy.save()
        except: pass
