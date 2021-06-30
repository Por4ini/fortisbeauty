from django.shortcuts import render
from rest_framework import viewsets
from apps.blog.models import BlogPost
from apps.blog.serializers import BlogPostSerializer




class BlogViewSet(viewsets.ViewSet):
    model = BlogPost
    serializer_class = BlogPostSerializer

    def list(self, request):
        posts = self.model.objects.all()
        posts_serialzied = self.serializer_class(posts, many=True).data
        return render(request, 'blog/blog.html', {'posts': posts_serialzied})

    def get(self, request, slug):
        post = self.model.objects.get(slug=slug)
        post_serialzied = self.serializer_class(post).data
        return render(request, 'blog/post.html', {'post': post_serialzied})