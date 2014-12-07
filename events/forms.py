from django import forms


class NewEventForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField(required=False)
    description = forms.CharField(required=False)
    admin_email = forms.EmailField(required=False)
    date = forms.DateField(required=False)
    time = forms.TimeField(required=False)
    location_address = forms.CharField(required=False)

    # wait for django leaflet
    # location_gps_lat
    # location_gps_lon
