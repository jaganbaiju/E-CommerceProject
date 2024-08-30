from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from Cart.models import Cart, CartItem
from e_app.models import Product

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, p_id):
    product = Product.objects.get(id=p_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # quantity adding
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()

    return redirect('cart:cart_details')


def cart_details(request, cart_item=None, total=0, counter=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(cart=cart, active=True)
        for cart_items in cart_item:
            total += (cart_items.product.price * cart_items.quantity)
            counter += cart_items.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', dict(cart_item=cart_item, total=total, counter=counter))


def cart_remove(request, p_id):
    # product = Product.objects.get(id=p_id)
    product = get_object_or_404(Product, id=p_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart_details')


def cart_delete(request, p_id):
    product = Product.objects.get(id=p_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(cart=cart, product=product)

    cart_item.delete()

    return redirect('cart:cart_details')
