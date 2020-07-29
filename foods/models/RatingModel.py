from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Rating(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    food_id = models.ForeignKey('foods.Food', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
