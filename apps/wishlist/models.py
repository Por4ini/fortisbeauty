from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.timezone import now



class Wishlist(models.Model):
    user =    models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, verbose_name=_("Пользователь"), related_name='products')
    variant = models.ForeignKey('shop.Variant',    on_delete=models.CASCADE, verbose_name=_("Товар"))
    date =    models.DateTimeField(default=now)

    class Meta:
        ordering = ['-date']
        unique_together = [['user', 'variant']]

    def __str__(self):
        return ''

    def save(self):
        self.date = now()
        super(Wishlist, self).save()

