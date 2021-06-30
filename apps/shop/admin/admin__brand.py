from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from apps.shop.models import Brand, BrandCategoryText, BrandSeries
from .globals import *



# BRAND
@admin.register(BrandCategoryText)
class BrandCategoryTextAdmin(admin.ModelAdmin):
    pass



class BrandCategoryTextInline(admin.TabularInline):
    def get_edit_link(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            url = '<a href="{url}">{text}</a>'.format(url=url,text='Редактировать',)
            return mark_safe(url)
        return _("Нажмите сохранить и продолжить, для получения ссылки редактирования")

    model = BrandCategoryText
    formfield_overrides = FORMFIELD_OVERRIDES
    extra = 0

    readonly_fields = ['get_edit_link']
    fields = ['category','get_edit_link']


    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(BrandCategoryTextInline, self).get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(BrandCategoryTextInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'category' and self.parent_obj:
            cats = BrandCategoryText.objects.filter(brand=self.parent_obj).values_list('category', flat=True)
            field.queryset = field.queryset.filter(product__brand=self.parent_obj).distinct()
        return field



@admin.register(BrandSeries)
class BrandSeriesAdmin(admin.ModelAdmin):
    extra = 0

class BrandSeriesInline(admin.TabularInline):
    model = BrandSeries
    formfield_overrides = FORMFIELD_OVERRIDES
    extra = 0


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name',]
    readonly_fields = ['slug']
    inlines = [
        BrandCategoryTextInline,
        BrandSeriesInline,
    ]

    fieldsets = (
        (None, {
            'fields': ('name','slug','description'),
        }),
        ('Image', {
            'fields': ('image',),
        }),
        ('Discount', {
            'fields': (('discount','discount_whoosale',), ('enable','disable',),),
        }),
        ('seo', {
            'fields': ('seo_title','seo_description','seo_keywords'),
        }),
    )


    formfield_overrides = FORMFIELD_OVERRIDES