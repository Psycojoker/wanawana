from django.shortcuts import render


def new_event(request):
    return render(request, "events/new.haml", {})
