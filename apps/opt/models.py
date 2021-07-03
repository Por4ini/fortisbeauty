from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from apps.core.models import NameSlug



class WhoosaleText(models.Model):
    text = RichTextUploadingField(verbose_name="Текст")

    class Meta:
        verbose_name = 'Текст для оптовго покупателя'
        verbose_name_plural = 'Текст для оптовго покупателя'



class BusinessTypes(NameSlug):
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Quiz: Вид бизнеса'
        verbose_name_plural = 'Quiz: Виды бизнеса'



class BusinessPositions(NameSlug):
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Quiz: Должность'
        verbose_name_plural = 'Quiz: Должности'



class BusinessDifficulties(NameSlug):
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Quiz: Трудности'
        verbose_name_plural = 'Quiz: Трудности'