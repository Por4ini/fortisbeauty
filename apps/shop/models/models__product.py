# MODELS
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.cache import cache
from apps.shop.tasks import cahce_all_products
from apps.core.models.models__translation import Translation
from apps.core.models import NameSlug, Images, Seo
from ckeditor.fields import RichTextField
import unidecode



class Country(Translation, NameSlug):
    class Meta:
        verbose_name = 'Продукт: Страна производитель'
        verbose_name_plural = 'Продукт: Страны производители'

    def __str__(self):
        return self.name



class Unit(NameSlug):
    unit = models.CharField(max_length=250, blank=True, null=True, verbose_name='Ед. измер.')

    def __str__(self):
        return f"{self.name}, {self.unit}" 

    

class Product(Translation, Seo):
    category =          models.ForeignKey('shop.Categories', on_delete=models.PROTECT,  verbose_name="Категория товара", related_name='product')
    brand =             models.ForeignKey('shop.Brand', on_delete=models.PROTECT,  verbose_name="Бренд", related_name='product')
    serie =             models.ForeignKey('shop.BrandSeries', on_delete=models.SET_NULL, verbose_name="Серия бренда", related_name='product', blank=True, null=True)
    country =           models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name="Стнрана", related_name='product', blank=True, null=True)
    unit =              models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="Ед. измер.")
    prescription =      models.TextField(blank=True, null=True, verbose_name="Назначение")
    application =       models.TextField(blank=True, null=True, verbose_name="Способ применения")
    composition =       models.TextField(blank=True, null=True, verbose_name="Состав")
    description =       RichTextField(blank=True, null=True, verbose_name="Описание")
    description_text =  models.TextField(blank=True, null=True, verbose_name="Описание (только текст)")
    name =              models.CharField(max_length=500, blank=False)
    slug =              models.CharField(max_length=500, blank=True,  verbose_name="Идентификатор (авто)")
    human =             models.CharField(max_length=500, blank=True, null=True, verbose_name="Понятное название (для чего продукт)")

    # DATE
    date =               models.DateTimeField(default=now, verbose_name="Дата загрузки")
    update =             models.DateTimeField(default=now, verbose_name="Дата обновления")

    unit =               models.CharField(max_length=500, verbose_name='Еденица измерения вариантов продукта', blank=True, null=True)
    views =           models.PositiveIntegerField(default=0, blank=True, verbose_name="Просмотров")
    
    class Meta:
        ordering = ('-name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукт'

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('shop:variant', kwargs={
            'category' : '/'.join([category.slug for category in self.category.get_ancestors(include_self=True)]),
            'brand':self.brand.slug, 
            'product_slug':self.slug, 
            'product_id':self.pk, 
           }
        )

    def cache_key(self):
        return f'product_{self.pk}__variant_{self.variant.first().pk}'

    def variant_price_down(self):
        return self.variant.all().order_by('-price')

    def get_variant(self):
        return self.variant.first()

    def get_image(self):
        return self.variant.first().images.first()

    def save(self):
        self.slug = slugify(str(unidecode.unidecode(self.name)))
        # cahce_all_products()
        super(Product, self).save()
      




class Variant(models.Model):
    parent =         models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name='variant')
    value =          models.CharField(max_length=250,       blank=True, null=True, verbose_name='Значение')
    price =          models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Цена")
    discount_price = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Цена (скидка)")
    whoosale_price = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Оптовая цена")
    discount_whoosale_price = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Оптовая цена (скидка)")
    code =           models.CharField(max_length=250,       blank=True, null=True, verbose_name="Артикул")
    barcode =        models.CharField(max_length=250,       blank=True, null=True, verbose_name='Штрихкод', default='')
    stock =          models.PositiveIntegerField(default=0, blank=True, verbose_name="Остаток")
    update =         models.DateTimeField(default=now, verbose_name="Дата обновления")
    views =           models.PositiveIntegerField(default=0, blank=True, verbose_name="Просмотров")
    

    class Meta:
        ordering = ['-price']
        verbose_name = 'Продукт: Вариант'
        verbose_name_plural = 'Продукт: Варианты'

   


    def save(self):
        cache.delete(self.get_absolute_url())
        if self.price == None:
            self.price = 0
        super(Variant, self).save()
    
    def get_absolute_url(self):
        if self.pk:
            return reverse('shop:variant', kwargs={
                'category' : '/'.join([category.slug for category in self.parent.category.get_ancestors(include_self=True)]),
                'brand':self.parent.brand.slug, 
                'product_slug':self.parent.slug, 
                'product_id':self.parent.pk, 
                'variant_id':self.pk}
            )
        return '/'

    def get_image(self):
        return self.images.first()

    def __str__(self):
        return f'{self.code}, {self.parent.brand.name} - {self.parent.name}'
    

class VariantImages(Images):
    parent =  models.ForeignKey(Variant, on_delete=models.CASCADE, verbose_name="Обьем", related_name='images')

    def save(self):
        super(VariantImages, self).save()


class ProductDescriptionImages(Images):
    parent =  models.ForeignKey(Variant, on_delete=models.CASCADE, verbose_name="Обьем", related_name='description_images')





@receiver(pre_delete, sender=VariantImages, dispatch_uid='delete_images_signal')
def delete_images(sender, instance, using, **kwargs):
    instance.delete_old()




   
