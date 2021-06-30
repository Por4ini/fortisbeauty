from django.db.models import Q, Count
from apps.shop.models import Categories



def set_category(self):
    category_slug = self.context['kwargs'].get('category')
  
    if category_slug:
        categories = [c for c in category_slug.split('/') if len(c) > 0]
        category_slug = categories[-1]
        parent_category_slug = None
        if len(categories) > 1:
            parent_category_slug = categories[-2]
        self.category = Categories.objects.filter(
            slug=category_slug,
            parent__slug=parent_category_slug, 
        ).first()
        
        if self.category:
            self.ancestors = self.category.get_ancestors()
            self.products = self.products.filter(
                category__in=self.category.get_descendants(include_self=True)
            )
            self.variants = self.variants.filter(parent__in=self.products)
            self.base_products = self.products
            
            if self.category.description:
                self.text = self.category.description
            
    self.categories = Categories.objects.filter(parent=self.category).annotate(
        product__count = Count('children_category__relation__product', distinct=True)
    ).order_by('name')

  

    if self.context['kwargs'].get('discount') == 'yes':
        self.categories = self.categories.filter(
            Q(product__variant__discount_price__gte=1) |
            Q(children__product__variant__discount_price__gte=1) |
            Q(children__children__product__variant__discount_price__gte=1) |
            Q(children__children__children__product__variant__discount_price__gte=1)
        ).distinct()
  