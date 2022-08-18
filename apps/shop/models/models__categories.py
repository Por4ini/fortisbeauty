from django.db import models
from django.urls import reverse
from django.core.cache import cache
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from mptt.models import MPTTModel
from apps.core.models import NameSlug, Images, Seo
from apps.shop.models.models__product import VariantImages
from ckeditor.fields import RichTextField
from datetime import datetime
import requests




class GoogleTaxonomy(models.Model):
    url =    models.CharField(max_length=1500, default="https://www.google.com/basepages/producttype/taxonomy-with-ids.ru-RU.txt")
    update = models.DateTimeField(null=True, blank=True)
    limit  = models.CharField(default="Красота и здоровье", blank=True, null=True, max_length=255, help_text="Для добавдения нескольких категорий, пишите их через запятую с пробелом.")

    class Meta:
        verbose_name = 'Таксономия Google - Загрузка'
        verbose_name_plural = 'Таксономия Google - Загрузка'

    def save(self):
        if not self.url:
            self.url = "https://www.google.com/basepages/producttype/taxonomy-with-ids.ru-RU.txt"
        self.update = datetime.now()
        super(GoogleTaxonomy, self).save()

        response = requests.get(self.url)
        response = response.content.decode('utf-8', 'ignore').split('\n')
        for item in response:
            item = item.split(' - ')
            if len(item) == 2:
                id, name = item[0], item[1]
                if self.limit and name.split(' > ')[0] not in self.limit.split(', '):
                    continue
                try:
                    category = GoogleTaxonomyCategories.objects.get(id=id)
                except:
                    category = GoogleTaxonomyCategories(parent=self, id=id)
                category.name = name
                category.save()
        



class GoogleTaxonomyCategories(models.Model):
    id =     models.PositiveIntegerField(primary_key=True)
    parent = models.ForeignKey(GoogleTaxonomy, on_delete=models.CASCADE, related_name="categories")
    name =   models.CharField(max_length=1500)

    class Meta:
        ordering = ['name']
        verbose_name = 'Таксономия Google - Категории'
        verbose_name_plural = 'Таксономия Google - Категории'

    def __str__(self):

        return f'{self.name} ({str(self.id)})'

    
class CategoryChildRel(models.Model):
    parent =   models.ForeignKey('shop.Categories', on_delete=models.CASCADE, related_name='children_category')
    relation = models.ForeignKey('shop.Categories', on_delete=models.CASCADE, related_name='children_rel')



class Categories(MPTTModel, NameSlug, Images, Seo):
    parent =      models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="родительская катгория", related_name="children", blank=True, null=True)
    human =       models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="Понятное названиме")
    taxonomy =    models.ForeignKey(GoogleTaxonomyCategories, on_delete=models.SET_NULL, null=True, help_text='Таксономия Google')
    description = RichTextField(verbose_name='Описание', blank=True, null=True)

  
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        names = []
        category = self
        while category != None:
            names.insert(0,category.name)
            category = category.parent
        return ' > '.join(names)

    @property
    def get_image(self):
        if self.image:
            return self.image_thmb['s']['path']
        image = VariantImages.objects.filter(parent__parent__category__children_rel__in=self.children_category.all()).first()
        if image:
            return  image.image_thmb['s']['path']
        return '/static/img/no_image.png'

    def get_tree(self):
        try:
            return '/'.join([category.slug for category in self.get_ancestors(include_self=True)])
        except:
            return '/'

    def get_tree_name(self):
        return ' > '.join([category.name for category in self.get_ancestors(include_self=True)])

    def get_absolute_url(self):
        return reverse('shop:catalogue', kwargs={
            'category': self.get_tree(), 
        })

    # @property
    # def udapte_descendants(self):
    #     for category in Categories.objects.all():
    #         category.children_category.all().delete()
    #         for c in category.get_descendants(include_self=True):
    #             obj = CategoryChildRel(parent=category, relation=c)
    #             obj.save()
    #     cache.delete('tree_categories')
    #     cache.delete(self.get_absolute_url())
    #     return True

    def save(self, *args, **kwargs):
        super(MPTTModel, self).save(*args, **kwargs)

    

        