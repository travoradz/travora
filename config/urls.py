from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views
from packages import views as package_views
from accounts.views import profit_loss
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

    # ✈️ صفحات الرحلات
    path(
        "trips/",
        include("packages.urls"),
    ),

    # 💰 الإدارة المالية
    path(
        "set-financial-password/",
        views.set_financial_password,
        name="set_financial_password",
    ),

    path(
        "financial-unlock/",
        views.financial_unlock,
        name="financial_unlock",
    ),

    path(
        "profit-loss/",
        profit_loss,
        name="profit_loss",
    ),
    path(
    "financial/export/excel/",
    views.export_financial_excel,
    name="export_financial_excel",
),
path(
    "financial/export/pdf/",
    views.export_financial_pdf,
    name="export_financial_pdf",
),
path(
    "subscription/chat/",
    views.subscription_chat,
    name="subscription_chat",
),

# لوحة الإدارة
path(
    "admin-panel/",
    views.admin_panel,
    name="admin_panel",
),

# طلبات الاشتراك
path(
    "admin-panel/subscriptions/",
    views.subscription_requests,
    name="subscription_requests",
),

# رسائل الدعم
path(
    "admin-panel/messages/",
    views.support_messages,
    name="support_messages",
),

# الوكالات
path(
    "admin-panel/agencies/",
    views.agencies,
    name="agencies",
),

# تسجيل دخول الإدارة
path(
    "admin-panel/login/",
    views.admin_panel_login,
    name="admin_panel_login",
),

# إحصائيات الإدارة
path(
    "admin-panel/statistics/",
    views.admin_statistics,
    name="admin_statistics",
),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )