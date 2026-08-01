from accounts.models import Subscription


class SubscriptionMiddleware:

    def __init__ (self, get_response):
        self.get_response = get_response

    def __call__ (self, request):

        if request.user.is_authenticated:
            try:
                Subscription.objects.get(
                    user=request.user
                )
            except Subscription.DoesNotExist:
                pass

        response = self.get_response(request)
        return response