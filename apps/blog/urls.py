from django.urls import path
from apps.blog import views


app_name = 'blog'


urlpatterns = [
   path('',        views.BlogViewSet.as_view({'get': 'list'}), name="list"),
   path('<slug>/', views.BlogViewSet.as_view({'get': 'get'}),  name="post"),
]
