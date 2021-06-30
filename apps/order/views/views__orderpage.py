from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.user.models import UserAdressChosen
from apps.shop.cart import Cart


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    context = {}

    def api(self, request, delivery=None):
        change_adress = request.data.get('change_adress')
        user = request.user
        if change_adress and user.is_authenticated:
            if hasattr(user, 'adress_chosen'):
                user.adress_chosen.delete()
            adress = UserAdressChosen(
                parent = request.user,
                adress = user.adress.get(pk=int(change_adress))
            )
            adress.save()
        args = {'user' : user}
        if delivery in ['newpost', None]:
            html = render_to_string('orders/delivery/delivery__newpost.html', args)
        else:
            html = render_to_string('orders/delivery/delivery__curier.html', args)
        return Response({'html' : html})

    
    def data(self, request, delivery=None):
        cart = Cart(request)
        data = cart.data()
        if data.get('quantity') in [0, None]:
            return redirect(reverse('shop:catalogue'))
        context = {'delivery' : delivery}
        return render(request, 'orders/order.html', context)