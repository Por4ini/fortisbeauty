from apps.shop.models.models__categories import Categories
from django.template.loader import render_to_string
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl.query import MultiMatch
from apps.search.documents import ProductDocument, CategoryDocument, BrandDocument
from apps.shop.serializers.serializers__catalogue import ProductSerializer, VariantProductSerializer
from apps.shop.serializers.serializers__category import CategorySerializer
from apps.shop.serializers.serializers__brand import BrandLiteSerializer

from apps.shop.models import Variant 
import json


class SearchProduct(APIView):
    def search(self, data):
        variant_output = Variant.objects.filter(Q(code__icontains=data) | Q(parent__name__icontains=data) | Q(parent__human__icontains=data))

        product_query = MultiMatch(query=data, fields=['name','human'], fuzziness='AUTO')
        product_output = ProductDocument.search().query(product_query)

        brands_query = MultiMatch(query=data, fields=['name','slug'], fuzziness='AUTO')
        brands_output = BrandDocument.search().query(brands_query)

        category_query = MultiMatch(query=data, fields=['name','slug'], fuzziness='AUTO')
        category_output = CategoryDocument.search().query(category_query)

        return variant_output, product_output.to_queryset(), category_output.to_queryset(), brands_output.to_queryset()
      

    def post(self, request):
        data = request.data
        context = {}
        variant_output, product_output, category_output, brand_output = self.search(data['input'])

        print(variant_output)

        if variant_output.count() > 0:

            context['variants'] = render_to_string(
                'base/header/search/search__variant.html', {
                    'variants' : VariantProductSerializer(variant_output, many=True).data
                }
            )


        if product_output.count() > 0:
            product_output = product_output.exclude(variant__in=variant_output)
            context['products'] = render_to_string(
                'base/header/search/search__products.html', {
                    'products' : ProductSerializer(product_output, many=True).data
                }
            )


        if brand_output.count() > 0:
            context['brands'] = render_to_string(
                'base/header/search/search__brands.html', {
                    'brands' : BrandLiteSerializer(brand_output, many=True).data
                }
            )
        

        if category_output.count() > 0:
            context['categories'] = render_to_string(
                'base/header/search/search__categories.html', {
                    'categories' : CategorySerializer(category_output, many=True).data
                }
            )
    
        return Response(context)