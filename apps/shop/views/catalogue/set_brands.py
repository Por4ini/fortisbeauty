from django.db.models import Count, Case, When, Value, BooleanField
from apps.shop.models import Brand, BrandCategoryText
from apps.shop.serializers import BrandSerializer, BrandDetailSerializer
import json




def set_brands(self):
    kwargs =   self.context['kwargs']
  
    # Get sku list of selected brands
    brands_skus = []
    if 'brand' in kwargs.keys():
        brands_skus = kwargs.get('brand').lower().split(',')


    # Filter products by selected brands
    if len(brands_skus):
        self.products = self.products.filter(brand__slug__in=brands_skus)
        self.variants = self.variants.filter(parent__in=self.products)

    # Filter brands, count products, and annonate selected bools
    self.brands = Brand.objects.filter(product__in=self.base_products).annotate(
        count=Count('product'),
        selected=Case(
            When(slug__in=brands_skus, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    ).order_by('-selected','name').distinct()


    # Create data for selected buttons
    for brand in self.brands.filter(selected=True):
        brand_serialized = BrandSerializer(brand, context={'kwargs': self.context['kwargs']}).data
        self.selected.append({
            'name' : brand_serialized['name'],
            'url' : brand_serialized['url']
        })


    # Get brend deatil info for its description presentation in catalogie
    if len(brands_skus) == 1:
        try:    category=self.category.first()
        except: category=None
        
        self.brand = Brand.objects.filter(slug = brands_skus[0]).first()
        brand_text = BrandCategoryText.objects.filter(category=category, brand=self.brand).first()
 
        if brand_text:
            self.text = brand_text.description
        
        
  
    



