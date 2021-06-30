
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator
from project import settings
from PIL import Image
# TRANSLATORS
from django.utils.translation import get_language as lang
from textblob import TextBlob
from unidecode import unidecode
import os

# ABSTRACT
# SEO
class Seo(models.Model):
    seo_title =       models.CharField(max_length=70,  blank=True, null=True, help_text="До 70 символов",  validators=[MaxLengthValidator(70)])
    seo_description = models.TextField(max_length=300, blank=True, null=True, help_text="До 300 символов", validators=[MaxLengthValidator(300)])
    seo_keywords =    models.TextField(max_length=255, blank=True, null=True, help_text="До 255 символов", validators=[MaxLengthValidator(255)])

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(Seo, self).save(*args, **kwargs)



class ProductsQuantity(models.Model):
    products_quantity = models.PositiveIntegerField(default=0, blank=True, editable=True)

    class Meta:
        abstract = True



class NameSlug(models.Model):
    name =  models.CharField(max_length=250, blank=False, verbose_name="Название")
    slug =  models.CharField(max_length=250, blank=True, null=True, verbose_name="Иденитификатор")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(NameSlug, self).save(*args, **kwargs)


class Language(models.Model):
    translate = models.BooleanField(default=True, verbose_name="Перевести")
    language =  models.ForeignKey('core.Languages', blank=False, on_delete=models.CASCADE, verbose_name="Язык")
    
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.language.code)

    def save(self):
        if self.translate == True:
            self.translate = False
        super(Language, self).save()
