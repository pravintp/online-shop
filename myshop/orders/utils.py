from .models import OrderItem


def apply_discount(order, cart):
    order.coupon = cart.coupon
    order.discount = cart.coupon.discount


def add_items_in_the_cart_to_order_and_clear_cart(cart, order):
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            price=item["price"],
            quantity=item["quantity"],
        )
    cart.clear()
