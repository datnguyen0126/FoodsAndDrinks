from rest_framework import serializers
from django.conf import settings
from .models.CategoryModel import Category
from .models.FoodModel import Food
from .models.ImagesMopdel import Images
from .services.FoodServices import FoodService


class ImagesSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return settings.DJANGO_HOST + obj.image_url.url

    class Meta:
        model = Images
        fields = ['id', 'image_url']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model: Category
        fields: ['id', 'name', 'parent_id']


class FoodSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'category_id', 'price', 'discount', 'description', 'avg_rating', 'images']


class PostOrPutFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'category_id', 'price', 'discount', 'description']

    def save_file(self, food):
        for file in self.files:
            Images.objects.create(image_url=file, food_id=food)

    def save(self):
        return FoodService.save_food(self.validated_data)

    def update(self):
        id = self.data.get('id')
        return FoodService.update_food(id, self.validated_data)
