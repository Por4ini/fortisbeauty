from django.urls import reverse
from rest_framework import serializers
from apps.shop.models import Categories

        
class CategorySerializer(serializers.ModelSerializer):
    url =      serializers.SerializerMethodField()
    image =    serializers.CharField(source='get_image', read_only=True)
    product__count = serializers.IntegerField(default=0)
    
    class Meta:
        model = Categories
        fields = ['name','human','id','slug','image','url','product__count']

    def get_url(self, obj):
        if self.context.get('discount'):
            category_name = '/'.join([category.slug for category in obj.get_ancestors(ascending=False, include_self=True)]) +'/'
            return reverse('shop:catalogue', kwargs={'category' : category_name, 'discount': 'yes'})
        return obj.get_absolute_url()



class CategoryBrandSerializer(serializers.ModelSerializer):
    url =  serializers.SerializerMethodField()
    
    class Meta:
        model = Categories
        fields = ['id','name','slug','url']

    def get_url(self, obj):
        brand = self.context.get('brand')
        return reverse('shop:brands', kwargs={'brand': brand.slug.lower(), 'category' : obj.slug})




class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    image =    serializers.CharField(source='get_image', read_only=True)
    url =      serializers.CharField(source="get_absolute_url")

    class Meta:
        model = Categories
        fields = ('id', 'name', 'human', 'url', 'children', 'image')
        

    def get_children(self, obj):
        children = obj.get_children()
        if children.count() > 0:
            return CategoryTreeSerializer(children, many=True).data
        return None

