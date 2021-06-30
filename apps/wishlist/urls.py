from django.urls import path
from apps.wishlist import views


app_name = 'wishlist'


urlpatterns = [
    path('',                 views.WishlistDataView.as_view(),              name='wishlist'),
    path('add/<int:id>/',    views.WishlistView.as_view({'get': 'put'}),    name='wishlist-add'),
    path('delete/<int:id>/', views.WishlistView.as_view({'get': 'delete'}), name='wishlist-delete'),
]
