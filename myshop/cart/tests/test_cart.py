from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from ..cart import Cart
from django.conf import settings

from shop.models import Product, Category


class CartTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="camera", slug="camera")
        self.product = Product.objects.create(
            name="canon",
            slug="canon",
            price=24000,
            category_id=1,
        )
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()
        settings.CART_SESSION_ID = "test"
        self.cart = Cart(self.request)

    def test_cart_add_should_add_product_to_cart(self):
        self.cart.add(product=self.product, quantity=1)
        self.assertEqual(len(self.cart), 1)

    def test_cart_remove_should_remove_product_from_cart(self):
        self.cart.add(product=self.product, quantity=1)
        self.cart.remove(self.product)
        self.assertEqual(len(self.cart), 0)

    def test_cart_clear_should_clear_all_items_from_cart(self):
        self.cart.add(product=self.product, quantity=5)
        self.cart.clear()
        self.assertRaises(KeyError, lambda: self.cart.session["test"])
