from django.urls import reverse
from django.utils.encoding import force_text
from apps.core.functions import send_telegeram
from apps.order.models import Order, OrderProduct, OrderDeliveryNP, OrderDeliveryCurier
from apps.shop.models import Variant
from apps.user.models.models__user import UserAdress, UserNP
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class CreateOrder():
    def __init__(self, data, user, cart):
        self.data = data
        self.user = user
        self.cart = cart


    def send_to_telegram(self, order):
        obj = order
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])

        title = 'Заказ'
        if order.whoosale:
            title = 'Оптовый заказ'

        msg = [
            title + '\n',
            ' '.join([obj.name,obj.surname]),
            'Телефон: ' + order.phone,
            'https://fortisbeauty.store' + url,
        ]

        for n, product in enumerate(order.products.all()):
            msg.append('\n')
            msg.append(f'{str(n + 1)}. {product.variant.code}, {product.variant.parent.name}, {product.variant.value}')
            
            if product.variant.stock <= 5:
                msg.append(f'Передзамовлення {str(product.quantity)}шт. х {str(product.price)} грн. = {str(product.total)}' )
            else:
                msg.append(f'{str(product.quantity)}шт. х {str(product.price)} грн. = {str(product.total)}')
        
        
        msg.append('\n')
        msg.append(f'Всего: {str(order.get_total())}', )

        send_telegeram(msg)

    
    def send_email_order(self, order):
        user = self.user
        data = self.data
        mail_subject = 'Ваше замовлення FortisBeuty.'

        html = render_to_string('orders/order__email.html', context={
            'user': user,
            'cart': order.products.all(),
            'total' : order.get_total(),

        },
                                )

        email = EmailMessage(
            mail_subject,
            html,
            'office.fortisbeauty@gmail.com',
            [data.get('email')],
            headers={
                'Reply-To': 'office.fortisbeauty@gmail.com'
            }
        )
        email.content_subtype = "html"
        email.send()
    
    
    def add_products(self, order):
        for item in self.cart:
            variant = Variant.objects.filter(pk=item['id']).first()
            if variant:
                order_product = OrderProduct(
                    parent=order,
                    variant=variant,
                    quantity=int(item['quantity']),
                    price=int(variant.price)
                )
                order_product.save()


    def save_delivery(self, order):
        data = self.data
        # Saving to NewPost models
        if self.data['delivery'] == 'newpost':
            delivery_np = OrderDeliveryNP(
                parent=order, 
                city=data.get('city'), 
                branch=data.get('branch')
            )
            delivery_np.save()  
            if self.user.is_authenticated:
                if UserNP.objects.all().count() == 0:
                    np = UserNP(
                        parent = self.user,
                        city = delivery_np.city,
                        branch =  delivery_np.branch,
                    )
                    np.save()
        
        # Saving to Curier models
        elif self.data['delivery'] == 'curier':
            delivery_curier = OrderDeliveryCurier(
                parent=order, 
                city=data.get('city'), 
                street=data.get('street'), 
                house=data.get('house'), 
                appartment=data.get('appartment'),
            )
            delivery_curier.save()

            if self.user.is_authenticated:
                if UserAdress.objects.all().count() == 0:
                    adress = UserAdress(
                        parent=self.user,
                        city=delivery_curier.city,
                        street=delivery_curier.street,
                        house=delivery_curier.house,
                        appartment=delivery_curier.appartment,
                    )
                    adress.save()


                    

    def create_order(self):
        data = self.data
        user = self.user

        order = Order(
            status =     'new',
            name =       data.get('first_name'),
            surname =    data.get('last_name'),
            patronymic = data.get('father_name'),
            phone =      data.get('phone'),
            email =      data.get('email'),
            pay_type =   data.get('pay_type'),
            delivery_type =  data.get('delivery'),
            user = user if user.is_authenticated else None,
            whoosale = user.is_whoosaler if user.is_authenticated else False,
        )
        order.save()
        self.order = order


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



        self.add_products(order)
        self.save_delivery(order)
        self.send_email_order(order)
        self.send_to_telegram(order)
        return order
