from django.urls import reverse
from django.core.paginator import Paginator
from django.template.loader import render_to_string


def set_pagination(self):
    qty = 24
    kwargs = self.context['kwargs']
    products = self.products

    page = kwargs.get('page') 

    
    pagination = Paginator(list(products), qty).page(page if page else 1)

    # Main vars
    current =  pagination.number
    previous = current - 1 if current > 1 else None
    total =    pagination.paginator.num_pages

    # Current page
    self.pagination['current'] = {
        "index" : current,
        "url" : reverse(self.urlpattern, kwargs={**kwargs, 'page' : current}) 
    }

    # First page
    self.pagination['first'] = {
        "index" : 1,
        "url" : reverse(self.urlpattern, kwargs={k : v for k, v in kwargs.items() if k != 'page'}) 
    }

    # Previous page
    if previous:
        self.pagination['previous'] = {
            'index' : previous,
            'url' : reverse(self.urlpattern, kwargs={**kwargs, 'page' : previous}) 
        }

    # Next page
    if pagination.has_next() and current != total:
        next_page = pagination.next_page_number()
        self.pagination['next'] = {
            'index' : next_page,
            'url' : reverse(
                self.urlpattern, kwargs={**kwargs, 'page' : next_page}
            ) 
        }

    # Last page
    self.pagination['total'] ={
            'index' : total,
            'limit' : total - 3,
            'url' : reverse(
                self.urlpattern, kwargs={**kwargs, 'page' : total}
            ) 
        } 

    # Middle pages
    self.pagination['middle'] = []
    for i in range(current - 2, current + 3):
        if i > 1 and i < total:
            self.pagination['middle'].append({
                    'index' : i,
                    'url' : reverse(self.urlpattern, kwargs={**kwargs, 'page' : i}) 
                }
            )

    self.pagination = render_to_string('shop/catalogue/catalogue__pagination.html', self.pagination)
    self.products = pagination.object_list