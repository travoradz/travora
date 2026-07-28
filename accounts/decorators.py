from functools import wraps
from django.shortcuts import redirect
from django.utils import timezone
from .models import Subscription


def subscription_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        subscription = Subscription.objects.get(user=request.user)

        if subscription.end_date < timezone.now().date():
            subscription.is_active = False
            subscription.save()
            return redirect("subscription_expired")

        return view_func(request, *args, **kwargs)

    return wrapper