from django.urls import reverse
from apps.shop.models import Variant
from django.db.models import Prefetch



def get_selected_price_extremums(self, kwargs):
    gte, lte = self.min_price, self.max_price
    if 'price' in kwargs.keys():
        price_range = kwargs['price'].split(',')
        if len(price_range) == 2:
            gte, lte = price_range[0], price_range[1]
    self.price__gte = gte
    self.price__lte = lte
    return gte, lte


def set_price_range(self):
    kwargs = self.context['kwargs']
    context = {**kwargs}
    if 'page' in context:
        del context['page']
        
    self.price_url = reverse(self.urlpattern, kwargs={**context, 'price' : 'min_price,max_price'})
    
    # Get lowetst and highest price products
    self.min_price = self.variants.order_by('price').values_list('price', flat=True).first()
    self.max_price = self.variants.order_by('-price').values_list('price', flat=True).first()

    gte, lte = self.get_selected_price_extremums(kwargs)
    
    if gte and lte:
        context = {**self.context.get("kwargs")}
        if 'price' in context.keys():
            del context['price']
            self.selected.append({
                'name' : f'{str(gte)} грн. - {str(lte)} грн.',
                'url' : reverse('shop:catalogue', kwargs=context)
            })
        self.products = self.products.filter(
            variant__price__gte = gte,
            variant__price__lte = lte,
        )
        self.variants = self.variants.filter(
            price__gte = gte, 
            price__lte = lte
        ).distinct()
        

        