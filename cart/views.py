from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foods.models.FoodModel import Food
from foods.serializers import FoodSerializer
from .cart import Cart

from django.http import JsonResponse
from requests.exceptions import HTTPError
from django.core.serializers.json import DjangoJSONEncoder
import json

class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        cart = Cart(request)
        for item in cart(str(request.user.id)):
            if not item:
                return Response({}, status=status.HTTP_200_OK)
            item['food'] = FoodSerializer(item['food']).data
        user_cart = cart.cart.get(str(request.user.id), {})
        food = get_object_or_404(Food, pk=1)
        data = json.dumps(user_cart, cls=DjangoJSONEncoder)
        return Response(json.loads(data), status=status.HTTP_200_OK)

    def create(self, request):
        cart = Cart(request)
        food = get_object_or_404(Food, pk=request.data['food_id'])
        cart.add(food=food, quantity=int(request.data['quantity']), override_quantity=False, user=request.user)
        data = { 'message': 'Cart added' }
        return Response(data, status=status.HTTP_201_CREATED)
        
    def update(self, request, pk=None):
        cart = Cart(request)
        food = get_object_or_404(Food, pk=pk)
        cart.add(food=food, quantity=int(request.data['quantity']), override_quantity=True, user=request.user)
        data = { 'message': 'cart updated' }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        cart = Cart(request)
        food = get_object_or_404(Food, pk=pk)
        cart.remove(food=food, user=request.user)        
        return Response(FoodSerializer(food).data, status=status.HTTP_200_OK)

