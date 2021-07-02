from apps.core.functions import *
from apps.shop.cart import Cart
from apps.shop.models import Variant
from apps.shop.models import Categories
from apps.shop.serializers import CategoryTreeSerializer
from project.settings import WISHLIST_SESSION_ID
from django.core.cache import cache
import json



def categories_tree(request=None):
    tree = cache.get('tree_categories')
 
    if tree is None:
        categories_qs = Categories.objects.filter(level=0).prefetch_related('children')
        tree = CategoryTreeSerializer(categories_qs, many=True).data
        cache.set('tree_categories', tree, 60*60*24*365)
    return {'tree' : tree}
 

def cart(request):
    return {'cart': Cart(request).data }


