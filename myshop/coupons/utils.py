from .models import Coupon
from django.utils import timezone


def apply_coupon_if_valid(code, request):
    now = timezone.now()
    try:
        coupon = Coupon.objects.get(
            code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
        )

        request.session["coupon_id"] = coupon.id
    except Coupon.DoesNotExist:
        request.session["coupon_id"] = None
