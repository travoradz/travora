from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Subscription(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    start_date = models.DateField(
        default=timezone.now
    )

    end_date = models.DateField(
        default=timezone.now
    )

    is_active = models.BooleanField(
        default=True
    )

    # كلمة السر الخاصة بالصفحة المالية
    # يتم تخزينها لاحقًا بشكل Hash وليس كنص عادي
    financial_password = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.end_date = self.start_date + timedelta(days=14)

        super().save(*args, **kwargs)

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