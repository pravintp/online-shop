from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from orders.models import Order


@task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    email = set_email_contents(order)
    output = BytesIO()
    generate_pdf(order, output)
    email.attach(f"order_{order.id}.pdf", output.getvalue(), "application/pdf")
    email.send()


def set_email_contents(order):
    subject = f"My Shop - EE Invoice no. {order.id}"
    message = "Please, find attached the invoice for your recent purchase."
    return EmailMessage(subject, message, "admin@myshop.com", [order.email])


def generate_pdf(order, output):
    html = render_to_string("orders/order/pdf.html", {"order": order})
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + "css/pdf.css")]
    weasyprint.HTML(string=html).write_pdf(output, stylesheets=stylesheets)
