from django.contrib import admin
from apps.sync1c.models import RequestData1CSettings, RequestData1C
# Register your models here.

@admin.register(RequestData1CSettings)
class RequestData1CSettingsAdmin(admin.ModelAdmin):
   list_display = ('ip',)



@admin.register(RequestData1C)
class RequestData1CAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['date']}),
        ('JSON', {'fields': ['detail_json_formatted']}),
    ]
    list_display = ('date',)
    readonly_fields = ('data', 'detail_json_formatted')

