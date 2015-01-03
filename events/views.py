from uuid import uuid4

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string

from wanawana.utils import get_base_url

from .forms import EventForm, EventAttendyForm, CommentForm
from .models import Event, EventAttending, Comment


def new_event(request):
    form = EventForm(request.POST) if request.method == "POST" else EventForm()

    if request.method == "POST" and form.is_valid():
        event = Event()
        event.title = form.cleaned_data["title"]
        event.slug = form.generate_slug()

        event.admin_email = form.cleaned_data["admin_email"]
        event.send_notification_emails = form.cleaned_data["send_notification_emails"]

        event.description = form.cleaned_data["description"]

        event.admin_id = form.generate_admin_id()

        event.date = form.cleaned_data["date"]
        event.time = form.cleaned_data["time"]

        event.location_address = form.cleaned_data["location_address"]

        event.save()

        if event.admin_email:
            email_body = render_to_string("emails/new_event.txt", {
                "url_scheme": request.META["wsgi.url_scheme"],
                "base_url": get_base_url(request),
                "event_slug": event.slug,
                "event_admin_id": event.admin_id
            })

            send_mail("[Wanawana] the admin url for you event '%s'" % (event.title),
                      email_body,
                      'noreply@%s' % get_base_url(request),
                      [event.admin_email],
                      fail_silently=False)

        return HttpResponseRedirect(reverse("event_admin", args=(event.admin_id,)))

    return render(request, "events/new.haml", {
        "form": form,
        "current_base_url": request.META["wsgi.url_scheme"] + "://" + get_base_url(request) + "/",
    })


def event_admin(request, admin_id):
    def remove_first_zero(time):
        if time.startswith("0"):
            return time[1:]
        return time

    event = get_object_or_404(Event, admin_id=admin_id)

    if request.method == "POST":
        form = EventForm(request.POST)
    else:
        form = EventForm({
            "title": event.title,
            "description": event.description,
            "admin_email": event.admin_email,
            "send_notification_emails": event.send_notification_emails,
            "date": event.date.strftime("%d/%m/%Y") if event.date else None,
            "time": remove_first_zero(event.time.strftime("%H:%M")) if event.time else None,
            "location_address": event.location_address,
        })

    if request.method == "POST" and form.is_valid():
        event.title = form.cleaned_data["title"]

        event.description = form.cleaned_data["description"]

        event.admin_email = form.cleaned_data["admin_email"]
        event.send_notification_emails = form.cleaned_data["send_notification_emails"]

        event.date = form.cleaned_data["date"]
        event.time = form.cleaned_data["time"]

        event.location_address = form.cleaned_data["location_address"]

        event.save()

        return HttpResponseRedirect(reverse("event_admin", args=(event.admin_id,)))

    return render(request, "events/event_form.haml", {
        "form": form,
        "event": event,
        "current_base_url": request.META["wsgi.url_scheme"] + "://" + get_base_url(request) + "/",
        "current_page_url": request.META["wsgi.url_scheme"] + "://" + get_base_url(request) + request.META["PATH_INFO"],
    })


def event_view(request, slug, user_uuid=None):
    event = get_object_or_404(Event, slug=slug)

    event_attending = get_object_or_404(EventAttending, uuid=user_uuid) if user_uuid else None

    in_comment_posting_mode = request.method == "POST" and "comment_name" in request.POST and "comment_content" in request.POST

    comment_form = CommentForm(request.POST) if in_comment_posting_mode else CommentForm()

    if request.method == "POST" and not in_comment_posting_mode:
        form = EventAttendyForm(request.POST)
    elif event_attending:
        form = EventAttendyForm({
            "name": event_attending.name,
            "choice": event_attending.choice,
            "private_answer": event_attending.private_answer,
        })
    else:
        form = EventAttendyForm()

    if in_comment_posting_mode and comment_form.is_valid():
        Comment.objects.create(
            name=comment_form.cleaned_data["comment_name"],
            content=comment_form.cleaned_data["comment_content"],
            event=event,
        )

        if event_attending:
            return HttpResponseRedirect(reverse("event_detail_uuid", args=(event.slug, event_attending.uuid)))
        else:
            return HttpResponseRedirect(reverse("event_detail", args=(event.slug,)))

    if not in_comment_posting_mode and request.method == "POST" and form.is_valid():
        if event_attending:
            event_attending.name = form.cleaned_data["name"]
            event_attending.choice = form.cleaned_data["choice"]
            event_attending.private_answer = form.cleaned_data["private_answer"]
            event_attending.save()
        else:
            event_attending = EventAttending.objects.create(
                name=form.cleaned_data["name"],
                choice=form.cleaned_data["choice"],
                event=event,
                uuid=str(uuid4()),
                private_answer = form.cleaned_data["private_answer"],
            )

            if event.admin_email and event.send_notification_emails:
                email_body = render_to_string("emails/event_attending_answer.txt", {
                    "url_scheme": request.META["wsgi.url_scheme"],
                    "base_url": get_base_url(request),
                    "event_attending": event_attending,
                    "event": event,
                })

                send_mail("[Wanawana] %s has answer '%s' to your event '%s'" % (event_attending.name, event_attending.choice, event.title),
                         email_body,
                         "noreply@%s" % get_base_url(request),
                         [event.admin_email])

        return HttpResponseRedirect(reverse("event_detail_uuid", args=(event.slug, event_attending.uuid)))

    return render(request, "events/event_detail.haml", {
        "event": event,
        "form": form,
        "comment_form": comment_form,
        "event_attending": event_attending,
        "current_page_url": request.META["wsgi.url_scheme"] + "://" + get_base_url(request) + request.META["PATH_INFO"],
    })
