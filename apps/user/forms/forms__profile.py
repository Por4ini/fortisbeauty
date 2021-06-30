from django import forms
from apps.user.models import CustomUser


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','phone','first_name','last_name','father_name','city']

    def __init__(self, language='ru', *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # EMAIL
        self.fields['email'].label = ''
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['data-type'] =   'text'
        self.fields['email'].widget.attrs['data-empty'] =  'Введите Ваш Email'
        self.fields['email'].widget.attrs['data-error'] =  'Email имеет не верный формат'
        self.fields['email'].widget.attrs['placeholder'] = 'Email *'
        # PHONE
        self.fields['phone'].label = ''
        self.fields['phone'].required = True
        self.fields['phone'].widget.attrs['data-type'] =   'text'
        self.fields['phone'].widget.attrs['data-empty'] =  'Введите Номер телефона'
        self.fields['phone'].widget.attrs['placeholder'] = 'Номер телефона *'
        # FIRST NAME
        self.fields['first_name'].label = ''
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['data-type'] =   'text'
        self.fields['first_name'].widget.attrs['data-empty'] =  'Введите Ваше имя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя *'
        # LAST NAME
        self.fields['last_name'].label = ''
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['data-type'] =   'text'
        self.fields['last_name'].widget.attrs['data-empty'] =  'Введите Вашу фамилию'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия *'
        # FATHER NAME
        self.fields['father_name'].label = ''
        self.fields['father_name'].required = True
        self.fields['father_name'].widget.attrs['data-type'] =   'text'
        self.fields['father_name'].widget.attrs['data-empty'] =  'Введите Ваше отчество'
        self.fields['father_name'].widget.attrs['placeholder'] = 'Отчество *'
        # CITY
        self.fields['city'].label = ''
        self.fields['city'].required = True
        self.fields['city'].widget.attrs['data-type'] =   'text'
        self.fields['city'].widget.attrs['data-empty'] =  'Ваш город для доставки'
        self.fields['city'].widget.attrs['placeholder'] = 'Город *'

      