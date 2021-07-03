from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _
from apps.core.models import NameSlug
from apps.user.functions import *
import urllib.parse





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, admin=False, data={}):
        if not email:
            raise ValueError('Пользователь должен иметь адрес элетронной почты')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, admin=True)
        user.is_admin = True
        user.is_active = True
        user.is_staff= True
        user.save(using=self._db)
        return user





    

class CustomUser(AbstractBaseUser):
    email =             models.EmailField(unique=True)
    email_confirmed =   models.BooleanField(default=False, blank=True)
    phone =             models.CharField(max_length=40, blank=True)
    phone_confirmed =   models.BooleanField(default=False, blank=True)
    # PERSONAL INFO
    first_name =        models.CharField(max_length=30, blank=True, editable=True, verbose_name='Имя')
    last_name =         models.CharField(max_length=30, blank=True, editable=True, verbose_name='Фамилия')
    father_name =       models.CharField(max_length=30, blank=True, editable=True, verbose_name='Отчество')
    country =           models.CharField(max_length=30, blank=True, editable=True, verbose_name='Страна')
    city =              models.CharField(max_length=30, blank=True, editable=True, verbose_name='Город')
    # BUSINESS INFO
    is_whoosaler =      models.BooleanField(default=False, verbose_name='Оптовый покупатель')
    want_be_whoosaler = models.BooleanField(default=False, verbose_name='Хочет продавать оптом')
    real_stock =        models.BooleanField(default=True,  verbose_name='Покупать по реальному остатку')

    # COSMETOLOGIST
    certificate =       models.FileField(upload_to='certificate', blank=True, null=True, verbose_name='Сертификат')
    passport =          models.FileField(upload_to='passport', blank=True, null=True, verbose_name='Удостоверение личноти')
    # PASSWORD
    password =          models.CharField(max_length=500, blank=True)
    # PERMISION
    was_active =        models.BooleanField(default=False)
    is_admin =          models.BooleanField(default=False, verbose_name='Администратор')  
    is_active =         models.BooleanField(default=False, verbose_name='Аккаунт активирован')
    is_staff =          models.BooleanField(default=False, verbose_name='Персонал')      
    # DATETIME
    created =         models.DateTimeField(default=now)

    objects = CustomUserManager()
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        ordering = ['-created']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def get_absolute_url(self):
        return 'url'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        if self.is_whoosaler:
            self.want_be_whoosaler = False
        super(CustomUser, self).save(*args, **kwargs)








class UserAdress(models.Model):
    parent =     models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="adress")
    city =       models.CharField(max_length=500, verbose_name=_("Город"))
    street =     models.CharField(max_length=500, verbose_name=_("Улица"))
    house =      models.CharField(max_length=500, verbose_name=_("Дом"))
    appartment = models.CharField(max_length=500, verbose_name=_("Квартира / Офис"))

    def __str__(self):
        return f'г. {self.city}, ул. {self.street} {self.house}, кв. {self.appartment}'

    def save(self):
        super(UserAdress, self).save()
        if not hasattr(self.parent, 'adress_chosen'):
            chosen = UserAdressChosen(parent = self.parent, adress=self)
            chosen.save()


class UserAdressChosen(models.Model):
    parent =     models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='adress_chosen')
    adress =     models.ForeignKey(UserAdress, on_delete=models.CASCADE)



class UserNP(models.Model):
    parent =     models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="np")
    city =       models.CharField(max_length=500)
    branch =     models.CharField(max_length=500)

    def __str__(self):
        return ' '.join([self.city, self.branch])

class UserNPChosen(models.Model):
    parent =     models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="np_chosen")
    adress =     models.ForeignKey(UserNP, on_delete=models.CASCADE)



class UserCompany(models.Model):
    parent =        models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="company")
    name =          models.CharField(max_length=500, blank=False, editable=True, verbose_name=_("Название"))
    code =          models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("ЕДРПОУ"))

    position =      models.CharField(max_length=500, verbose_name='Должность', blank=True, null=True)
    company =       models.CharField(max_length=500, verbose_name='Организация', blank=True, null=True)
    business_type = models.ManyToManyField('opt.BusinessTypes', verbose_name='Тип бизнеса', blank=True)


    email =         models.EmailField(blank=False, null=True, unique=True, max_length=500, verbose_name=_("Корпоративный E-mail"))
    iban =          models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("Номер счета (IBAN)"))
    director =      models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("ФИО Директора"))
    adress =        models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("Юридический адрес"))



class UserSubscripton(models.Model):
    parent =   models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="subscription")
    category = models.ManyToManyField('shop.Categories', related_name="subscription")

    def __str__(self):
        return ', '.join([category.name for category in self.category.all()])

    class Meta:
        verbose_name = _('Подписка на категории')
        verbose_name_plural = _('Подписка на категории')














