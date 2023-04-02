from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import get_language as lang
from apps.core.models import NameSlug, Translation, Images, Seo
from ckeditor.fields import RichTextField
import math



# BRAND
class Brand(NameSlug, Translation, Seo, Images):
    description = RichTextField(verbose_name='Описание', blank=True, null=True)
    discount = models.PositiveIntegerField(default=0)
    discount_whoosale = models.PositiveIntegerField(default=0)
    enable =   models.BooleanField(default=False)
    disable =  models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:brands', kwargs={'brand' : self.slug.lower()})
  
    def save(self, *args, **kwargs):
        # Enable disount to discount price
        if self.enable:
            for product in self.product.all():
                for variant in product.variant.all():
                    if self.discount:
                        variant.discount_price = int(math.ceil(variant.price * (1 - self.discount / 100)))
                    if variant.whoosale_price != 0:
                        if self.discount_whoosale:
                            variant.discount_whoosale_price = int(math.ceil(variant.whoosale_price * (1 - self.discount_whoosale / 100)))
                        else:
                            variant.discount_whoosale_price = 0
                    else:
                        variant.whoosale_price = variant.price
                        variant.discount_whoosale_price = variant.discount_price
                    variant.save()

            self.enable = False

        # Set all disount prices to zero
        if self.disable:
            for product in self.product.all():
                for variant in product.variant.all():
                    variant.discount_price = 0
                    variant.discount_whoosale_price = 0
                    variant.save()
            self.disable = False
        super(Brand, self).save(*args, **kwargs)




class BrandCategoryText(Translation):
    brand =       models.ForeignKey(Brand, on_delete=models.PROTECT)
    category =    models.ForeignKey('shop.Categories', on_delete=models.PROTECT)
    description = RichTextField(verbose_name='Описание', blank=True, null=True)
    
    class Meta:
        unique_together = (('brand','category'))





class BrandSeries(NameSlug):
    parent = models.ForeignKey(Brand,  on_delete=models.CASCADE, related_name="series")

    def __str__(self):
        
        try:
            return self.name + ' (' + str(len(self.product.all())) + ' шт.)' 
        except:
            return self.slug

    # def save(self):
    #     self.slug = '_'.join([self.parent.slug, self.slug])
    #     super(BrandSeries, self).save()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Бренд: Cерия'
        verbose_name_plural = 'Бренды: Cерии'


class BrandBanner(models.Model):
    parent =    models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="banners")
    image_pc =  models.ImageField(blank=False,    verbose_name="Баннер для ПК")
    image_mob = models.ImageField(blank=False,    verbose_name="Баннер для мобильных")
    date =      models.DateTimeField(default=now, verbose_name="Дата загрузки")

    class Meta:
        ordering = ('date',)
        verbose_name = 'Бренд: баннер'
        verbose_name_plural = 'Бренды: баннеры'
