from uuid import uuid4

from django import forms
from django.template.defaultfilters import slugify

from .utils import generate_random_password
from .models import Event


class EventForm(forms.Form):
    title = forms.CharField()
    admin_email = forms.EmailField(required=False, label="Administrator email (optional)")
    send_notification_emails = forms.BooleanField(required=False, initial=False)
    slug = forms.SlugField(required=False, label="Public url (optional)")
    description = forms.CharField(required=False, widget=forms.Textarea, label="Description (optional)")
    date = forms.DateField(required=False, widget=forms.DateInput, input_formats=['%d/%m/%Y'])
    time = forms.TimeField(required=False, widget=forms.TimeInput)
    location_address = forms.CharField(required=False, label="Location address (optional)")

    def clean_title(self):
        if len(self.cleaned_data["title"].strip()) == 0:
            raise forms.ValidationError("The event title can't be an empty string")

        return self.cleaned_data["title"]

    def generate_admin_id(self):
        admin_id = str(uuid4())

        while Event.objects.filter(admin_id=admin_id).exists():
            admin_id = str(uuid4())

        return admin_id

    def generate_slug(self):
        base_slug = self.cleaned_data["slug"] if self.cleaned_data["slug"] else slugify(self.cleaned_data["title"])
        slug = base_slug

        while Event.objects.filter(slug=slug).exists():
            slug = base_slug + "-%s" % generate_random_password(5)

        return slug

    # wait for django leaflet
    # location_gps_lat
    # location_gps_lon


class EventAttendyForm(forms.Form):
    name = forms.CharField()
    choice = forms.ChoiceField(choices=(('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')))
    private_answer = forms.BooleanField(required=False)

    def clean_name(self):
        if len(self.cleaned_data["name"].strip()) == 0:
            raise forms.ValidationError("Your name can't be an empty string")

        return self.cleaned_data["name"]


class CommentForm(forms.Form):
    comment_name = forms.CharField()
    comment_content = forms.CharField()

    def clean_comment_content(self):
        if len(self.cleaned_data["comment_content"].strip()) == 0:
            raise forms.ValidationError("Your comment can't be an empty string")

        return self.cleaned_data["comment_content"]

    def clean_comment_name(self):
        if len(self.cleaned_data["comment_name"].strip()) == 0:
            raise forms.ValidationError("Your name can't be an empty string")

        return self.cleaned_data["comment_name"]
