from django.db import models
from apps.shop.models import Product
from apps.user.models import CustomUser
from mptt.models import MPTTModel, TreeForeignKey




class Comment(models.Model):
    TYPES = (
        ("COMMENT",  "Comment"),
        ("QUESTION", "Question"),
    )
    RATE = ((5, 5),(4, 4),(3, 3),(2, 2),(1, 1))

    type =           models.CharField(max_length=10, choices=TYPES, default="COMMENT")
    product =        models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate =           models.PositiveIntegerField(choices=RATE, default=5, verbose_name="Оцените товар", blank=True, null=True)
    text =           models.TextField(blank=True, null=True, verbose_name="Комментарий")
    advantages =     models.CharField(max_length=1200, blank=True, null=True, verbose_name="Преимущества")
    disadvantages =  models.CharField(max_length=1200, blank=True, null=True, verbose_name="Недостатки")
    date =           models.DateTimeField(auto_now=False, auto_now_add=True)
    like =           models.PositiveIntegerField(default=0)
    dislike =        models.PositiveIntegerField(default=0)

    @property
    def get_rate(self):
        return [int(i < self.rate) for i in range(0, 5)]



class Reply(MPTTModel):
    parent =   TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    comment =  models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replys")
    user =     models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text =     models.TextField(blank=True, null=True, verbose_name="Комментарий")
    date =     models.DateTimeField(auto_now=False, auto_now_add=True)
    like =     models.PositiveIntegerField(default=0)
    dislike =  models.PositiveIntegerField(default=0)

