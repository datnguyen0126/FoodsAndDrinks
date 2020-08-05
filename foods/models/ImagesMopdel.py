from django.db import models
from .FoodModel import Food


class Images(models.Model):
    image_url = models.ImageField()
    food_id = models.ForeignKey(Food, related_name="images", on_delete=models.CASCADE)
