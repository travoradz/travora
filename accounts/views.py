from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.utils import timezone
from accounts.decorators import subscription_required
from packages.models import Trip, Customer
from accounts.models import Subscription
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.utils import timezone
def login_view(request):

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")

        return render(request, "login.html", {
            "error": "البريد الإلكتروني أو كلمة المرور غير صحيحة."
        })

    return render(request, "login.html")


def signup_view(request):

    if request.method == "POST":

        agency_name = request.POST["agency_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=email).exists():
            return render(request, "signup.html", {
                "error": "البريد الإلكتروني مستخدم بالفعل."
            })

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=agency_name,
        )

        Subscription.objects.create(
            user=user
        )

        login(request, user)

        return redirect("/dashboard/")

    return render(request, "signup.html")
@login_required
@subscription_required
def dashboard_view(request):
    subscription = Subscription.objects.get(user=request.user)

    today = timezone.now().date()

    if subscription.end_date < today:
        subscription.is_active = False
        subscription.save()

    days_left = (subscription.end_date - today).days
    if days_left < 0:
        days_left = 0

    trips = Trip.objects.all()
    customers = Customer.objects.filter(user=request.user)

    trips_count = trips.count()
    customers_count = customers.count()

    total_received = (
        customers.aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
    )

    total_remaining = sum(
        customer.remaining_amount()
        for customer in customers
    )

    latest_customers = customers.order_by("-id")[:5]
    latest_trips = trips.order_by("-id")[:5]

    low_seats_trips = trips.filter(
        seats__lte=5,
        seats__gt=0
    ).order_by("seats")

    full_trips = trips.filter(seats=0)

    unpaid_customers = customers.exclude(
        amount_paid__gte=F("total_price")
    )

    expiring_subscription = days_left <= 5

    # توزيع الغرف
    double_rooms = customers.filter(room_type="ثنائية").count()
    triple_rooms = customers.filter(room_type="ثلاثية").count()
    quad_rooms = customers.filter(room_type="رباعية").count()
    quint_rooms = customers.filter(room_type="خماسية").count()

    # إشعارات الدعم
    unread_support = SupportMessage.objects.filter(
        user=request.user,
        is_admin=True,
        is_read=False
    ).count()

    # إحصائيات
    today_bookings = customers.count()
    month_bookings = customers.count()
    full_trips_count = trips.filter(seats=0).count()
    total_seats = trips.aggregate(Sum("seats"))["seats__sum"] or 0

    return render(
        request,
        "dashboard.html",
        {
            "subscription": subscription,
            "days_left": days_left,
            "trips_count": trips_count,
            "customers_count": customers_count,
            "total_received": total_received,
            "total_remaining": total_remaining,
            "latest_customers": latest_customers,
            "latest_trips": latest_trips,
            "low_seats_trips": low_seats_trips,
            "full_trips": full_trips,
            "unpaid_customers": unpaid_customers,
            "expiring_subscription": expiring_subscription,
            "subscription_days": days_left,
            "double_rooms": double_rooms,
            "triple_rooms": triple_rooms,
            "quad_rooms": quad_rooms,
            "quint_rooms": quint_rooms,
            "unread_support": unread_support,
            "today_bookings": today_bookings,
            "month_bookings": month_bookings,
            "full_trips_count": full_trips_count,
            "total_seats": total_seats,
        },
    )
def logout_view(request):

    logout(request)

    return redirect("/")
def subscription_expired(request):

    return render(
        request,
        "subscription_expired.html"
    )
def subscription_plans(request):

    return render(
        request,
        "subscription_plans.html"
    )
def payment_info(request):
    return render(request, "payment_info.html")
@login_required
def change_password(request):

    if request.method == "POST":

        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if not request.user.check_password(current_password):
            return render(request, "change_password.html", {
                "error": "كلمة المرور الحالية غير صحيحة."
            })

        if new_password != confirm_password:
            return render(request, "change_password.html", {
                "error": "كلمتا المرور غير متطابقتين."
            })

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        return render(request, "change_password.html", {
            "success": "تم تغيير كلمة المرور بنجاح."
        })

    return render(request, "change_password.html")
def payment_page(request):
    return render(request, "payment.html")
from .models import SupportMessage
from django.contrib.auth.decorators import login_required
@login_required
def support_chat(request):

    if request.method == "POST":
        SupportMessage.objects.create(
            user=request.user,
            message=request.POST.get("message"),
            image=request.FILES.get("image"),
            is_admin=False,
        )

        return redirect("support_chat")

    messages = SupportMessage.objects.filter(
        user=request.user
    ).order_by("created_at")

    # تعليم رسائل الإدارة كمقروءة
    messages.filter(
        is_admin=True,
        is_read=False
    ).update(is_read=True)

    return render(
        request,
        "support_chat.html",
        {
            "messages": messages,
        },
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def payment_page(request):
    return render(request, "payment.html")