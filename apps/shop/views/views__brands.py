from apps.shop.views.views__pages import contacts
from django.shortcuts import render
from django.db.models import Prefetch, Max
from django.template.loader import render_to_string
from django.views.generic import View
from django.http import JsonResponse
from apps.shop.models import Product, Variant, Brand, Categories
from apps.shop.serializers import BrandLiteSerializer, ProductSerializer, CategoryBrandSerializer
import json 

from apps.shop.serializers import BrandSerializer, BrandDetailSerializer


def brands(request):
    return render(request, 'shop/brands/brands.html', {
        'brands' : BrandLiteSerializer(Brand.objects.all(), many=True).data
    })



class BrandsCatalogue(View):
    urlpattern = 'shop:brands'
    selected = []
    brand = None
    brands = None
    category = None
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
    price__gte = 0
    price__lte = 0
    min_price = 0
    max_price = 0

    context = {
        'params' : {},
    }
    attrvalues = []
    attrkeys = []

    # Import functions
 
    from .catalogue.set_brands import set_brands
    from .catalogue.set_attrs import get_attrs, get_selected_attrs, filter_products_attrs
    from .catalogue.set_pagination import set_pagination
    from .catalogue.set_price_range import set_price_range, get_selected_price_extremums


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
        else:
            self.products = self.products.order_by('-variant__stock')
        
    
    def get_context(self, request):
        context = {
            
            'total_products' : self.total,
            'categories' : self.categories,
            'selected_category' : self.category.first() if self.category else None,
            'brands' : BrandSerializer(
                self.brands, 
                context={'kwargs': self.context['kwargs']},
                many=True
            ).data,
            'selected_brand' : BrandDetailSerializer(self.brand).data,
            'pagination' : self.pagination,
            'price_url' : self.price_url,
            'price__gte' : self.price__gte,
            'price__lte' : self.price__lte,
            'min_price' : self.min_price,
            'max_price' : self.max_price,
        }
        context['products'] = ProductSerializer(
            self.products, many=True, context={'is_whoosaler': request.user.is_whoosaler if request.user.is_authenticated else None}
        ).data
        categories =  Categories.objects.filter(product__brand=self.brand).distinct()
        context['types'] = CategoryBrandSerializer(
            categories,context={'brand': self.brand}, many=True
        ).data 
        return context


    def set_context(self):
        # Filter products by category
        category_slug = self.context['kwargs'].get('category')
        if category_slug:
            self.category = Categories.objects.filter(slug=category_slug)
            self.products = Product.objects.filter(category__in=self.category).distinct()
        else:
            self.products = Product.objects.all()
        self.base_products = self.products
        self.variants = Variant.objects.filter(parent__in=self.products)
        self.set_brands()
        self.set_price_range()
        self.get_sorted()
        self.total = self.products.count()
        self.products = self.products.prefetch_related(
            Prefetch('variant', queryset=self.variants)
        ).distinct()
        self.set_pagination()

    

    

    def get(self, request, *args, **kwargs):
        self.context = {
            **self.context,
            "kwargs" : {k : v for k, v in kwargs.items() if v} 
        }
        self.set_context()
        return render(request, 'shop/brands/brands__catalogue.html', self.get_context(request))


    def post(self, request, *args, **kwargs):
        self.context = {
            **self.context,
            "kwargs" : {k : v for k, v in kwargs.items() if v}, 
            "request" : request
        }
        self.set_context()
        context = self.get_context()
        return JsonResponse({
            'products' :   render_to_string('shop/catalogue/catalogue__product__list.html', context), 
            'attributes' : render_to_string('shop/brands/brands__filters.html', context),
            'pagination' : self.pagination,
        })