from django.shortcuts import render
from django.shortcuts import redirect
from apps.shop.models import Product, Variant
from apps.shop.serializers import ProductSerializer
from apps.main.models import Slogan, OurAdvantages
from apps.banners.models import Banner
from apps.core.functions import send_telegeram


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
    
    
def appear__product(request):
    data = request.POST
    
    msg = [
        "Повідомити, коли з'явиться. \n"
        "Email: " + data["email"],
        'Товар' + request.META.get('HTTP_REFERER'),
        
    ]
    send_telegeram(msg)
  
    prev_url = request.META.get('HTTP_REFERER')
    if prev_url:
        return redirect(prev_url)
    return redirect('/')
    
    
def product__available(request, user):
    pass
