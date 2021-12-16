from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            cart.add_all_items_in_the_cart_to_order_and_clear_the_cart(order)
            order_created.delay(order.id)
            request.session["order_id"] = order.id
            return redirect(reverse("payment:process"))
    return render(
        request, "orders/order/create.html", {"cart": cart, "form": OrderCreateForm()}
    )
