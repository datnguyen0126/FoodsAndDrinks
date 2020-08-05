from django.contrib import admin
from .models.CategoryModel import Category
from .models.FoodModel import Food
from .models.ImagesMopdel import Images


admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Images)
