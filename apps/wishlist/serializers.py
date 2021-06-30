from rest_framework import serializers
from apps.shop.models import Variant
from apps.wishlist.models import Wishlist


class WishlistVariantSerializer(serializers.ModelSerializer):
    name =     serializers.CharField(source="parent.name",  read_only=True)
    human =    serializers.CharField(source="parent.human", read_only=True)
    slug =     serializers.CharField(source="parent.slug",  read_only=True)
    unit  =    serializers.CharField(source="parent.unit.name", read_only=True)
    brand =    serializers.CharField(source="parent.brand.name", read_only=True)
    url =      serializers.CharField(source="get_absolute_url", read_only=True)
    image =    serializers.SerializerMethodField()
    price =    serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = [
            'id','name','human','slug','brand','url','unit','image','price'
        ]

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return image.image_thmb['s']['path']
        return None

    def get_price(self, obj):
        if self.context.get('is_whoosaler'):
            return obj.whoosale_price
        return obj.price


class WishlistSerializer(serializers.ModelSerializer):
    variant = WishlistVariantSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            'pk','variant'
        ]

