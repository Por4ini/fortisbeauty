from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.decorators.vary import vary_on_headers

from django.views.generic import TemplateView
from apps.shop import views


app_name = 'shop'

comments = [
    path('product-<int:product_id>/comment_form/',                       views.ProductViewSet.as_view({'get' : 'comment_form', 'post' : 'comment_form'}), name="product_comment_form"),
    path('product-<int:product_id>-<comment_type>/comment_form/',        views.ProductViewSet.as_view({'get' : 'comment_form', 'post' : 'comment_form'}), name="product_comment_form"),
    path('comment-<int:comment_id>/reply_form/',                         views.ProductViewSet.as_view({'get' : 'reply_form',   'post' : 'reply_form'}),   name="comment_reply_form"),
    path('comment-<int:comment_id>/reply_form/parent-<int:parent_id>',   views.ProductViewSet.as_view({'get' : 'reply_form',   'post' : 'reply_form'}),   name="comment_reply_form"),
]


product = [
    path('comments/', include(comments)),
    path('serie/product-<int:product_id>', views.ProductViewSet.as_view({'get' : 'fetch_serie'}), name="fetch_serie"),
    re_path(
        r'''^catalogue/(?P<category>([/\w-]*))/'''
        r'''(?P<brand>[\w-]+)__'''
        r'''(?P<product_slug>([\w-]+))'''
        r'''_(?P<product_id>[\d+]+)/?$''',
        views.ProductViewSet.as_view({'get' : 'get', 'post' : 'post'}) , 
        name='product'
    ),
    re_path(
        r'''^catalogue/(?P<category>([/\w-]*))/'''
        r'''(?P<brand>[\w-]+)__'''
        r'''(?P<product_slug>([\w-]+))'''
        r'''_(?P<product_id>[\d+]+)'''
        r'''?(?:-(?P<variant_id>[\d+]+))?/?$''', 
        views.ProductViewSet.as_view({'get' : 'get', 'post' : 'post'}) , 
        name='variant'
    ),
    
]


catalogue = [
    path('brands/', views.brands, name="brands_all"),
    re_path(
        r'''^brands/(?P<brand>[\w-]+)?/?'''
        r'''(?:\/(?P<category>([\w-]*)))?/?'''
        r'''(?:\/page=(?P<page>[\d+]+))?/?'''
        r'''(?:\/price=(?P<price>[,\w-]+))?/?'''
        r'''(?:\/sort=(?P<sort>price_asc|price_dsc|newest|popular))?/?'''
        r'''(?:\/(?P<atributes>([\w-]+(=[,\w-]*))?(((\/[\w-]+(=[,\w-]*))?)*)))?/$''',
        views.BrandsCatalogue.as_view(), 
        name="brands"
    ),
    path('catalogue/', views.Catalogue.as_view(),  name="catalogue"),
    re_path(
        r'''^catalogue/'''
        r'''?(?:\/(?P<category>([/\w-]*)))?/'''
        r'''?(?:discount=(?P<discount>yes|no))?/'''
        r'''?(?:\/brand=(?P<brand>[,\w-]+))?/'''
        r'''?(?:\/page=(?P<page>[\d+]+))?/'''
        r'''?(?:\/price=(?P<price>[,\w-]+))?/'''
        r'''?(?:\/sort=(?P<sort>price_asc|price_dsc|newest|popular))?/'''
        r'''?(?:\/(?P<atributes>([\w-]+(=[,\w-]*))?(((\/[\w-]+(=[,\w-]*))?)*)))?/''',
        views.Catalogue.as_view(), 
        name="catalogue"
    ),

   
]


cart = [
    path('add/',    views.CartViewSet.as_view({'post' : 'add'}),    name='cart__add'),
    path('delete/', views.CartViewSet.as_view({'post' : 'delete'}), name='cart__delete'),
    path('get/',    views.CartViewSet.as_view({'get' : 'get'}),     name='cart__get'),
    path('clear/',  views.CartViewSet.as_view({'get' : 'clear'}),   name='cart__clear'),
]


templates = [
    path('buyer-info', views.TemplatesView.as_view({'get' : 'buyer_info'}), name='tpl-buyer_info')
]


urlpatterns = [
    path('',             views.home, name='home'),
    path('watchlist',    views.WatchListView.as_view({'get': 'get'}), name="watchlist"),
    path('cart/',        include(cart)),
    path('feed/',        views.FeedView.as_view(), name="feed"),
    path('templates',    include(templates)),
    path('', include(product)),
    path('', include(catalogue)),

]
