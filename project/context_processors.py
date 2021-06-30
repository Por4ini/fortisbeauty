from project.settings import LANGUAGES
from apps.shop.models import Brand

def languages(request):
    url = request.path.split('/')
    langList = []
    languages = {}

    for i in LANGUAGES:
        langList.append(i[0])

    for i in LANGUAGES:

            if (url[1] in langList) and (url[1] != ''):
                url[1] = i[0]
                if i[0] == 'zh-cn':
                    languages['zh'] = '/'.join(url)
                else:
                    languages[i[0]] = '/'.join(url)
            elif url[1] == '':
                if i[0] == 'zh-cn':
                    languages['zn'] = i[0]
                else:
                    languages[i[0]] = i[0]

    return {'languages': languages }

def brands(request):
    brands = Brand.objects.all()
    return {'brands' : brands}
