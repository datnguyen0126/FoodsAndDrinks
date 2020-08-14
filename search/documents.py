from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from foods.models.FoodModel import Food


@registry.register_document
class FoodDocument(Document):
    class Index:
        name = 'foods'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Food
        fields = ['id', 'name', 'price', 'discount', 'description']
