from django.urls import path
from . import views

urlpatterns = [
    # الرحلات
    path("", views.trips_list, name="trips"),
    path("add/", views.add_trip, name="add_trip"),
    path("edit/<int:trip_id>/", views.edit_trip, name="edit_trip"),
    path("delete/<int:trip_id>/", views.delete_trip, name="delete_trip"),

    # الزبائن
    path("customers/", views.customers_list, name="customers"),
    path("customers/edit/<int:customer_id>/", views.edit_customer, name="edit_customer"),
    path("customers/delete/<int:customer_id>/", views.delete_customer, name="delete_customer"),
    path(
        "customers/print/<int:customer_id>/",
        views.print_customer,
        name="print_customer",
    ),
path(
    "rooming/<int:trip_id>/",
    views.rooming,
    name="rooming",
),
path(
    "move-customer/<int:customer_id>/",
    views.move_customer,
    name="move_customer",
),

path(
    "print-rooming/<int:trip_id>/",
    views.print_rooming,
    name="print_rooming",
),
path(
    "admin-support/",
    views.admin_support,
    name="admin_support",
),
path(
    "admin-chat/<int:user_id>/",
    views.admin_chat,
    name="admin_chat",
),
path(
    "activate-subscription/<int:user_id>/",
    views.activate_subscription,
    name="activate_subscription",
),
    # إعدادات الوكالة
    path("agency-settings/", views.agency_settings, name="agency_settings"),
]