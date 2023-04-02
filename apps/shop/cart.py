from django.core import serializers
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Case, When
from project import settings
from apps.shop.models import Product, Variant, VariantImages
from apps.shop.serializers import CartVartinatSerializer
import time
import json
import datetime


class Cart(object):
    def __init__(self, request):
        user = request.user
        self.whoosale = user.is_whoosaler if user.is_authenticated else False
        self.real_stock = user.real_stock if user.is_authenticated else True
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart

    def __iter__(self):
        for item in list(self.cart):
            yield item

    def get_number(self, id):
        for n, item in enumerate(self.cart):
            if int(item['id']) == int(id):
                return n
        return None

    def chack_exclude(self, ids, variants):
        ids_exists = [variant.id for variant in variants]
        ids_exclude = [n for n, id in enumerate(ids) if int(id) not in ids_exists]
        if len(ids_exclude) > 0:
            for n in sorted(ids_exclude, reverse=True):
                del self.cart[n]
            self.save()

    def add(self, data, update=False):
        id = int(data['id'])
        variant = Variant.objects.get(id=id)
        number = self.get_number(int(data['id']))
        quantity = data.get('quantity')

        if number is not None:
            if quantity:
                self.cart[number]['quantity'] = int(quantity)
            else:
                cur_qty = self.cart[number]['quantity']
                if self.real_stock and cur_qty >= variant.stock:
                    self.cart[number]['quantity'] = variant.stock
                else:
                    self.cart[number]['quantity'] += 0
        else:
            self.cart.append({'id': data['id'], 'quantity': quantity if quantity else 1})
        self.save()
        return self.data()

    def remove(self, id):
        number = self.get_number(id)
        if number != None:
            del self.cart[number]
            self.save()
        return self.data()

    def data(self):
        qty = 0
        data, total = [], 0

        # Get variant cart in cart
        ids = [item['id'] for item in self.cart]

        # Get variant objects
        variants = Variant.objects.filter(pk__in=ids)

        # Check if variant deleted from db
        self.chack_exclude(ids, variants)

        # Serialize and calculate total
        for item in self.cart:
            variant = variants.get(pk=item['id'])
            variant = CartVartinatSerializer(variant, context={'whoosale': self.whoosale}).data
            variant['quantity'] = int(item['quantity'])
            variant['total'] = int(variant['price']) * int(item['quantity'])
            total += variant['total']
            qty += variant['quantity']
            data.append(variant)
        print(data)
        return {'items': data, 'total': total, 'quantity': qty}

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()





