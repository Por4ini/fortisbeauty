from django.shortcuts import render
from apps.shop.cart import Cart


def order_success(request):
    cart = Cart(request)
    cart.clear()
    request.session['promo_data'] = {'brand_id': None, 'discount': 0}
    request.session['promo_code'] = None
    return render(request, 'orders/order__success.html', {'cart' : cart.data})
