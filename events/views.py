from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView

from .forms import NewEventForm
from .models import Event


def new_event(request):
    form = NewEventForm(request.POST) if request.method == "POST" else NewEventForm()

    if request.method == "POST" and form.is_valid():
        event = Event()
        event.title = form.cleaned_data["title"]
        # event.slug = form.get_slug()

        event.description = form.cleaned_data["description"]

        event.admin_id = form.generate_admin_id()

        event.date = form.cleaned_data["date"]
        event.time = form.cleaned_data["time"]

        event.location_address = form.cleaned_data["location_address"]

        event.save()

        return HttpResponseRedirect(reverse("event_admin", args=(event.admin_id,)))

    return render(request, "events/new.haml", {
        "form": form,
    })


class EventAdminView(UpdateView):
    model = Event
    template_name = "events/event_form.haml"

    fields = [
        'title',
        'description',
        'date',
        'time',
        'location_address',
    ]

    def get_object(self):
        return get_object_or_404(Event, admin_id=self.kwargs["admin_id"])
