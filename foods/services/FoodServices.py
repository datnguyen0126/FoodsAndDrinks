from ..models.FoodModel import Food
from ..models.ImagesMopdel import Images
from django.db import transaction


class FoodService:

    @classmethod
    def save_img(cls, images, food):
        for file in images:
            Images.objects.create(image_url=file, food_id=food)

    @classmethod
    def save_food(cls, data):

        with transaction.atomic():
            food = Food.objects.create(
                name=data.get('name'),
                category_id=data.get('category_id'),
                price=data.get('price'),
                discount=data.get('discount'),
                description=data.get('description'),
            )
            cls.save_img(data.files, food)
        return food

    @classmethod
    def update_food(cls, id_food, data):
        try:
            food = Food.objects.get(id=id_food)
            food.name = data.get('name')
            food.category_id = data.get('category_id')
            food.price = data.get('price')
            food.discount = data.get('discount')
            food.description = data.get('description')
            with transaction.atomic():
                food.save()
                cls.save_img(data.files, food)
            return food
        except Food.DoesNotExist:
            return None
