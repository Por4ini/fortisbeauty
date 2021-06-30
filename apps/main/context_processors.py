from apps.main.models import Phones, MainData


def PhonesContext(request):
    phones = Phones.objects.all()
    maindata = MainData.objects.first()
    return {
        'phones' : phones,
        'maindata' : maindata,
    }