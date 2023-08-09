from cart.cart import Cart


# 장바구니 요청 컨텍스트에 설정하기
def cart(request):
    return {'cart': Cart(request)}