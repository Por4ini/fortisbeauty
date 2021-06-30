from django.apps import apps
import requests




def cahce_all_products():
    Product = apps.get_model('shop', 'Product')
    for product in Product.objects.all():
        url = product.get_absolute_url()
        requests.get('http://127.0.0.1:8000' +  url)
       

def cahce_product(id):
    Product = apps.get_model('shop', 'Product')
    product = Product.objects.get(id=id)
    url = product.get_absolute_url()
    requests.get('http://127.0.0.1:8000' +  url)


def cahce_all_categories():
    Categories = apps.get_model('shop', 'Categories')
    for category in Categories.objects.all():
        url = category.get_absolute_url()
        requests.get('http://127.0.0.1:8000' +  url)


def cahce_category(id):
    Categories = apps.get_model('shop', 'Product')
    category = Categories.objects.get(id=id)
    url = category.get_absolute_url()
    requests.get('http://127.0.0.1:8000' +  url)