from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response
from apps.shop.cart import Cart



@method_decorator(csrf_exempt, name='dispatch')
class CartViewSet(viewsets.ViewSet):
    def cart_html(self, data):
        return {
            'items' : render_to_string('shop/cart/cart__list.html', {'cart':data}),
            'total' : render_to_string('shop/cart/cart__total.html', {'cart':data}),
            'quantity' : data['quantity'],
            'amount' :  data['total'],
        }

    def order_html(self, data):
        return {
            'items' : render_to_string('shop/cart/cart__list.html', {'cart':data}),
            'order_items' : render_to_string('orders/order__products.html', {'cart':data}),
            'total' : render_to_string('shop/cart/cart__total.html', {'cart':data}),
            'quantity' : data['quantity'],
            'amount' :  data['total'],
        }


    def get(self, request, order=None):
        cart = Cart(request)
        data = cart.data()
        if request.GET.get('order'):
            return Response(self.order_html(data))
        return Response(self.cart_html(data))


    def add(self, request):
        order = request.data.get('order')
        cart = Cart(request)
        data = cart.add(request.data)
        if request.data.get('order'):
            return Response(self.order_html(data))
        return Response(self.cart_html(data))


    def delete(self, request):
        cart = Cart(request)
        data = cart.remove(request.data.get('id'))
        if request.data.get('order'):
            return Response(self.order_html(data))
        return Response(self.cart_html(data))

    def clear(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect('shop:catalogue')





