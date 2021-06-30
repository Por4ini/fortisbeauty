from rest_framework import serializers
from apps.filters.models import Attribute, AttributeValue


class AttributeValueSerializer(serializers.ModelSerializer):
    products =          serializers.IntegerField(read_only=True)
    products_filtered = serializers.IntegerField(read_only=True)
    selected =          serializers.BooleanField(read_only=True)
    count =             serializers.IntegerField(read_only=True)
    more =              serializers.IntegerField(read_only=True)
 
    class Meta:
        model = AttributeValue
        fields = [
            'pk','name','slug','products','products_filtered','selected','count', 'more'
        ]

        
class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)
    
    class Meta:
        model = Attribute
        fields = ['pk','name','slug','values']