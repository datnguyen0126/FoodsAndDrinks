from decimal import Decimal
from django.conf import settings
from foods.models.FoodModel import Food


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, food, user, quantity=1, override_quantity=False):
        user_id = str(user.id)
        if user_id not in self.cart:
            self.cart[user_id] = {}
        food_id = str(food.id)
        if food_id not in self.cart[user_id]:
            self.cart[user_id][food_id] = {'quantity': 0, 'price': str(food.price)}
        if override_quantity:
            self.cart[user_id][food_id]['quantity'] = quantity
        else:
            self.cart[user_id][food_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, food, user):
        user_id = str(user.id)
        food_id = str(food.id)
        if user_id in self.cart:
            if food_id in self.cart[user_id]:
                del self.cart[user_id][food_id]
            if len(self.cart[user_id]) == 0:
                del self.cart[user_id]
        self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

