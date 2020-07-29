from django.db import models
from .CategoryModel import Category
from .RatingModel import Rating


class FoodQuerySet(models.Manager):
    def get_object(self, pk):
        return super().get_queryset().get(id=pk)


class Food(models.Model):
    category_id = models.ForeignKey(Category, related_name="foods", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    description = models.TextField()

    objects = FoodQuerySet()

    def avg_rating(self):
        total_score = 0
        ratings = Rating.objects.filter(food_id=self)
        if len(ratings) == 0:
            return total_score
        for rating in ratings:
            total_score += rating.score
        return total_score / len(ratings)
