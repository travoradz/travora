from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Trip, Customer, AgencySettings
from accounts.decorators import subscription_required
from django.utils.formats import date_format

@login_required
@subscription_required
def trips_list(request):
    trips = Trip.objects.filter(user=request.user)
    return render(
        request,
        "trips/list.html",
        {
            "trips": trips,
        },
    )


@login_required
@subscription_required
def add_trip(request):
    if request.method == "POST":
        Trip.objects.create(
            user=request.user,
            name=request.POST["name"],
            destination=request.POST["destination"],
            duration=request.POST["duration"],
            airline=request.POST["airline"],
            trip_type=request.POST["trip_type"],
            guide_name=request.POST["guide_name"],
            stop_city=request.POST["stop_city"],
            hotel=request.POST["hotel"],
            departure_date=request.POST["departure_date"],
            return_date=request.POST["return_date"],
            seats=request.POST["seats"],
            double_price=request.POST["double_price"],
            triple_price=request.POST["triple_price"],
            quad_price=request.POST["quad_price"],
            quint_price=request.POST["quint_price"],
            notes=request.POST["notes"],
        )
        return redirect("trips")

    return render(request, "trips/add.html")


@login_required
@subscription_required
def edit_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id, user=request.user)

    if request.method == "POST":
        trip.name = request.POST["name"]
        trip.destination = request.POST["destination"]
        trip.duration = request.POST["duration"]
        trip.airline = request.POST["airline"]
        trip.trip_type = request.POST["trip_type"]
        trip.guide_name = request.POST["guide_name"]
        trip.stop_city = request.POST["stop_city"]
        trip.hotel = request.POST["hotel"]
        trip.departure_date = request.POST["departure_date"]
        trip.return_date = request.POST["return_date"]
        trip.seats = request.POST["seats"]
        trip.double_price = request.POST["double_price"]
        trip.triple_price = request.POST["triple_price"]
        trip.quad_price = request.POST["quad_price"]
        trip.quint_price = request.POST["quint_price"]
        trip.notes = request.POST["notes"]
        trip.save()

        return redirect("trips")

    return render(
        request,
        "trips/edit.html",
        {
            "trip": trip,
        },
    )


@login_required
@subscription_required
def delete_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id, user=request.user)
    trip.delete()
    return redirect("trips")
@login_required
@subscription_required
def customers_list(request):
    if request.method == "POST":
        trip = Trip.objects.get(
            id=request.POST["trip"],
            user=request.user
        )

        room_type = request.POST["room_type"]

        if room_type == "ثنائية":
            total_price = trip.double_price
        elif room_type == "ثلاثية":
            total_price = trip.triple_price
        elif room_type == "رباعية":
            total_price = trip.quad_price
        else:
            total_price = trip.quint_price

        Customer.objects.create(
            trip=trip,
            user=request.user,
            full_name=request.POST["full_name"],
            phone=request.POST["phone"],
            room_type=room_type,
            total_price=total_price,
            group_code=request.POST.get("group_code", ""),
            amount_paid=request.POST["amount_paid"],
        )

        return redirect("customers")

    search = request.GET.get("q")

    customers = Customer.objects.filter(
        user=request.user
    ).select_related("trip")

    if search:
        customers = customers.filter(
            full_name__icontains=search
        )

    trips = Trip.objects.filter(user=request.user)

    return render(
        request,
        "customers/list.html",
        {
            "customers": customers,
            "trips": trips,
        },
    )


@login_required
@subscription_required
def edit_customer(request, customer_id):

    customer = Customer.objects.get(
        id=customer_id,
        user=request.user
    )

    if request.method == "POST":

        trip = Trip.objects.get(id=request.POST["trip"])
        room_type = request.POST["room_type"]

        if room_type == "ثنائية":
            total_price = trip.double_price
        elif room_type == "ثلاثية":
            total_price = trip.triple_price
        elif room_type == "رباعية":
            total_price = trip.quad_price
        else:
            total_price = trip.quint_price

        customer.full_name = request.POST["full_name"]
        customer.phone = request.POST["phone"]
        customer.trip = trip
        customer.room_type = room_type
        customer.total_price = total_price
        customer.amount_paid = request.POST["amount_paid"]

        customer.save()

        return redirect("customers")

    return render(
        request,
        "customers/edit.html",
        {
            "customer": customer,
            "trips": Trip.objects.all(),
        },
    )


@login_required
@subscription_required
def delete_customer(request, customer_id):

    customer = Customer.objects.get(
        id=customer_id,
        user=request.user
    )

    customer.delete()

    return redirect("customers")


from django.contrib.auth.decorators import login_required
from accounts.decorators import subscription_required
from django.shortcuts import render, redirect
from .models import AgencySettings

@login_required
@subscription_required
def agency_settings(request):
    settings, created = AgencySettings.objects.get_or_create(
        user=request.user,
        defaults={
            "agency_name": request.user.first_name,
            "phone": "",
            "email": request.user.email,
            "address": "",
            "city": "",
        },
    )

    if request.method == "POST":
        settings.agency_name = request.POST.get("agency_name")
        settings.phone = request.POST.get("phone")
        settings.email = request.POST.get("email")
        settings.address = request.POST.get("address")
        settings.city = request.POST.get("city")

        if request.FILES.get("logo"):
            settings.logo = request.FILES["logo"]

        settings.save()

        return redirect("agency_settings")

    return render(
        request,
        "settings.html",
        {
            "settings": settings,
        },
    )
@login_required
@subscription_required
def print_customer(request, customer_id):
    customer = Customer.objects.get(
        id=customer_id,
        user=request.user
    )

    settings = AgencySettings.objects.get(
        user=request.user
    )

    return render(
        request,
        "customers/print.html",
        {
            "customer": customer,
            "settings": settings,
        },
    )
from django.shortcuts import render, get_object_or_404
from .models import Trip, Room, Customer

from django.shortcuts import render, get_object_or_404, redirect
from .models import Trip, Room, Customer
@login_required
@subscription_required
def rooming(request, trip_id):

    trip = get_object_or_404(Trip, id=trip_id)

    customers = Customer.objects.filter(
        trip=trip
    ).order_by("room_type", "group_code", "full_name")

    rooms = Room.objects.filter(trip=trip).prefetch_related("customers")

    # نقل زبون إلى غرفة أخرى
    if request.method == "POST" and "move_customer" in request.POST:

        customer = get_object_or_404(
            Customer,
            id=request.POST["customer_id"],
            trip=trip,
        )

        room = get_object_or_404(
            Room,
            id=request.POST["room_id"],
            trip=trip,
        )

        customer.room = room
        customer.save()

        return redirect("rooming", trip_id=trip.id)

    # التسكين التلقائي
    if request.method == "POST" and "auto_rooming" in request.POST:

        Room.objects.filter(trip=trip).delete()

        room_number = 101

        room_sizes = {
            "ثنائية": 2,
            "ثلاثية": 3,
            "رباعية": 4,
            "خماسية": 5,
        }

        for room_type, size in room_sizes.items():

            room_customers = list(
                customers.filter(room_type=room_type)
            )

            processed = set()

            for customer in room_customers:

                if customer.id in processed:
                    continue

                room = Room.objects.create(
                    trip=trip,
                    room_number=str(room_number),
                    room_type=room_type,
                )

                if customer.group_code:

                    same_group = [
                        c for c in room_customers
                        if c.group_code == customer.group_code
                        and c.id not in processed
                    ]

                    for c in same_group[:size]:
                        c.room = room
                        c.save()
                        processed.add(c.id)

                else:

                    customer.room = room
                    customer.save()
                    processed.add(customer.id)

                room_number += 1

        return redirect("rooming", trip_id=trip.id)

    rooms = Room.objects.filter(trip=trip).prefetch_related("customers")

    return render(
        request,
        "rooming.html",
        {
            "trip": trip,
            "customers": customers,
            "rooms": rooms,
        },
    )


@login_required
@subscription_required
def move_customer(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id,
        user=request.user,
    )

    rooms = Room.objects.filter(
        trip=customer.trip,
        room_type=customer.room_type,
    ).prefetch_related("customers")

    if request.method == "POST":

        room = get_object_or_404(
            Room,
            id=request.POST["room_id"],
        )

        customers_count = Customer.objects.filter(
            room=room
        ).count()

        room_limit = {
            "ثنائية": 2,
            "ثلاثية": 3,
            "رباعية": 4,
            "خماسية": 5,
        }

        if customers_count < room_limit[room.room_type]:

            customer.room = room
            customer.save()

            return redirect(
                "rooming",
                trip_id=customer.trip.id,
            )

    return render(
        request,
        "move_customer.html",
        {
            "customer": customer,
            "rooms": rooms,
        },
    )
@login_required
@subscription_required
def print_rooming(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
    )

    rooms = Room.objects.filter(
        trip=trip
    ).prefetch_related("customers")

    return render(
        request,
        "print_rooming.html",
        {
            "trip": trip,
            "rooms": rooms,
        },
    )

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

@staff_member_required
def admin_support(request):

    users = User.objects.all().order_by("username")

    return render(
        request,
        "admin_support.html",
        {
            "users": users,
        },
    )
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from accounts.models import SupportMessage, Subscription


@staff_member_required
def admin_chat(request, user_id):

    agency = get_object_or_404(
        User,
        id=user_id,
    )

    messages = SupportMessage.objects.filter(
        user=agency
    ).order_by("created_at")

    subscription, created = Subscription.objects.get_or_create(
        user=agency
    )

    months = {
        "January": "جانفي",
        "February": "فيفري",
        "March": "مارس",
        "April": "أفريل",
        "May": "ماي",
        "June": "جوان",
        "July": "جويلية",
        "August": "أوت",
        "September": "سبتمبر",
        "October": "أكتوبر",
        "November": "نوفمبر",
        "December": "ديسمبر",
    }

    start = subscription.start_date.strftime("%d %B %Y")
   
    end = f"متبقي {subscription.days_left} يوم"

    for en, ar in months.items():
        start = start.replace(en, ar)
        end = end.replace(en, ar)

    if request.method == "POST":

        SupportMessage.objects.create(
            user=agency,
            message=request.POST["message"],
            is_admin=True,
        )

        return redirect(
            "admin_chat",
            user_id=agency.id,
        )

    return render(
        request,
        "admin_chat.html",
        {
            "agency": agency,
            "messages": messages,
            "subscription": subscription,
            "start_date_ar": start,
            "end_date_ar": end,
        },
    )



from django.utils import timezone
from datetime import timedelta
from accounts.models import Subscription

@staff_member_required
def activate_subscription(request, user_id):

    agency = get_object_or_404(User, id=user_id)

    subscription, created = Subscription.objects.get_or_create(
        user=agency
    )

    subscription.start_date = timezone.now().date()
    subscription.end_date = timezone.now().date() + timedelta(days=30)
    subscription.is_active = True
    subscription.save()

    return redirect("admin_chat", user_id=agency.id)