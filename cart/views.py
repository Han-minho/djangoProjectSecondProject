from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.models import Product
from shop.recommender import Recommender


# Create your views here.
# 상품 장바구니에 추가
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('cart:cart_detail')


# 상품 장바구니에서 제거
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


# 장바구니 항목 추가 및 제거 이외의 작업을 처리
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'override': True})
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form,
                   'recommended_products': recommended_products})


