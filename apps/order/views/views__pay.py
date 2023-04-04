from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.shop.cart import Cart
from apps.order.models import PaymentResponses
from apps.order.functions.create import CreateOrder
import json
import time
import hmac




class OrderPay(APIView):
    def get_request_data(self, request_data, cart_data, order_id):
        request_data = {
            'merchantAccount' : 'fortisbeauty_com_ua',
            'merchantAuthType' : 'SimpleSignature',
            'merchantDomainName' : 'fortisbeauty.store',
            'merchantTransactionType' : 'AUTO',
            'merchantSignature' : '',
            'language' : 'AUTO',
            'returnUrl' : 'https://fortisbeauty.store' + reverse('order:payment_response'),
            'serviceUrl' : 'https://fortisbeauty.store' + reverse('order:payment_response'),
            'orderReference' : int(time.time()) - 1622730000,
            'orderDate' : int(time.time()),
            'amount' : cart_data['total'],
            'currency' : 'UAH',
            'productName' :  [product['name']     for product in cart_data['items']],
            'productPrice' : [product['price']    for product in cart_data['items']],
            'productCount' : [product['quantity'] for product in cart_data['items']],
            'deliveryList' : [],
            'clientFirstName' : request_data['first_name'], 					
            'clientLastName' : request_data['last_name'], 				
            'clientEmail' : request_data['email'], 				
            'clientPhone': request_data['phone'], 
        }
        return request_data


    def sign(self, data):
        s = ';'.join([
            data['merchantAccount'],
            data['merchantDomainName'],
            str(data['orderReference']),
            str(data['orderDate']),
            str(data['amount']),
            data['currency'],
        ])
        for item in data['productName']:
            s += ';' + str(item)
        for item in data['productCount']:
            s += ';' + str(item)
        for item in data['productPrice']:
            s += ';' + str(item)
        return s

                
    def post(self, request):
        cart = Cart(request)
        order = CreateOrder(data=request.data, user=request.user, cart=cart, request=request)
        order = order.create_order(request)
        data = self.get_request_data(request.data, cart.data(), order.id)
        order.reference = int(data['orderReference'])
        order.save()
        sign = self.sign(data)
        data['merchantSignature'] = hmac.new(
            "d4501f69fdf17e81127e9a36f2cade9651439818".encode('utf-8'), 
            sign.encode('utf-8'), 'MD5'
        ).hexdigest()
        return Response({'data': data,})
       

class OrderPrePay(APIView):
    def get_request_data(self, request_data, cart_data, order_id):
        request_data = {
            'merchantAccount': 'fortisbeauty_com_ua',
            'merchantAuthType': 'SimpleSignature',
            'merchantDomainName': 'fortisbeauty.store',
            'merchantTransactionType': 'AUTO',
            'merchantSignature': '',
            'language': 'AUTO',
            'returnUrl': 'https://fortisbeauty.store' + reverse('order:payment_response'),
            'serviceUrl': 'https://fortisbeauty.store' + reverse('order:payment_response'),
            'orderReference': int(time.time()) - 1622730000,
            'orderDate': int(time.time()),
            'amount': 200,
            'currency': 'UAH',
            'productName': [product['name'] for product in cart_data['items']],
            'productPrice': [product['price'] for product in cart_data['items']],
            'productCount': [product['quantity'] for product in cart_data['items']],
            'deliveryList': [],
            'clientFirstName': request_data['first_name'],
            'clientLastName': request_data['last_name'],
            'clientEmail': request_data['email'],
            'clientPhone': request_data['phone'],
        }
        return request_data

    def sign(self, data):
        s = ';'.join([
            data['merchantAccount'],
            data['merchantDomainName'],
            str(data['orderReference']),
            str(data['orderDate']),
            str(data['amount']),
            data['currency'],
        ])
        for item in data['productName']:
            s += ';' + str(item)
        for item in data['productCount']:
            s += ';' + str(item)
        for item in data['productPrice']:
            s += ';' + str(item)
        return s

    def post(self, request):
        cart = Cart(request)
        order = CreateOrder(data=request.data, user=request.user, cart=cart, request=request)
        order = order.create_order(request)
        data = self.get_request_data(request.data, cart.data(), order.id)
        order.reference = int(data['orderReference'])
        order.save()
        sign = self.sign(data)
        data['merchantSignature'] = hmac.new(
            "d4501f69fdf17e81127e9a36f2cade9651439818".encode('utf-8'),
            sign.encode('utf-8'), 'MD5'
        ).hexdigest()
        return Response({'data': data, })
       



@csrf_exempt
def payment_response(request):
    resp = PaymentResponses(response='response')
    resp.save()

    if request.method == "POST":
        resp = PaymentResponses(response=dict(request.POST.lists()))
        resp.save()
        HttpResponse(status=200)
    return HttpResponse(status=404)

