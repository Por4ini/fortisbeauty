from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from apps.main.models import Phones, MainData, Message, Slogan, OurAdvantages


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
    pass



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['date','subject','first_name','email','phone','text']
