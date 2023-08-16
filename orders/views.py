from django.shortcuts import render, redirect

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from orders.tasks import order_created
from django.urls import reverse


# Create your views here.
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 카트 목록 삭제
            cart.clear()
            # 비동기 작업 시작
            # order_created.delay(order.id)
            # 주문하기 세션 세팅
            request.session['order_id'] = order.id
            # 결제 대행사 서비스로 넘어간다.
            return redirect(reverse('payment:process'))
            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})

    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})