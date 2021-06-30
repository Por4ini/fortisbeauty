from django.shortcuts import render
from apps.shop.cart import Cart


def order_success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'orders/order__success.html')
