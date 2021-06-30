from django.db import models
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer
from apps.shop.models import Variant
import json


class RequestData1CSettings(models.Model):
    ip = models.CharField(verbose_name="IP адрес", unique=True, max_length=255)

    class Meta:
        verbose_name = 'Допустимый IP'
        verbose_name_plural = 'Допустимые IP'



class RequestData1C(models.Model):
    date =  models.DateTimeField(default=now, verbose_name="Дата загрузки")
    data =  models.JSONField(default=list)

    class Meta:
        verbose_name = 'Сохраненный запрос 1С сервера'
        verbose_name_plural = 'Сохраненные запросы 1С сервера'


    def detail_json_formatted(self):
        data = json.dumps(self.data, indent=2)
        formatter = HtmlFormatter(style='colorful')
        response = highlight(data, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br/>"
        return mark_safe(style + response)

    detail_json_formatted.short_description = 'Details Formatted'


    def run_workers(self):
        if type(self.data) == list:
            for product in self.data:
                code = product.get('code')
                if code:
                    Variant.objects.filter(code=code).update(
                        price =          product.get('price'),
                        whoosale_price = product.get('whoosale_price'),
                        quantity =       product.get('qunatity'),
                        update =         now()
                    )
            return True
        return False


    def save(self):
        # self.run_workers()
        super(RequestData1C, self).save()

