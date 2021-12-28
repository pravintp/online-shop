from django.test import TestCase
from django.urls import reverse

from shop.models import Product, Category


class TranslationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="tea", slug="tea")
        product = Product.objects.create(
            name="tea",
            slug="tea",
            price=100,
            category_id=1,
        )
        product.set_current_language("es")
        product.name = "te"

    def test_response_should_contain_translation_for_the_product_tea(self):
        url = reverse("orders:order_create")
        self.response = self.client.get(url)
        self.assertContains(self.response, "te")
