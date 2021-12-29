from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from .models import OrderItem, Order
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


@staff_member_required
def admin_order_detail(request, order_id):
    return render(
        request,
        "admin/orders/order/detail.html",
        {"order": get_object_or_404(Order, id=order_id)},
    )


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = get_pdf_response(order_id)
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + "css/pdf.css")]
    )
    return response


def get_pdf_response(order_id):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order_id}.pdf"
    return response
