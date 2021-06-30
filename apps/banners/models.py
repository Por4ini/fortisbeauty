from django.db import models
from apps.core.models import Translation, Images
from django.utils.timezone import now



class Banner(Translation):
    title =       models.CharField(max_length=1024, blank=True, null=True,   verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True,                    verbose_name="Текст")
    link =        models.CharField(max_length=1024, blank=True, null=True,   verbose_name="Ссылка")
    date =        models.DateTimeField(default=now,                          verbose_name="Время создания")

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class BannerPC(Images):
    parent =      models.OneToOneField(Banner, on_delete=models.CASCADE, related_name='pc')
    image =       models.FileField(max_length=1024, null=False, blank=False, verbose_name="Изображение PC")


class BannerMobile(Images):
    parent =      models.OneToOneField(Banner, on_delete=models.CASCADE, related_name='mobile')
    image =       models.FileField(max_length=1024, null=False, blank=False, verbose_name="Изображение Мобильный")