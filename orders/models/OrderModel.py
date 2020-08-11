from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    contact_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default=1)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

