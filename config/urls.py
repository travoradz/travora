from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views
from packages import views as package_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),

    path(
        "subscription-expired/",
        views.subscription_expired,
        name="subscription_expired",
    ),

    path(
        "subscription-plans/",
        views.subscription_plans,
        name="subscription_plans",
    ),

    path(
        "payment-info/",
        views.payment_info,
        name="payment_info",
    ),

    path(
        "payment/",
        views.payment_page,
        name="payment",
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password",
    ),

    # 💬 محادثة الوكالة
    path(
        "support/",
        views.support_chat,
        name="support_chat",
    ),

    # 💬 لوحة الإدارة للمحادثات
    path(
        "admin-support/",
        package_views.admin_support,
        name="admin_support",
    ),

    # صفحات الرحلات
    path(
        "trips/",
        include("packages.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )