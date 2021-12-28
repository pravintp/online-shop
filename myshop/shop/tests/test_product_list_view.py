from django.urls import reverse
from django.test import TestCase

from ..models import Product, Category


class ProductListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_products = 10
        Category.objects.create(name="camera", slug="camera")

        for product in range(number_of_products):
            Product.objects.create(
                name=f"product {product}",
                slug=f"Product-{product}",
                price=product * 100,
                category_id=1,
            )

    def test_product_list_status_code(self):
        url = reverse("shop:product_list")
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_exists(self):
        url = reverse("shop:product_list")
        self.response = self.client.get(url)
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse("shop:product_list")
        self.response = self.client.get(url)
        self.assertTemplateUsed(self.response, "shop/product/list.html")

    def test_product_list_view_should_return_all_available_products(self):
        url = reverse("shop:product_list")
        self.response = self.client.get(url)
        self.assertEqual(len(self.response.context["products"]), 10)
