from django.contrib import admin
from django import forms 
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms import TextInput, Textarea
from apps.shop.forms import *
from apps.shop.models import *
from .globals import *


# COUNTRY
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


# PRODUCT IMAGES
@admin.register(VariantImages)
class VariantImagesAdmin(admin.ModelAdmin):
    def delete_model(VariantImagesAdmin, request, queryset):
        for obj in queryset:
            obj.delete()


class VariantImagesInline(admin.TabularInline):
    def get_image(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="object-fit: cover; object-position: center;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'], width=120, height=120))
            return img
        else:
            return '-'


    model = VariantImages
    readonly_fields = ['get_image',]
    fields = ['num','get_image','image',]
    extra = 0
    
   


class ProductDescriptionImagesInline(admin.TabularInline):
    model = ProductDescriptionImages
    fields = ['num','image','image_thmb']
    extra = 1
 


# VARIANTS
@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    def product(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s_change' % (obj.parent._meta.app_label, obj.parent._meta.model_name), args=[force_text(obj.parent.pk)])
            url = '<a href="{url}">{text}</a>'.format(url=url,text=obj.parent.name)
            return mark_safe(url)
        return '-'

    def brand(self, obj):
        return obj.parent.brand

    def get_image(self, obj=None):
        if hasattr(obj, 'images'):
            image = obj.images.first()
            if image is not None:
                try:
                    image_path = image.image_thmb['xs']['path']
                except:
                    image_path = ''

                url = '<img width="120" heigh="120" src="{url}">'.format(url=image_path)
                return mark_safe(url)
        else:
            return '-'

    readonly_fields = ['product', ]
    search_fields = ['code']
    list_display = ['code','stock','get_image','brand','parent','value', 'price', 'whoosale_price',]
    list_filter = ['stock','parent__brand','parent__category']
    list_editable=['stock','price', 'whoosale_price']
    # exclude = ['parent']
    inlines = [
        VariantImagesInline,
        ProductDescriptionImagesInline
    ]

    fieldsets = (
        (_('Продукт'), {
            'fields': ('parent','product')
        }),
        (_('Основная информация'), {
            'fields': ('code','barcode','stock',)
        }),
        (_('Значение варианта'), {
            'fields': ('value',)
        }),
        (_('Цена розничная'), {
            'fields': (('price','discount_price'),)
        }),
        (_('Цена Оптовая'), {
            'fields': (('whoosale_price','discount_whoosale_price'),)
        }),
    )


class VariantInline(admin.TabularInline):
    def get_edit_link(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            url = '<a href="{url}">{text}</a>'.format(url=url,text='Редактировать',)
            return mark_safe(url)
        return _("Нажмите сохранить и продолжить, для получения ссылки редактирования")

    def get_image(self, obj=None):
        try: url = obj.images.first().image_thmb['s']['path']
        except: url = '/static/img/no_image.jpg'
        return mark_safe(
            f'''<img width=120 height=120 style="object-fit: contain;" src="{url}">'''
        )

    model = Variant
    readonly_fields = ['get_image','get_edit_link']
    fields =  ['get_image','get_edit_link','value','price','discount_price','whoosale_price','stock']
    exclude = ['type']
    inlines = [VariantImagesInline]
    extra = 0

    

    
    
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def image(self, obj=None):
        try:
            url = obj.variant.first().images.first().image_thmb['s']['path']
        except:
            url = '/static/img/no_image.jpg'
        return mark_safe(
            f'''<img width=120 height=120 style="object-fit: contain;" src="{url}">'''
        )
            
             
    
    def comments_count(self, obj=None):
        return obj.comments.count()

    readonly_fields = ['comments_count']
    list_filter = ['brand','category',]
    list_display = [
        'image','name','human','brand','category','comments_count'
    ]
   
    formfield_overrides = FORMFIELD_OVERRIDES
    inlines = [
        VariantInline,
        CommentInline,
    ]


    fieldsets = (
        (_('Сатегория'), {
            'fields': ('category',)
        }),
        (_('Бренд'), {
            'fields': ('brand','serie',)
        }),
        (_('Страна'), {
            'fields': ('country',)
        }),
        (_('Еденицы измерения'), {
            'fields': ('unit',)
        }),
        (_('Онсовная информация'), {
            'fields': ('name','human',)
        }),
        (_('Описание'), {
            'fields': ('prescription','application','composition','description')
        }),
        (_('SEO'), {
            'fields': ('seo_title','seo_description','seo_keywords',)
        }),

    )


