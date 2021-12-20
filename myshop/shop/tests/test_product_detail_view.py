from django.test import TestCase
from django.urls import reverse

from ..models import Product, Category


class ProductDetailTest(TestCase):
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

    def test_product_detail_returns_404_for_invalid_product(self):
        self.response = self.client.get(
            reverse("shop:product_detail", args=[100, "camera"])
        )
        self.assertEquals(self.response.status_code, 404)
