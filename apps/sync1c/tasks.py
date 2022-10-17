from workers import task
from .models import RequestData1C



def update_products(id):
    data = RequestData1C.objects.get(id=id)
    data.run_workers()
    