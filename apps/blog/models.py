from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.timezone import now
from apps.core.models import Translation, NameSlug, Images




class BlogPost(Translation, NameSlug, Images):
    image = models.FileField(max_length=1024, blank=False, verbose_name="Фото")
    text =  RichTextUploadingField(verbose_name='Текст', blank=True, null=True)
    date =  models.DateTimeField(default=now, verbose_name="Время")

    class Meta:
        ordering = ['-date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return 'Пост: ' +  self.name + ' ' + self.date.strftime('%m/%d/%Y')




class BlogPostImages(Images):
    parent =  models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотограии'