from django.db.models import Q, Prefetch, Case, When, Count, Value, F,  ExpressionWrapper, Sum
from django.db.models.functions import Round
from django.db.models import  OuterRef, Subquery, IntegerField, BooleanField, CharField, TextField
from apps.filters.models import Attribute, AttributeValue, CategoryAttribute, CategoryAttributeValue, ProductAttribute
from apps.shop.models import Product, Variant, Categories
from apps.shop.serializers import AttributeSerializer, AttributeValueSerializer, ProductSerializer
import json, time, math




def get_attrs(self, category, params_attr=None, params=None, products_excluded=None, products_filtered=None):
    all_categories = Categories.objects.all()
    excluded__pks = products_excluded.values_list('pk', flat=True)
    attr_values = AttributeValue.objects.distinct().filter(
        category_values__parent__parent__in = category.get_family() if category else all_categories,
        product_attrs__parent__category__in = category.get_descendants(include_self=True) if category else all_categories
    )
    attr_values =  attr_values.annotate(
        count=Count(
            'product_attrs__parent',  
            filter=Q(
                product_attrs__parent__in=products_filtered,
            ), 
            output_field=IntegerField(), 
            distinct=True
        ),
    )
    if params_attr:
        attr_values = attr_values.annotate(
            selected=Case(When(params_attr, then=Value(True)), default=Value(False), output_field=BooleanField(),),
        )
    attrs = Attribute.objects.distinct().filter(values__in=attr_values).prefetch_related(
        Prefetch('values', attr_values)
    )
    return attrs


# GET SELECTED ATTRIBUTES FROM URL PARAMS
def get_selected_attrs(self, atributes=None):
    if atributes:
        params_price = {}
        params_attr, params  = Q(), {}
        for attr in atributes.split('/'):
            try: key, value = attr.split('=')
            except: continue
            value = value.split(',')
            if key == 'price':
                params_price['price_ua__gte'] = int(value[0])
                params_price['price_ua__lte'] = int(value[1])
            else:
                print(key, value)
                params_attr |= Q(parent__slug=key, slug__in=value)
                params[key] = value
        return params_attr, params_price, params
    else:
        return None, {}, {}


# FILTER PRODUCTS BU ATRIBUTES
def filter_products_attrs(self, products, params):
    values = []
    keys = []

    if params:
        for key, value in params.items():
            if key in ['price_ua__gte', 'price_ua__lte']:
                products = products.filter(**{key : value})
            else:
                products = products.filter(
                    product_attrs__attribute__attribute__slug = key, 
                    product_attrs__value__slug__in = value,
                )
                for val in value:
                    values.append(key + '__' + val) 
                keys.append(key) 
        
        products = products.distinct()
        self.attrvalues = values
        self.attrkeys = keys
    return products