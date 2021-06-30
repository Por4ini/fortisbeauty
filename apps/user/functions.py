from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from apps.user.tokens import account_activation_token
from unidecode import unidecode
import re


def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Активация Вашего аккаунта FortisBeauty'
    message = render_to_string('user/email/acc_activation_email.html', {
        'user':   user,
        'domain': current_site.domain,
        'uid':    urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8") ,
        'token':  account_activation_token.make_token(user),
    })
    email = send_mail(
        subject=mail_subject, 
        message='',
        from_email='office.fortisbeauty@gmail.com', 
        recipient_list=[user.email], 
        html_message=message, 
        fail_silently=False
    )
    return email


def ValidateEmail(email):
    validator = EmailValidator()
    try:
        validator(email)
    except ValidationError:
        return False
    return email

def ValidatePhone(phone):
    for symb in [' ','+','-','(',')','_','*']:
        phone = phone.replace(symb,'')
    phone = ''.join(filter(lambda x: x.isdigit(), phone))
    if 6 < len(phone) < 14: 
        phone = str(PhoneNumber.from_string(phone_number=phone, region='UA').as_e164).replace('+','')
        return phone
    else:
        return False


def ValidateUserName(username):
    if ValidateEmail(username) == False:
        for symb in [' ','+','-','(',')','_','*']:
            username = username.replace(symb,'')
        username = ''.join(filter(lambda x: x.isdigit(), username))
        if 6 < len(username) < 14: 
            phone = str(PhoneNumber.from_string(phone_number=username, region='UA').as_e164).replace('+','')
            return {'username':phone,'field':'phone'}
        else:
            return {'username':None, 'field': None}
    else:
        return {'username':username,'field':'email'}




















def UserDocs(instance, filename, document):
    path = ''
    ext = filename.split('.')[-1]
    path = 'media/user/' + str(instance.parent.pk) + '/' + document + '_'
    ext = filename.split('.')[-1]
    for par in [instance.parent.first_name, instance.parent.last_name, instance.parent.father_name]:
        if len(str(par)) > 0:
            path +=  slugify(unidecode(str(par))) + '_'
    path += '.' + ext
    return path

def passportPath(instance, filename):
    return UserDocs(instance, filename, document='passport')

def certificatePath(instance, filename):
    return UserDocs(instance, filename, document='certificate')



