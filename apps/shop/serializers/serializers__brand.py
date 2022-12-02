from rest_framework import serializers
from apps.shop.models import Brand, BrandSeries
from django.urls import reverse



class BrandLiteSerializer(serializers.ModelSerializer):
    url =     serializers.URLField(source='get_absolute_url', read_only=True)
    image =   serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Brand
        fields = ['id','name','slug','url','image']

    def get_image(self, obj):
        if 's' in obj.image_thmb.keys():
            return obj.image_thmb['s']['path']
        return '/static/img/no_image.jpg'



class BrandDetailSerializer(serializers.ModelSerializer):
    url =     serializers.URLField(source='get_absolute_url', read_only=True)
    image =   serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Brand
        fields = ['id','name','slug','url','image','description']

    def get_image(self, obj):
        if 's' in obj.image_thmb.keys():
            return obj.image_thmb['s']['path']
        return '/static/img/no_image.jpg'

    
   

class BrandSerializer(serializers.ModelSerializer):
    count =   serializers.CharField(read_only=True)
    url =     serializers.SerializerMethodField(read_only=True)
    selected = serializers.BooleanField(read_only=True)
    image =   serializers.SerializerMethodField(read_only=True)
  

    class Meta:
        model = Brand
        fields = ['id','name','slug','count','url','selected','image']

    def get_url(self, obj):
        brands = []
        slug = obj.slug.lower()
        context = {**self.context.get("kwargs")}
        if 'page' in context:
            del context['page']
        
        if 'brand' in context:
            brands = context['brand'].split(',')
            if slug not in brands:
                brands.append(slug)
            else:
                brands.remove(slug)

            if len(brands) == 0:
                del context['brand']
            else:
                brands.sort()
                context['brand'] = ','.join(brands)
        else:
            context['brand'] = slug

       

       
        return reverse('shop:catalogue', kwargs=context) 

  

    def get_image(self, obj):
        if 's' in obj.image_thmb.keys():
            return obj.image_thmb['s']['path']
        return '/static/img/no_image.jpg'



class BrandSeriesSerializer(serializers.ModelSerializer):
    count = serializers.CharField(read_only=True)
    url =   serializers.SerializerMethodField(read_only=True)
    selected = serializers.BooleanField(read_only=True)

    class Meta:
        model = BrandSeries
        fields = ['id','name','slug','count','url','selected']

    def get_url(self, item):
        return reverse('shop:catalogue', kwargs={**self.context.get("kwargs"), 'series' : item.slug.lower()}) 