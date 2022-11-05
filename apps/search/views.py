from django.template.loader import render_to_string
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.shop.serializers.serializers__catalogue import ProductSerializer, VariantProductSerializer
from apps.shop.serializers.serializers__category import CategorySerializer
from apps.shop.serializers.serializers__brand import BrandLiteSerializer

from apps.shop.models import Product, Brand, Categories, Variant
import json


class SearchProduct(APIView):
    def search(self, data):
        variant_output = Variant.objects.filter(
            Q(code__icontains=data) |
            Q(parent__name__icontains=data) |
            Q(parent__human__icontains=data)
        )
        product_output = Product.objects.filter(
            Q(name__icontains=data) | Q(human__icontains=data)
        )
        brands_output = Brand.objects.filter(name__icontains=data)
        category_output = Categories.objects.filter(
            Q(human__icontains=data) |
            Q(name__icontains=data) |
            Q(parent__name__icontains=data) |
            Q(parent__human__icontains=data)
        )

        return variant_output, product_output, category_output, brands_output

    def post(self, request):
        data = request.data
        context = {}
        variant_output, product_output, category_output, brand_output = self.search(data['input'])

        if variant_output.count() > 0:
            context['variants'] = render_to_string(
                'base/header/search/search__variant.html', {
                    'variants': VariantProductSerializer(variant_output, many=True).data
                }
            )

        if product_output.count() > 0:
            product_output = product_output.exclude(variant__in=variant_output)
            context['products'] = render_to_string(
                'base/header/search/search__products.html', {
                    'products': ProductSerializer(product_output, many=True).data
                }
            )

        if brand_output.count() > 0:
            context['brands'] = render_to_string(
                'base/header/search/search__brands.html', {
                    'brands': BrandLiteSerializer(brand_output, many=True).data
                }
            )

        if category_output.count() > 0:
            context['categories'] = render_to_string(
                'base/header/search/search__categories.html', {
                    'categories': CategorySerializer(category_output, many=True).data
                }
            )
    
        return Response(context)