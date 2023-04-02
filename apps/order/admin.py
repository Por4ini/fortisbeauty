from apps.order.models import *
from apps.order.models import PromoCode
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.db import models
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin




class OrderProductInline(admin.StackedInline):
    def get_image(self, obj=None):
        url = obj.variant.get_absolute_url()

        try:    image = obj.variant.images.first().image_thmb['s']['path']
        except: image = ''
    
        img = mark_safe("""<a href="{url}" target="_blank">
            <img style="object-fit: contain; object-position: center;" src="{image}" width="240" height="240" />
        </a>""".format(
            image=image, url=url
        ))
        return img
    
    get_image.short_description = 'Фото'

    formfield_overrides = {
        models.ForeignKey: {'widget': AutocompleteSelect(
            OrderProduct.variant.field.remote_field,
            admin.site,
            attrs={'style': 'width: 600px'} 
        )},
    }
    readonly_fields = ['get_image']
    autocomplete_fields = ['variant']
    model = OrderProduct
    extra = 0


    fieldsets = (
        ('Товар',           {'fields': ('get_image','variant','quantity','price','total')}),
    )


@admin.register(PaymentResponses)
class PaymentResponsesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('JSON', {'fields': ['detail_json_formatted']}),
    ]
    readonly_fields = ('detail_json_formatted',)



class OrderDeliveryNPAdmin(admin.StackedInline):
    model = OrderDeliveryNP
    extra = 0


class OrderDeliveryCurierAdmin(admin.StackedInline):
    model = OrderDeliveryCurier
    extra = 0
    
   
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderProductInline,
        OrderDeliveryNPAdmin,
        OrderDeliveryCurierAdmin,
    ]

    list_display = [
        'created',
        'status',
        'pay_type',
        'name',
        'surname',
        'patronymic',
        'phone',
        'email',
        'payed',
        'whoosale',
    ]

    fieldsets = (
        ('Статус заказа',     {'fields': ('status',)}),
        ('Способ оплыты',     {'fields': ('pay_type',)}),
        ('Способ доставки',   {'fields': ('delivery_type','delivery_cost')}),
        ('Клиент',            {'fields': ('user','name','surname','patronymic',)}),
        ('Контакты',          {'fields': ('phone','email',)}),
        ('Опт',               {'fields': ('whoosale',)}),
        ('Время',             {'fields': (('created','payed'),)}),
    )


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'created_at')
