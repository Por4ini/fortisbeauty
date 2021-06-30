from rest_framework import serializers
from apps.order.models import Order, OrderProduct
from apps.shop.models import Variant, VariantImages
from apps.shop.serializers import VariantSerializer



class OrderVariantimagesImagesSerializer(serializers.ModelSerializer):
    s =     serializers.CharField(source="image_thmb.s.path",  allow_blank=True, read_only=True)

    class Meta:
        model = VariantImages
        fields = ['s']


class OrderVariantSerializer(serializers.ModelSerializer):
    images = OrderVariantimagesImagesSerializer(many=True, read_only=True)
    name =   serializers.CharField(source="parent.name", read_only=True)
    brand =      serializers.CharField(source="parent.brand.name", read_only=True)
    brand_url =  serializers.CharField(source="parent.brand.get_absolute_url", read_only=True)
    url =    serializers.CharField(source="get_absolute_url", read_only=True)

    class Meta:
        model = Variant
        fields = [
            'id','price','value','images','url','name','brand','brand_url'
        ]



class OrderProductSerializer(serializers.ModelSerializer):
    variant = OrderVariantSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = [
            'id','quantity','price','total','variant'
        ]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)
    status =   serializers.CharField(source="get_status_display")
    pay_type = serializers.CharField(source="get_pay_type_display")
    created =  serializers.DateTimeField(format="%m:%H - %d.%m.%Y")
    total =    serializers.CharField(source="get_total")

    class Meta:
        model = Order
        fields = [
            'id','status','pay_type','created','products','total'
        ]