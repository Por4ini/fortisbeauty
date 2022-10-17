from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.sync1c.models import RequestData1C, RequestData1CSettings
from braces.views import CsrfExemptMixin
from .tasks import update_products
from rest_framework import serializers
from apps.shop.models import Variant



class limitIp(BasePermission):
    def has_permission(self, request, view):
        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip

        if RequestData1CSettings.objects.filter(ip=get_client_ip(request)).first():
            return True
        return False




class updateFrom1C(CsrfExemptMixin, APIView):
    model = RequestData1C
    authentication_classes = []
    permission_classes = [limitIp]
    db_model = Variant
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        if request.data.get('products'):
            data = RequestData1C(data = request.data['products'])
            
            data.save()
            update_products(data.id)
            return Response({'sucess': True})
            
        else:
            return Response({'sucess': False})
    
    

    