from django.shortcuts import render

from .forms import NewEventForm


def new_event(request):
    form = NewEventForm()

    return render(request, "events/new.haml", {
        "form": form,
    })
