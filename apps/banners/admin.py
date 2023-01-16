from apps.core import models
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Banner, BannerPC, BannerMobile, BannerOpt, BannerOptPC, BannerOptMobile




class BannerPCInlinbe(admin.TabularInline):
    def get_image(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="object-fit: cover; object-position: center;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'],  width=480, height=240))
            return img
        else:
            return '-'

    get_image.short_description = 'Изображение'

    fields = ['get_image','image']
    readonly_fields = ['get_image']
    model = BannerPC
    extra = 1


class BannerMobileInlinbe(admin.TabularInline):
    def get_image(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="object-fit: cover; object-position: center;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'],  width=240, height=480))
            return img
        else:
            return '-'

    get_image.short_description = 'Изображение'

    readonly_fields = ['get_image']
    fields = ['get_image','image']
    model = BannerMobile
    extra = 1

    
@admin.register(Banner)
class BannerAdmain(admin.ModelAdmin):
    inlines = [
        BannerPCInlinbe,
        BannerMobileInlinbe,
    ]
    list_display = ['date','title','description','link']
    fieldsets = (
        (_('Заголовок и текст'), {
            'fields': ('title','description',),
        }),
        (_('Ссылка'), {
            'fields': ('link',)
        }),
    )
    
    
class BannerOptPCInlinbe(admin.TabularInline):
    def get_image(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="object-fit: cover; object-position: center;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'],  width=480, height=240))
            return img
        else:
            return '-'

    get_image.short_description = 'Изображение'

    fields = ['get_image','image']
    readonly_fields = ['get_image']
    model = BannerOptPC
    extra = 1


class BannerOptMobileInlinbe(admin.TabularInline):
    def get_image(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="object-fit: cover; object-position: center;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'],  width=240, height=480))
            return img
        else:
            return '-'

    get_image.short_description = 'Изображение'

    readonly_fields = ['get_image']
    fields = ['get_image','image']
    model = BannerOptMobile
    extra = 1


@admin.register(BannerOpt)
class BannerOptAdmain(admin.ModelAdmin):
    inlines = [
        BannerOptPCInlinbe,
        BannerOptMobileInlinbe,
    ]
    list_display = ['title','description']
    fieldsets = (
        (_('Заголовок и текст'), {
            'fields': ('title','description',),
        }),
    )