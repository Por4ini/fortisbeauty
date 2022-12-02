from django.urls import reverse
from django import template
from apps.shop.models.models__product import Variant

register = template.Library()


@register.filter
def variant_url(variant_id):
    if not variant_id:
        return '/'

    variant = Variant.objects.get(id=variant_id)
    return reverse('shop:variant', kwargs={
        'category': '/'.join([
            category.slug for category in variant.parent.category.get_ancestors(include_self=True)
        ]),
        'brand': variant.parent.brand.slug,
        'product_slug': variant.parent.slug,
        'product_id': variant.parent.pk,
        'variant_id': variant.pk
    })
