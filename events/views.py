from uuid import uuid4

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from .forms import EventForm, EventAttendyForm
from .models import Event, EventAttending


def new_event(request):
    form = EventForm(request.POST) if request.method == "POST" else EventForm()

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


def event_admin(request, admin_id):
    event = get_object_or_404(Event, admin_id=admin_id)

    if request.method == "POST":
        form = EventForm(request.POST)
    else:
        form = EventForm({
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "time": event.time,
            "location_address": event.location_address,
        })

    if request.method == "POST" and form.is_valid():
        event.title = form.cleaned_data["title"]

        event.description = form.cleaned_data["description"]

        event.date = form.cleaned_data["date"]
        event.time = form.cleaned_data["time"]

        event.location_address = form.cleaned_data["location_address"]

        event.save()

        return HttpResponseRedirect(reverse("event_admin", args=(event.admin_id,)))

    return render(request, "events/event_form.haml", {
        "form": form,
        "event": event,
    })


def event_view(request, slug, user_uuid=None):
    event = get_object_or_404(Event, slug=slug)

    event_attending = get_object_or_404(EventAttending, uuid=user_uuid) if user_uuid else None

    if request.method == "POST":
        form = EventAttendyForm(request.POST)
    elif event_attending:
        form = EventAttendyForm({
            "name": event_attending.name,
            "choice": event_attending.choice,
        })
    else:
        form = EventAttendyForm()

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
