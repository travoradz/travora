from django.utils import timezone
from accounts.models import Subscription


class SubscriptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            try:
                subscription = Subscription.objects.get(
                    user=request.user
                )

                if (
                    subscription.is_active
                    and subscription.end_date < timezone.now().date()
                ):
                    subscription.is_active = False
                    subscription.save()

            except Subscription.DoesNotExist:
                pass

        response = self.get_response(request)

        return response