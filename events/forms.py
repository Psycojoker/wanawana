from django import forms

from .utils import generate_random_password
from .models import Event


class NewEventForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField(required=False)
    description = forms.CharField(required=False)
    admin_email = forms.EmailField(required=False)
    date = forms.DateField(required=False)
    time = forms.TimeField(required=False)
    location_address = forms.CharField(required=False)

    def generate_admin_id(self):
        password = generate_random_password(15)

        while Event.objects.filter(admin_id=password):
            password = generate_random_password(15)

        return password

    # wait for django leaflet
    # location_gps_lat
    # location_gps_lon
