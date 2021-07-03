from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from apps.user.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)


    class Meta:
        model = CustomUser
        fields = [
            'email','phone','password1','password2','first_name','last_name','father_name','city'
        ]

    def __init__(self,*args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # EMAIL
        self.fields['email'].label = ''
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['data-type'] =   'email'
        self.fields['email'].widget.attrs['data-empty'] =  'Введите Ваш Email'
        self.fields['email'].widget.attrs['data-error'] =  'Email имеет не верный формат'
        self.fields['email'].widget.attrs['placeholder'] = 'Email *'
        self.fields['email'].widget.attrs['id'] = 'user_registration_email'
        # PHONE
        self.fields['phone'].label = ''
        self.fields['phone'].required = True
        self.fields['phone'].widget.attrs['data-type'] =   'text'
        self.fields['phone'].widget.attrs['data-empty'] =  'Введите Номер телефона'
        self.fields['phone'].widget.attrs['placeholder'] = 'Номер телефона *'
        self.fields['phone'].widget.attrs['id'] = 'user_registration_phone'
        # PASSWORD-1
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Придумайте пароль'
        self.fields['password1'].widget.attrs['data-type'] =   'password'
        self.fields['password1'].widget.attrs['data-empty'] = 'Введите пароль'
        self.fields['password1'].widget.attrs['data-error'] = 'от 6-ти символов латиницы и содержать цифры'
        self.fields['password1'].widget.attrs['id'] = 'user_registration_password1'
        # PASSWORD-2
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['placeholder'] = 'Пароль еще раз'
        self.fields['password2'].widget.attrs['data-type'] =   'password2'
        self.fields['password2'].widget.attrs['data-parent'] = 'user_registration_password1'
        self.fields['password2'].widget.attrs['data-empty'] = 'Поаторите проль'
        self.fields['password2'].widget.attrs['data-error'] = 'Пароли не совпадают'
        self.fields['password2'].widget.attrs['id'] = 'user_registration_password2'
        # FIRST NAME
        self.fields['first_name'].label = ''
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['data-type'] =   'text'
        self.fields['first_name'].widget.attrs['data-empty'] =  'Введите Ваше имя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя *'
        self.fields['first_name'].widget.attrs['id'] = 'user_registration_first_name'
        # LAST NAME
        self.fields['last_name'].label = ''
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['data-type'] =   'text'
        self.fields['last_name'].widget.attrs['data-empty'] =  'Введите Вашу фамилию'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия *'
        self.fields['last_name'].widget.attrs['id'] = 'user_registration_last_name'
        # FATHER NAME
        self.fields['city'].label = ''
        self.fields['city'].required = False
        self.fields['city'].widget.attrs['data-type'] = 'text'
        self.fields['city'].widget.attrs['data-empty'] =  'Введите Ваш город проживания'
        self.fields['city'].widget.attrs['placeholder'] = 'Город'
        self.fields['city'].widget.attrs['id'] = 'user_registration_city'
        

       
    def clean(self):
        cd = super().clean()
        errors = []
        user = CustomUser.objects.filter(email=cd['email']).first()
        if user:
            errors.append("Такой пользователь уже зарегестрирован")
       
        if len(errors):
            raise forms.ValidationError(errors)