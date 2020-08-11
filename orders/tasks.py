from celery import task
from django.core.mail import send_mail
from .models.OrderModel import Order
from django.contrib.auth import get_user_model
import environ


env = environ.Env()
User = get_user_model()

@task
def order_created(order_id):
    order = Order.objects.get(pk=order_id)
    user = User.objects.get(pk=order.user_id)
    subject = f'Order number {order.id}'
    message = f'Dear {user.name},\n\n' \
                f'You have successfully placed an order at Da Nang Milktea.' \
                f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, env("EMAIL_HOST_USER"), [user.email])
    return mail_sent

