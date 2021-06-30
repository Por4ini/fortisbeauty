from django.shortcuts import render
from apps.shop.models import Product, Variant
from apps.shop.serializers import ProductSerializer
from apps.main.models import Slogan, OurAdvantages
from apps.banners.models import Banner


def home(request):
    args = {
        'banners' : Banner.objects.all(),
        'products' : ProductSerializer(
            Product.objects.all().prefetch_related('variant','variant__images')[:40], many=True
        ).data,
        'slogan' :Slogan.objects.first(),
        'our_advantages' : OurAdvantages.objects.all(),

    }
    return render(request, 'shop/home/home.html', args)