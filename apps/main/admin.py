from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from apps.main.models import Phones, MainData, Message, Slogan, OurAdvantages, OurAdvantagesPC


class OurAdvantegesPCInlinbe(admin.TabularInline):
    def get_image(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="object-fit: cover; object-position: center;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'],  width=480, height=480))
            return img
        else:
            return '-'

    get_image.short_description = 'Изображение'

    fields = ['get_image','image']
    readonly_fields = ['get_image']
    model = OurAdvantagesPC
    extra = 1


@admin.register(Phones)
class PhonesAdmin(admin.ModelAdmin):
    list_display = ('phone',)
    fields = ['image','name','phone']


@admin.register(MainData)
class MainDataAdmin(SingleModelAdmin):
    pass

@admin.register(Slogan)
class SloganAdmin(SingleModelAdmin):
    pass


@admin.register(OurAdvantages)
class OurAdvantagesAdmin(admin.ModelAdmin):
    inlines = [
        OurAdvantegesPCInlinbe,
        
    ]
    

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['date','subject','first_name','email','phone','text']
