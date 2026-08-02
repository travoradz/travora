from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta
from django.utils import timezone

class Subscription(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    start_date = models.DateField(default=timezone.now)

    trial_days = models.IntegerField(default=14)

    lifetime = models.BooleanField(default=False)

    financial_password = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )

    @property
    def days_left(self):
        if self.lifetime:
            return "مدى الحياة"

        end_date = self.start_date + timedelta(days=self.trial_days)
        remaining = (end_date - timezone.now().date()).days
        return max(remaining, 0)

    @property
    def is_active(self):
        if self.lifetime:
            return True

        return self.days_left > 0

    def str(self):
        return self.user.username

class SupportMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    image = models.ImageField(
        upload_to="support/",
        blank=True,
        null=True
    )

    is_admin = models.BooleanField(
        default=False
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def str(self):
        return self.user.username


class PaymentInfoRequest(models.Model):
    PAYMENT_METHODS = [
        ("ccp", "CCP"),
        ("gold", "Gold Card"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_sent = models.BooleanField(
        default=False
    )

    approved = models.BooleanField(
        default=False
    )

    def str(self):
        return f"{self.user.username} - {self.method}"