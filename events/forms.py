from django import forms


class NewEventForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    admin_email = forms.EmailField(required=False)
