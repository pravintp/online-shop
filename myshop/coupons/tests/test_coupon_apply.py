import datetime

import requests
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Coupon


class CouponApplyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Coupon.objects.create(
            code="BookWarm",
            valid_from=timezone.now() - datetime.timedelta(days=1, seconds=1),
            valid_to=timezone.now() + datetime.timedelta(days=1, seconds=1),
            discount=10,
            active=True,
        )
        Coupon.objects.create(
            code="IAmDied",
            valid_from=timezone.now() - datetime.timedelta(days=2, seconds=1),
            valid_to=timezone.now() - datetime.timedelta(days=1, seconds=1),
            discount=50,
            active=True,
        )

    def test_should_not_apply_expired_coupon(self):
        url = reverse("cart:cart_detail")
        response = self.client.get(url)
        form = response.context["coupon_apply_form"]
        data = form.initial
        data["code"] = "IAmDied"
        session = self.client.session
        session["coupon_id"] = Coupon.objects.get(code="IAmDied").id
        self.response = self.client.post(reverse("coupons:apply"), data)
        self.assertEqual(self.client.session["coupon_id"], None)
