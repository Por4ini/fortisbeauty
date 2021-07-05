from django.apps import apps
from celery import shared_task



@shared_task
def load_products_worker(id):
    LoadProductsFromTable = apps.get_model('productloader', 'LoadProductsFromTable')
    obj = LoadProductsFromTable.objects.get(id=id)
    obj.run_worker()



@shared_task
def load_products_images_worker(id):
    LoadProductsImages = apps.get_model('productloader', 'LoadProductsImages')
    obj = LoadProductsImages.objects.get(id=id)
    obj.run_worker()

