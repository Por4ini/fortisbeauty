from rest_framework import serializers
from apps.shop.models import Brand, Categories, Product, Unit, Variant, VariantImages
from apps.shop.serializers.serializers__brand import BrandLiteSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Categories
        fields = [
            'name', 'url'
        ]


class ProductrPageVariantImagesSerializer(serializers.ModelSerializer):
    l = serializers.CharField(source="image_thmb.l.path", allow_blank=True, read_only=True)
    s = serializers.CharField(source="image_thmb.s.path", allow_blank=True, read_only=True)
    xs = serializers.CharField(source="image_thmb.xs.path", allow_blank=True, read_only=True)
    h = serializers.CharField(source="image_thmb.l.h", allow_blank=True, read_only=True)
    w = serializers.CharField(source="image_thmb.l.w", allow_blank=True, read_only=True)
    color = serializers.CharField(source="image_thmb.color", allow_blank=True, read_only=True)
    

    class Meta:
        model = VariantImages
        fields = [
            'l','s','xs','color','h','w'
        ]


class ProductPageVariantsSerializer(serializers.ModelSerializer):
    images = ProductrPageVariantImagesSerializer(many=True, read_only=True)
    url =    serializers.CharField(source="get_absolute_url", read_only=True)
    whoosale_price = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = [
            'id','value','code','price','discount_price','whoosale_price','discount_whoosale_price','images', 'url', 'stock'
        ]

    def whoosale_price(self, obj):
        if self.context.get('is_whoosaler'):
            return obj.whoosale_price
        return None
    
    
    

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=Unit
        fields=['unit']


class ProductPageSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    brand =    BrandLiteSerializer(read_only=True)
    unit =     UnitSerializer(read_only=True)
    variant =  ProductPageVariantsSerializer(many=True, read_only=True)
    serie =    serializers.CharField(source='serie.name')

    class Meta:
        model  = Product
        fields = [
            'id','category','brand','name','slug','unit','human','serie','unit','variant',
            'description','prescription','application','composition'
        ]