from django.contrib import admin
from .models import LoadProductsFromTable, LoadProductsImages
from singlemodeladmin import SingleModelAdmin



@admin.register(LoadProductsImages)
class LoadProductsImagesAdmin(SingleModelAdmin):
    pass


@admin.register(LoadProductsFromTable)
class LoadProductsFromTableAdmin(SingleModelAdmin):
    list_display = ['date','brand_name']
  
    