from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.user.models import *



class UserCompanyInline(admin.StackedInline):
    model=UserCompany
    extra=0




@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email','phone','first_name','last_name','created','is_active', 'is_whoosaler','want_be_whoosaler')
    list_filter = ('is_whoosaler','company__business_type','want_be_whoosaler','is_admin')
    fieldsets = (
        (None,          {'fields': ('first_name', 'last_name', 'father_name','city')}),
        ('Contacts',    {'fields': (('email','email_confirmed'),('phone','phone_confirmed'),'password', )}),
        ('Business',    {'fields': ('is_whoosaler','want_be_whoosaler','real_stock')}),
        ('Permissions', {'fields': ('is_admin', 'was_active','is_active')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ['-want_be_whoosaler','-is_whoosaler','-created']
    filter_horizontal = ()
    inlines = [
        UserCompanyInline
    ]


