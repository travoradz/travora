from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):

    DESTINATIONS = [
        ("مكة", "مكة"),
        ("المدينة", "المدينة"),
        ("مكة والمدينة", "مكة والمدينة"),
    ]

    TRIP_TYPES = [
        ("مباشرة", "مباشرة"),
        ("غير مباشرة", "غير مباشرة"),
    ]

    name = models.CharField(max_length=200)

    destination = models.CharField(
        max_length=30,
        choices=DESTINATIONS,
    )

    duration = models.CharField(max_length=50)

    airline = models.CharField(max_length=100)

    trip_type = models.CharField(
        max_length=20,
        choices=TRIP_TYPES,
        default="مباشرة",
    )

    guide_name = models.CharField(
        max_length=150,
        blank=True,
    )

    stop_city = models.CharField(
        max_length=150,
        blank=True,
    )

    hotel = models.CharField(max_length=200)

    departure_date = models.DateField()

    return_date = models.DateField()

    seats = models.PositiveIntegerField()

    double_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    triple_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    quad_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    quint_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_number = models.CharField(max_length=20)

    room_type = models.CharField(
        max_length=20,
        choices=[
            ("ثنائية", "ثنائية"),
            ("ثلاثية", "ثلاثية"),
            ("رباعية", "رباعية"),
            ("خماسية", "خماسية"),
        ]
    )

    def str(self):
        return f"{self.room_number} - {self.trip.name}"
class Booking(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    full_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    pilgrims = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.full_name
class Customer(models.Model):
    ROOM_TYPES = [
        ("ثنائية", "ثنائية"),
        ("ثلاثية", "ثلاثية"),
        ("رباعية", "رباعية"),
        ("خماسية", "خماسية"),
    ]

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    full_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES,
        default="رباعية",
    )

    # 👥 رقم المجموعة
    group_code = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # 🏨 الغرفة التي تم تسكين الزبون فيها
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers",
    )

    def remaining_amount(self):
        return self.total_price - self.amount_paid

    def str(self):
        return self.full_name

class AgencySettings(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    agency_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=30)

    email = models.EmailField()

    address = models.CharField(max_length=250)

    city = models.CharField(max_length=100)

    logo = models.ImageField(
        upload_to="agency_logos/",
        blank=True,
        null=True,
    )

    def str(self):
        return self.agency_name