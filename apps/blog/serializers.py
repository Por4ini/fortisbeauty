from apps.core import models
from rest_framework import serializers
from apps.blog.models import BlogPost, BlogPostImages



class BlogPostImagesSerializer(serializers.ModelSerializer):
    l =     serializers.CharField(source="image_thmb.l.path",  allow_blank=True, read_only=True)
    s =     serializers.CharField(source="image_thmb.s.path",  allow_blank=True, read_only=True)
    xs =    serializers.CharField(source="image_thmb.xs.path", allow_blank=True, read_only=True)
    h =     serializers.CharField(source="image_thmb.l.h",     allow_blank=True, read_only=True)
    w =     serializers.CharField(source="image_thmb.l.w",     allow_blank=True, read_only=True)
    color = serializers.CharField(source="image_thmb.color",   allow_blank=True, read_only=True)

    class Meta:
        model = BlogPostImages
        fields = [
            'id','l','s','xs','h','w','color'
        ]


class BlogPostSerializer(serializers.ModelSerializer):
    date =    serializers.DateTimeField(format="%H:%M - %Y/%m/%d", read_only=True)
    name =    serializers.CharField(source="trans.name", read_only=True)
    text =    serializers.CharField(source="trans.text", read_only=True)
    image =   serializers.CharField(source="image_thmb.s.path", allow_blank=True, read_only=True)
    image_l = serializers.CharField(source="image_thmb.l.path",  allow_blank=True, read_only=True)
    images =  BlogPostImagesSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'date','name','slug','text','image','image_l','images'
        ]

