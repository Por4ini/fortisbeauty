from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from apps.opt.models import Quiz, WhoosaleText


@admin.register(WhoosaleText)
class WhoosaleTextAdmin(SingleModelAdmin):
    pass


# @admin.register(Quiz)
# class QuizAdmin(admin.ModelAdmin):
#     pass