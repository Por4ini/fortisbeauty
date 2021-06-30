from django.apps import apps
from workers import task



@task()
def load_products_worker(id):
    LoadProductsFromTable = apps.get_model('productloader', 'LoadProductsFromTable')
    obj = LoadProductsFromTable.objects.get(id=id)
    obj.run_worker()



@task()
def load_products_images_worker(id):
    LoadProductsImages = apps.get_model('productloader', 'LoadProductsImages')
    obj = LoadProductsImages.objects.get(id=id)
    obj.run_worker()

