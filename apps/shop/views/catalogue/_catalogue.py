from django.shortcuts import render
from django.db.models import Prefetch
from django.template.loader import render_to_string
from django.views.generic import View
from django.http import JsonResponse
from apps.shop.models import Brand, Product, Variant
from apps.shop.serializers.serializers__category import CategorySerializer
from apps.shop.serializers.serializers__brand import BrandSerializer, BrandDetailSerializer
from apps.shop.serializers.serializers__catalogue import ProductSerializer 
import json 




class Catalogue(View):
    urlpattern = 'shop:catalogue'
    selected = []
    text = None
    brand = None
    brands = Brand.objects.none()
    category = None
    ancestors = []
    categories = None
    products = Product.objects.none()
    base_products = Product.objects.none()
    variants = Variant.objects.none()
    pagination = {
        'first' :    None,
        'previous' : None,
        'next' :     None,
        'middle' :   [],
        'total' :    None,
    }

    total = 0
    price__gte, price__lte = 0, 0
    min_price, max_price = 0, 0
    context = {
        'params' : {},
    }
    attrvalues = []
    attrkeys = []

    from .set_category import set_category
    from .set_brands import set_brands
    from .set_attrs import get_attrs, get_selected_attrs, filter_products_attrs
    from .set_pagination import set_pagination
    from .set_price_range import set_price_range, get_selected_price_extremums


    def get_sorted(self):
        sort = self.context['kwargs'].get('sort')
        order_by = {
            'newest' : '-update',
            'popular' : '-update',
            'price_asc' : 'variant__price',
            'price_dsc' : '-variant__price',
        }
        if sort and sort in order_by.keys():
            self.products = self.products.order_by(order_by[sort])
            if sort == 'price_asc':
                self.variants = self.variants.order_by('price')
            elif sort == 'price_dsc':
                self.variants = self.variants.order_by('-price')


    def get_context(self, request):
        context = {
            'brands' : BrandSerializer(self.brands, many=True, context={'kwargs': self.context['kwargs']}).data,
            'selected_brand' : BrandDetailSerializer(self.brand).data,
            'pagination' : self.pagination,
            'price_url' :  self.price_url,
            'price__gte' : self.price__gte,
            'price__lte' : self.price__lte,
            'min_price' :  self.min_price,
            'max_price' :  self.max_price,
            'seo_text' :   self.text,
        }
        context['products'] = ProductSerializer(
            self.products, many=True, context={'is_whoosaler': request.user.is_whoosaler if request.user.is_authenticated else None}
        ).data
        context['total_products'] = self.total
        context['category_ancestors'] = CategorySerializer(self.ancestors, many=True).data
        context['tree_categories'] = CategorySerializer(
            self.categories, 
            many=True, 
            context={
                'discount': self.context['kwargs'].get('discount')
            }).data
        context['category'] = CategorySerializer(self.category).data if self.category else None
        context['selected'] = self.selected
        return context


    def set_products(self):
       
        self.products = Product.objects.all()
        self.variants = Variant.objects.filter(parent__in=self.products)
        if 'discount' in self.context['kwargs']:
            self.products = self.products.filter(variant__discount_price__gte=1).distinct()
            self.variants = self.variants.filter(discount_price__isnull=False).distinct()
        self.base_products = self.products


    def set_context(self):
        self.selected = []
        self.set_products()
        self.set_category()
        self.set_brands()
        self.set_price_range()
        self.get_sorted()
        self.total = self.products.count()
        self.products = self.products.prefetch_related(
            Prefetch('variant', queryset=self.variants)
        ).distinct()
        self.set_pagination()
        return self


    def get(self, request, **kwargs):
        self.context = {
            **self.context,
            "kwargs" : {k : v for k, v in kwargs.items() if v} 
        }
        
        self.set_context()
        return render(request, 'shop/catalogue/catalogue.html', self.get_context(request))

    # For ajax requests
    def post(self, request, **kwargs):
        self.context = {
            **self.context,
            "kwargs" : {k : v for k, v in kwargs.items() if v}, 
            "request" : request
        }
        self.set_context()
        context = self.get_context(request)
        return JsonResponse({
            'total_products' : context['total_products'],
            'products' :   render_to_string('shop/catalogue/catalogue__product__list.html', context), 
            'attributes' : render_to_string('shop/catalogue/catalogue__filters.html', context),
            'selected' :   render_to_string('shop/catalogue/catalogue__selected.html', context), 
            'pagination' : self.pagination,
            
        })