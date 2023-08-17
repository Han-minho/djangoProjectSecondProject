import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from payment.tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # 잘못된 페이로드
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # 잘못된 서명
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)

            except Order.DoesNotExist:
                return HttpResponse(status=404)
        # 주문을 결제 완료로 표시
        order.paid = True
        # Stripe 결제 ID 저장
        order.stripe_id = session.payment_intent
        order.save()
        # 비동기 작업 실행
        payment_completed.delay(order.id)

    return HttpResponse(status=200)