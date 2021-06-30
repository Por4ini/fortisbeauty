from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.opt.models import Quiz
from apps.core.functions import send_telegeram
import urllib.request
import urllib.parse




def salons(request):
    args = {}
    if request.method == 'POST':
        data = dict(request.POST)
        request.session['user'] = data
        
        msg = [
            "ОПТ. Получить КП. \n"
            "1. Тип бизнеса: "    + data["business_type_hidden"][0] + ', ' + data["business_type_custom"][0],
            "2. Должность: "      + data["position_hidden"][0] + ', ' + data["position_custom"][0],
            "3. Месячный доход: " + data["month_income"][0],
            "4. Трудности: "      + data["difficulties_hidden"][0] + ', ' + data["difficulties_custom"][0],
            "Имя: " + data["name"][0], "телефон: " + data["phone"][0], "Email: " + data["email"][0], 
        ]
        send_telegeram(msg)
        return HttpResponseRedirect(reverse('opt:get_analitics', args={}))
    return render(request, 'opt/salons/quiz/quiz__base.html',args)

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



def salonsTwo(request):
    args = {}
    if request.method == 'POST':
        data = request.POST

        quiz = Quiz(
            business = data['business_type_hidden'],
            business_custom = data['business_type_custom'],
            brand_work =   data['brand_work_hidden'],
            brand_i_want = data['brand_i_want_hidden'],
            budjet_clien = data['budget_hidden'],
            budjet_month = data['month_budjet_hidden'],
            gift = data['gift_hidden'],
            gift_custom = data['gift_custom'],
            name = data['name'],
            phone = data['phone'],
            email = data['email']
        )
        quiz.save()

        text = "Опт - Салон \n" 
        text += f"Имя: {data['name']}\n" 
        text += f"Телефон: {data['phone']}" 

        msg = urllib.parse.quote(text)
        url = "https://api.telegram.org/bot817785032:AAG-Q3s8wRhyZbkoJScSPvE2XDrCVlgZKKA/sendMessage?chat_id=-1001490724377&text=" + msg
        contents = urllib.request.urlopen(url).read()

        return HttpResponseRedirect(reverse('opt:success', args={}))
    return render(request, 'opt/salons/salons.html', args)