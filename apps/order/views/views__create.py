from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from apps.shop.cart import Cart
from apps.order.functions.create import CreateOrder



class CreateOrderView(View):
    def post(self, request):
        order = CreateOrder(data=request.POST, user=request.user, cart=Cart(request))
        order = order.create_order()

        user = request.user
        if user.is_authenticated:
            changed = False

            fields = [
                ('name', 'first_name'),
                ('surname', 'last_name'),
                ('patronymic', 'father_name'),
                ('phone', 'phone'),
                ('email', 'email')
            ]

            for field in fields:
                if getattr(user, field[1]) in [None, '']:
                    print(field[0], field[1])
                    setattr(user, field[1], getattr(order,field[0]))
                    changed = True

            if changed:
                user.save()
            
        return redirect(reverse('order:success'))