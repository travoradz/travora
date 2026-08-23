from django.db import models
from django.contrib.auth.models import User


from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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

    def str(self):
        return self.name
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("طيران", "طيران"),
        ("فندق", "فندق"),
        ("نقل", "نقل"),
        ("فيزا", "فيزا"),
        ("إشهار", "إشهار"),
        ("رواتب", "رواتب"),
        ("مكتب", "مكتب"),
        ("أخرى", "أخرى"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="أخرى",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    date = models.DateField(auto_now_add=True)

    notes = models.TextField(blank=True)

    def str(self):
        return self.title
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

    # =========================
    # الرحلة والوكالة
    # =========================

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    # =========================
    # معلومات الزبون
    # =========================

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=20
    )

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES,
        default="رباعية",
    )

    group_code = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    # =========================
    # السعر الأصلي
    # =========================

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    # =========================
    # العمولة / التخفيض
    # =========================

    commission = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # =========================
    # المبلغ المدفوع القديم
    #
    # نخليه موجود باش ما نكسروش
    # البيانات القديمة.
    # =========================

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # =========================
    # تاريخ الإضافة
    # =========================

    created_at = models.DateField(
        auto_now_add=True
    )

    # =========================
    # الغرفة
    # =========================

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers",
    )

    # =========================
    # السعر النهائي بعد العمولة
    # =========================

    def final_price(self):
        return self.total_price - self.commission

    # =========================
    # مجموع الدفعات
    #
    # إذا كانت هناك دفعات مسجلة
    # نستعملها.
    #
    # وإذا كان الزبون قديمًا وما عندوش
    # CustomerPayment نستعمل amount_paid
    # القديم حتى لا تضيع البيانات.
    # =========================
# =========================
# مجموع الدفعات
# =========================
def total_payments(self):
    return self.amount_paid


# =========================
# تحديث amount_paid
# =========================
def update_amount_paid(self):
    self.amount_paid = self.total_payments()
    self.save(
        update_fields=["amount_paid"]
    )
    return self.amount_paid


# =========================
# المبلغ المتبقي
# =========================
def remaining_amount(self):
    remaining = (
        self.final_price()
        - self.total_payments()
    )

    # ما نخليش المتبقي يولي بالسالب
    if remaining < 0:
        return 0

    return remaining


# =========================
# حالة الدفع
# =========================
def payment_status(self):
    total = self.total_payments()
    final = self.final_price()

    if total <= 0:
        return "غير مدفوع"

    elif total < final:
        return "دفع جزئي"

    else:
        return "مدفوع"
    # =========================
    # اسم الزبون
    # =========================

    def str(self):
        return self.full_name


# =========================================================
# دفعات الزبون
# =========================================================

class CustomerPayment(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    payment_date = models.DateField(
        auto_now_add=True
    )

    note = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def str(self):

        return (
            f"{self.customer.full_name} - "
            f"{self.amount} دج"
        )
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