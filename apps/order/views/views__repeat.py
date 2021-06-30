from django.shortcuts import redirect
from apps.order.models import Order
from apps.shop.cart import Cart
from django.views import View


class OrderRepeat(View):
    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except:
            return redirect('shop:catalogue')
        cart = Cart(request)
        for product in order.products.all():
            cart.add({'id': product.variant.id, 'quantity': product.quantity })
        return redirect('order:order')