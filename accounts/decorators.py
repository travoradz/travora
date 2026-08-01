from functools import wraps
from django.shortcuts import redirect
from .models import Subscription


def subscription_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        try:
            subscription = Subscription.objects.get(user=request.user)

            if not subscription.is_active:
                return redirect("subscription_expired")

        except Subscription.DoesNotExist:
            return redirect("subscription_plans")

        return view_func(request, *args, **kwargs)

    return wrapper