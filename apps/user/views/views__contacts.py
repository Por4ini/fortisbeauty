from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.user.models import CustomUser
import json



@require_http_methods(["POST"])
def user_subscribe(request):
    args = {}
    data = json.loads(request.body.decode('utf-8'))
    # GET OR CREATE USER
    try:    
        user = CustomUser.objects.get(**{ user_data['field'] : user_data['username'] })
        user.subscribed = True
        user.save()
    except: 
        user = CustomUser.objects.create_user(username=user_data['username'], data=data)

    msg = 'Спасибо что проявили интерес к нашим новостям. Подписка оформлена. Email: %s' % user.email

    response =  json.dumps({'status' : msg}, ensure_ascii=False).encode('utf8')
    return JsonResponse(json.loads(response.decode('utf8')))


