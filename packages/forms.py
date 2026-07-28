from django import forms
from .models import Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            "name",
            "destination",
            "duration",
            "hotel",
            "departure_date",
            "return_date",
            "pilgrims",
            "price",
        ]

        labels = {
            "name": "اسم الرحلة",
            "destination": "الوجهة",
            "duration": "مدة الرحلة",
            "hotel": "اسم الفندق",
            "departure_date": "تاريخ الانطلاق",
            "return_date": "تاريخ العودة",
            "pilgrims": "عدد المقاعد",
            "price": "السعر (دج)",
        }

        widgets = {
            "departure_date": forms.DateInput(attrs={"type": "date"}),
            "return_date": forms.DateInput(attrs={"type": "date"}),
        }