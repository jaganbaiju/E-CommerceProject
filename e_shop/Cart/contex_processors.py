from Cart.views import _cart_id
from Cart.models import CartItem, Cart

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return "{}"
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_item = CartItem.objects.all().filter(cart=cart[:1])

            for i in cart_item:
                item_count += i.quantity
        except Cart.DoesNotExist:
            item_count = 0

    return dict(item_count=item_count)
