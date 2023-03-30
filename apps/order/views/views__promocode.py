from django.contrib import messages
from django.shortcuts import redirect
from project import settings
from ..models import PromoCode


def apply_promo(request):
    promo_code = request.POST.get('promo_code')
    try:
        promo_obj = PromoCode.objects.get(code=promo_code)
        messages.add_message(request, messages.SUCCESS, 'Промо-код успішно застосовано.')
        discount_percent = promo_obj.discount
        if discount_percent != 0:
            request.session[settings.DISCOUNT_SESSION_ID] = float(discount_percent)
    except PromoCode.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Недійсний промо-код.')
        request.session[settings.DISCOUNT_SESSION_ID] = 0

    return redirect('orders:order')
