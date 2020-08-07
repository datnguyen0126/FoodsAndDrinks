from django.db import models
from users.models import User


class Comment(models.Model):
    food_id = models.ForeignKey('foods.Food', related_name="food", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']
