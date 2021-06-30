from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import translation
from django.http import JsonResponse
from django.utils.translation import get_language
from apps.shop.models import Categories 
from apps.core.functions import send_telegeram
from project.settings import LANGUAGE_CODE
from project import settings
import json


def sitemap(request):
    categories = Categories.objects.all().prefetch_related('children', 'product', 'product__variant').distinct()
    return render(request, 'sitemap.xml', {'categories': categories}, content_type="application/xhtml+xml", )



def set_language(request, language):
    curent_language = get_language()
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    path = request.GET.get('path')
    if not path:
        path = reverse('shop:home')
    else:
        if language == LANGUAGE_CODE:
            path = path.replace(f'/{curent_language}/', '/')
        else:
            if curent_language == LANGUAGE_CODE:
                path = f'/{language}'+ path
            else:
                path = path.replace(f'/{curent_language}/', f'/{language}/')
    return redirect(path)




def recall(request):
    data = request.POST
    msg = [
        "Перезвонить. \n"
        "Телефон: " + data["phone"],
    ]
    send_telegeram(msg)
  
    prev_url = request.META.get('HTTP_REFERER')
    if prev_url:
        return redirect(prev_url)
    return redirect('/')