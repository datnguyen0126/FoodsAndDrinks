from rest_framework import serializers
from .models.OrderModel import Order
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Order
        fields = ['address', 'city', 'contact_number', 'user']

