from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import serializers
from django.shortcuts import render

from cart.cart import Cart
from .models.OrderItemModel import OrderItem
from .models.OrderModel import Order
from .tasks import order_created
from django.http import JsonResponse
from requests.exceptions import HTTPError
from django.db import transaction
from django.db import IntegrityError


User = get_user_model()

class OrderViewSet(viewsets.GenericViewSet):
    permission_class = [IsAuthenticated]
    serializer_class = serializers.OrderSerializer
    
    def create(self, request):
        cart = Cart(request)
        order_serializer = serializers.OrderSerializer(data=request.data, context={'request': request})
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()
        try:
            with transaction.atomic():
                for item in cart(str(request.user.id)):
                    OrderItem.objects.create(order=order, food=item['food'], price=item['price'], quantity=item['quantity'])
        except IntegrityError:
            data = {'message': 'Error orcur while adding order item, please check your cart again'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        order_created.delay(order.id)
        cart.clear(request.user)
        data = {'message': 'Order created successfully'}
        return Response(data=data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = serializers.OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
