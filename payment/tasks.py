import weasyprint
from celery.app import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from orders.models import Order
from django.conf import settings
from django.core.mail import EmailMessage
from io import BytesIO


@shared_task
def payment_completed(order_id):
    """
        주문이 성공적으로 결제된 경우 이메일 알림을 보내는 작업입니다.
    """
    order = Order.objects.get(id=order_id)
    # 인보이스 이메일 생성
    subject = f'My Shop - Invoice no. {order_id}'
    message = 'Please, find attached invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'hihi6024@gmail.com', [order.email])

    # pdf 생성
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()

    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    # pdf 파일 첨부
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    # 이메일 전송
    email.send()
