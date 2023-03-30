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
        # розділяємо вхідні дані на слова та зберігаємо їх в список
        search_words = data.split()

        # створюємо порожні запити для кожної моделі
        variant_query = Q()
        product_query = Q()
        category_query = Q()
        brand_query = Q()

        # для кожного слова в списку виконуємо пошук за відповідною колонкою відповідної моделі та додаємо його до запиту
        for word in search_words:
            variant_query |= Q(code__icontains=word) | Q(parent__name__icontains=word) | Q(
                parent__human__icontains=word)
            product_query |= Q(name__icontains=word) | Q(human__icontains=word) | Q(brand__name__icontains=word)
            brand_query |= Q(name__icontains=word)
            category_query |= Q(human__icontains=word) | Q(name__icontains=word) | Q(parent__name__icontains=word) | Q(
                parent__human__icontains=word)

        variant_output = Variant.objects.filter(variant_query)
        product_output = Product.objects.filter(product_query)
        brand_output = Brand.objects.filter(brand_query)
        category_output = Categories.objects.filter(category_query)

        return variant_output, product_output, category_output, brand_output

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

