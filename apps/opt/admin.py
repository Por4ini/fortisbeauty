from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from apps.opt.models import WhoosaleText, BusinessTypes, BusinessPositions, BusinessDifficulties


@admin.register(WhoosaleText)
class WhoosaleTextAdmin(SingleModelAdmin):
    pass


@admin.register(BusinessTypes)
class BusinessTypesAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessPositions)
class BusinessPositionsAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessDifficulties)
class BusinessDisfficultiesAdmin(admin.ModelAdmin):
    pass


