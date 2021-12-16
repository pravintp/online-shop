from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .utils import apply_coupon_if_valid

# Create your views here.


@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        apply_coupon_if_valid(form.cleaned_data["code"], request)
    return redirect("cart:cart_detail")
