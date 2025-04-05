from django import forms
from datetime import date, timedelta

class BookingDateForm(forms.Form):
    booking_date = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Select a Booking Date",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        self.fields['booking_date'].widget.attrs.update({
            'min': today,
            'max': today + timedelta(days=14),
        })