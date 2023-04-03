from django.contrib import messages
from django.shortcuts import redirect
from project import settings
from ..models import PromoCode
from ...shop.cart import Cart

def apply_promo(request):
    promo_code = request.POST.get('promo_code')
    try:
        promo_obj = PromoCode.objects.get(code=promo_code)
        brand_id = promo_obj.brand.id
        discount = promo_obj.discount
        promo_code = promo_obj.code
        request.session['promo_code'] = promo_code
        request.session['promo_data'] = {'brand_id': brand_id, 'discount': int(discount)}
        messages.add_message(request, messages.SUCCESS, 'Промо-код успішно застосовано.')
    except PromoCode.DoesNotExist:
        request.session['promo_data'] = {'brand_id': None, 'discount': 0}
        request.session['promo_code'] = None
        messages.add_message(request, messages.ERROR, 'Недійсний промо-код.')


    return redirect('orders:order')
