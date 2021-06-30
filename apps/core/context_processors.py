from django.utils.translation import get_language as lang
from apps.core.models import Languages


def language_change(request):
    languages = {}
    current_lang = lang()
    path = str(request.path).replace('/' + str(current_lang) + '/', '')
    for language in Languages.objects.all():
        languages[language.code] = { 'path' : '/'.join([language.code,path]) , 'active' : True if language.code == current_lang else False}
    return {'languages':languages}