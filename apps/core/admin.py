from django.contrib import admin
from .models import *



@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    pass

