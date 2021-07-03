from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.functions import send_telegeram
from apps.user.models import CustomUser, UserCompany
from apps.opt.models import BusinessTypes, BusinessPositions, BusinessDifficulties
from apps.user.functions import send_activation_email_with_password
import urllib.request
import urllib.parse
import json
from django.contrib.auth.tokens import default_token_generator   




class SalonsView(APIView):
    def get(self, request):
        return render(request, 'opt/salons/quiz/base.html', {
            'business_types': BusinessTypes.objects.all(),
            'business_positions': BusinessPositions.objects.all(),
            'business_difficuties': BusinessDifficulties.objects.all()
        })


    def create_user(self, request, user, data, business_position=''):
        # Create user
        user = CustomUser(
            first_name = data['form']['name'],
            email = data['form']['email'],
            phone = data['form']['phone'],
            want_be_whoosaler = True
        )
        user.save()

        # Create user cimpany
        company = UserCompany(
            parent = user,
            position = business_position,
        )
        company.save()

        # Add business types
        for bt in data['business_type']['values']:
            obj = BusinessTypes.objects.get(id=int(bt['id']))
            company.business_type.add(obj)

        # Send email with activation link
        send_activation_email_with_password(request, user)
        return user



    def post(self, request):
        data = request.data

        business_types =       ', '.join([item['value'] for item in data['business_type']['values']] + [data['business_type']['custom']])
        business_position =    ', '.join([item['value'] for item in data['business_position']['values']] + [data['business_position']['custom']])
        business_difficuties = ', '.join([item['value'] for item in data['business_difficuties']['values']] + [data['business_difficuties']['custom']])

        user = CustomUser.objects.filter(email=data['form']['email']).first()
        if not user:
            user = self.create_user(request, user, data, business_position)
        
        msg = [
            "ОПТ. Получить КП. \n",
            "Имя: " + data['form']["name"], 
            "Телефон: " + data['form']["phone"], 
            "Email: " +  data['form']["email"], 
            "1. Тип бизнеса: "    + business_types,
            "2. Должность: "      + business_position,
            "3. Месячный доход: " + data["income"],
            "4. Трудности: "      + business_difficuties,
        ]

        send_telegeram(msg)
        return Response({'success': True})
            





def get_analitics(request):
    args = {}
    if 'user' in request.session.keys():
        args['user'] = request.session['user']
    if request.method == 'POST':
        if 'user' in request.session.keys():
            del request.session['user']
        data = dict(request.POST)

        msg = [
            "ОПТ. Получить разбор. \n"
            "1. Бренды с которыми Вы работаете: "+ data["brand_work_hidden"][0] + ', ' + data["brand_i_want_hidden"][0],
            "2. Бренды с которыми Вы хотели бы работать: " + data["brand_i_want_hidden"][0],
            "3. Средний чек: " + data["avarage_check"][0],
            "4. Месячный доход: "  + data["month_income"][0],
            "Имя: " + data["name"][0], "телефон: " + data["phone"][0], "Email: " + data["email"][0], 
        ]
        request.session['user'] = data
        msg = urllib.parse.quote('\n'.join(msg))
        url = "https://api.telegram.org/bot817785032:AAG-Q3s8wRhyZbkoJScSPvE2XDrCVlgZKKA/sendMessage?chat_id=-1001490724377&text=" + msg
        contents = urllib.request.urlopen(url).read()
        return HttpResponseRedirect(reverse('opt:success', args={}))
    return render(request, 'opt/salons/get_analysis.html',args)


