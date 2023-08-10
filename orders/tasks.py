from orders.models import Order
from django.core.mail import send_mail


def order_created(order_id):
    """
        Task to send e-mail notification when an order is
        successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message,
                          'hihi6024@gmail.com',
                          [order.email])
    return mail_sent
