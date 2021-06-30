from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _
from project import settings
from datetime import datetime

def createLanguages():
    from apps.core.models import Languages

    for lang in settings.LANGUAGES:
        try:
            language = Languages.objects.get(code=lang[0])
        except:
            language =Languages(code=lang[0], name=lang[1])
            language.save()


class CoreConfig(AppConfig):
    name = 'apps.core'
    verbose_name = _("Базовая информация")

    def ready(self):
        from apps.core.translation import createLanguageModels

        try: 
            createLanguages()
            createLanguageModels()
        except: pass



       