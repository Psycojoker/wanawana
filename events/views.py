from uuid import uuid4

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView

from .forms import NewEventForm, NewAttendyForm
from .models import Event, EventAttending


def new_event(request):
    form = NewEventForm(request.POST) if request.method == "POST" else NewEventForm()

    if request.method == "POST" and form.is_valid():
        event = Event()
        event.title = form.cleaned_data["title"]
        event.slug = form.generate_slug()

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

    def get_success_url(self):
        return reverse("event_admin", args=(self.kwargs["admin_id"],))


def event_view(request, slug, user_uuid=None):
    event = get_object_or_404(Event, slug=slug)

    event_attending = get_object_or_404(EventAttending, uuid=user_uuid) if user_uuid else None

    if request.method == "POST":
        form = NewAttendyForm(request.POST)
    elif event_attending:
        form = NewAttendyForm({
            "name": event_attending.name,
            "choice": event_attending.choice,
        })
    else:
        form = NewAttendyForm()

    if request.method == "POST" and form.is_valid():
        if event_attending:
            event_attending.name = form.cleaned_data["name"]
            event_attending.choice = form.cleaned_data["choice"]
            event_attending.save()
        else:
            event_attending = EventAttending.objects.create(
                name=form.cleaned_data["name"],
                choice=form.cleaned_data["choice"],
                event=event,
                uuid=str(uuid4()),
            )

        return HttpResponseRedirect(reverse("event_detail_uuid", args=(event.slug, event_attending.uuid)))

    return render(request, "events/event_detail.haml", {
        "event": event,
        "form": form,
        "event_attending": event_attending,
    })
