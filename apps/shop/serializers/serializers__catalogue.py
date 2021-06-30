from rest_framework import serializers
from apps.shop.models import Product, Variant, VariantImages


class VariantimagesImagesSerializer(serializers.ModelSerializer):
    s =     serializers.CharField(source="image_thmb.s.path",  allow_blank=True, read_only=True)
    xs =    serializers.CharField(source="image_thmb.xs.path", allow_blank=True, read_only=True)
    color = serializers.CharField(source="image_thmb.color",   allow_blank=True, read_only=True)


    class Meta:
        model = VariantImages
        fields = [
            's','xs','color'
        ]


class VariantSerializer(serializers.ModelSerializer):
    images = VariantimagesImagesSerializer(many=True, read_only=True)
    url =    serializers.CharField(source="get_absolute_url", read_only=True)
    whoosale_price = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = [
            'id',
            'price',
            'discount_price',
            'whoosale_price',
            'discount_whoosale_price',
            'value',
            'images',
            'url'
        ]

    def get_whoosale_price(self, obj):
        if self.context.get('is_whoosaler'):
            return obj.whoosale_price
        return None


class ProductSerializer(serializers.ModelSerializer):
    variant = VariantSerializer(many=True, read_only=True)
    brand =   serializers.CharField(source="brand.name", read_only=True)
    url =     serializers.CharField(source="get_absolute_url", read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'human',
            'name',
            'slug',
            'brand',
            'unit',
            'variant',
            'url'
        ]

    def get_variant(self, obj):
        return VariantSerializer(
            obj.variant.all(), many=True, context=self.context, read_only=True
        ).data



class VariantProductSerializer(serializers.ModelSerializer):
    human =  serializers.CharField(source="parent.human", read_only=True)
    name =   serializers.CharField(source="parent.name", read_only=True)
    brand =  serializers.CharField(source="parent.brand.name", read_only=True)
    unit =   serializers.CharField(source="parent.unit", read_only=True)
    images = VariantimagesImagesSerializer(many=True, read_only=True)
    url =    serializers.CharField(source="get_absolute_url", read_only=True)
    whoosale_price = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = [
            'id',
            'code',
            'price',
            'discount_price',
            'whoosale_price',
            'discount_whoosale_price',
            'value',
            'images',
            'url',
            'human',
            'name',
            'brand',
            'unit',
        ]
  
    def get_whoosale_price(self, obj):
        if self.context.get('is_whoosaler'):
            return obj.whoosale_price
        return None