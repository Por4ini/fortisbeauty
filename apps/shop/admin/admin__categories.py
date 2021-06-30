from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin
from apps.shop.models import Categories, CategoryChildRel, GoogleTaxonomy, GoogleTaxonomyCategories 




@admin.register(GoogleTaxonomyCategories)
class GoogleTaxonomyCategoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(GoogleTaxonomy)
class GoogleTaxonomyAdmin(SingleModelAdmin):
    pass



class CategoryChildRelInline(admin.TabularInline):
    model = CategoryChildRel
    fk_name = 'parent'
    extra = 0



@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('parent','name','human',)
        }),
        ('Излбражение', {
            'fields': ('image',),
        }),
        ('taxonomy', {
            'fields': ('taxonomy',),
        }),
        ('seo', {
            'fields': ('seo_title','seo_description','seo_keywords',)
        }),
    )