from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.loader import render_to_string 
from apps.user.models import CustomUser
from django.core.mail import send_mail






class PasswordRestoreForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordRestoreForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['data-type'] =   'email'
        self.fields['email'].widget.attrs['data-empty'] =  'Введите Ваш Email'
        self.fields['email'].widget.attrs['data-error'] =  'Email имеет не верный формат'
        self.fields['email'].widget.attrs['placeholder'] = 'Email *'


    def clean(self):
        cd = super().clean()
        email = cd['email']
        user = CustomUser.objects.filter(email=email).first()
        if user == None:
            raise forms.ValidationError([f"Пользователь с email: {email} не зарегестрирован в системе"])

    
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        cd = super().clean()
        message = render_to_string('user/password_restore/email_template.html', context=context)
        send_mail(
            subject = _('Востанволение пароля'),
            from_email = "office.fortisbeauty@gmail.com",
            recipient_list = [cd['email']],
            message = message,
            html_message = message,
            fail_silently = True,
        )
