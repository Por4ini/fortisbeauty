from django.contrib import admin
from apps.pages.models import (
    Page,
    PageContacts,
    PageAbout,
    PageReturnProd,
    PagePayment,
    PageDelivery,
    PageTermsOfUse
)
from singlemodeladmin import SingleModelAdmin


@admin.register(PageContacts)
class PageContactsAdmin(SingleModelAdmin):
    pass


@admin.register(PageAbout)
class PageAboutAdmin(SingleModelAdmin):
    pass


@admin.register(PageReturnProd)
class PageAboutAdmin(SingleModelAdmin):
    pass


@admin.register(PagePayment)
class PagePaymentAdmin(SingleModelAdmin):
    pass


@admin.register(PageDelivery)
class PageDeliveryAdmin(SingleModelAdmin):
    pass


@admin.register(PageTermsOfUse)
class PageTermsOfUseAdmin(SingleModelAdmin):
    pass





# class PageInline(admin.TabularInline):
#     model = Page
#     fields = [
#         'image','name','text'
#     ]


# @admin.register(PageGroup)
# class PageGroupAdmin(admin.ModelAdmin):
#     inlines = [
#         PageInline
#     ]


# @admin.register(Page)
# class PageAdmin(admin.ModelAdmin):
#     pass
