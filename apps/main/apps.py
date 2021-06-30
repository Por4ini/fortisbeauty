from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _



def TryMainData():
    from .models import MainData

    if not MainData.objects.first():
        
        data = MainData()
        data.save()


class MainConfig(AppConfig):
    name = 'apps.main'
    verbose_name = _("Основное")

    def ready(self):
        try:
           TryMainData
        except:
            pass
      
       



       
