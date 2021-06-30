from django.urls import path
from . import views


app_name = 'search'


urlpatterns = [
   path('', views.SearchProduct.as_view(), name='search')
]
