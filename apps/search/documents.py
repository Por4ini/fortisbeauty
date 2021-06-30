from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from apps.shop.models import Product, Categories, Brand


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'product'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Product # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'slug',
            'human',
            'prescription',
            'application',
            'composition',
            'description_text',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000


@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'categories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Categories # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name', 'slug'
        ]


@registry.register_document
class BrandDocument(Document):
    class Index:
        name = 'brands'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Brand # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name', 'slug'
        ]