from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from apps.wishlist.models import Wishlist
from apps.wishlist.serializers import WishlistSerializer
from apps.shop.models import Variant




def get_wishlist_data(request):
    user = request.user
    is_whoosaler = user.is_whoosaler if user.is_authenticated else None
    if user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
    else:
        wishlist = Wishlist.objects.none()
    wishlist_serialized = WishlistSerializer(wishlist, context={'is_whoosaler': is_whoosaler},  many=True).data
    return {
        'html' : render_to_string('wishlist/wishlist__list.html', {
            'wishlist' : wishlist_serialized, 'request' : request
        }),
        'total' : wishlist.count()
    }




class WishlistDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'wishlist' : get_wishlist_data(request)})




class WishlistView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        user = request.user
        variant = Variant.objects.get(id=id)
        try:
            wish = Wishlist.objects.get(user=user, variant=variant)
        except:
            wish = Wishlist(user=user, variant=variant)
        wish.save()
        return Response({'wishlist' : get_wishlist_data(request)})
    

    def delete(self, request, id):
        user = request.user
        variant = Variant.objects.get(id=id)
        try:
            wish = Wishlist.objects.get(user=request.user, variant=variant)
            wish.delete()
        except:
            pass
        return Response({'wishlist' : get_wishlist_data(request)})