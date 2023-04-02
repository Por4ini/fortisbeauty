from rest_framework import serializers
from apps.shop.models import Variant, VariantImages




class CartVartinatSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    name = serializers.CharField(source="parent.name", read_only=True)
    unit = serializers.CharField(source="parent.unit.name", read_only=True)
    price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = ['id','name','unit','price','discount_price','image','url','stock' ]


    def get_image(self, obj):
        try:
            return obj.images.first().image_thmb['s']['path']
        except:
            return '-'
 

    def get_price(self, obj):
        whoosale = self.context['whoosale']
        if whoosale:
            return  obj.whoosale_price
        return obj.price

    def get_discount_price(self, obj):
        whoosale = self.context['whoosale']
        if whoosale:
            return obj.discount_whoosale_price
        return obj.discount_price

