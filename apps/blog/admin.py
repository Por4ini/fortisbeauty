from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.blog.models import BlogPost, BlogPostImages



class BlogPostImagesInline(admin.TabularInline):
    def image_preview(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="object-fit: contain; object-position: center; background-color: #e7eff3;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'], width=240, height=240))
            return img
        else:
            return '-'

    model = BlogPostImages
    readonly_fields = ['image_preview']
    fields = ['num','image_preview','image']
    extra = 0

   



@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    def image_preview(self, obj=None):
        if hasattr(obj, 'image'):
            try:
                return mark_safe("""<img style="object-fit: contain; object-position: center; background-color: #e7eff3;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'], width=240, height=240))
            except:
                pass
        return '-'



    image_preview.short_description ='Главное фото'

    inlines = [
        BlogPostImagesInline
    ]

    readonly_fields = ['image_preview']

    list_display = ['image_preview','name','date']

    fieldsets = (
        (None, {
            'fields': ('name','slug',)
        }),
        ('image', {
            'fields': ('image_preview','image')
        }),
        ('text', {
            'fields': ('text',),
        }),

    )