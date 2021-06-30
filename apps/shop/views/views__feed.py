from django.http import request
from django.shortcuts import render
from django.views import View
from apps.shop.models import Product
from apps.shop.serializers import ProductSerializer


class FeedView(View):
    def get(self, request):
        return render(request, 'feed/feed.xml', {
            'products' : Product.objects.filter(variant__images__isnull=False)
        }, content_type="application/xhtml+xml")