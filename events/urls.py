from django.conf.urls import patterns, url
from django.views.generic import DetailView

from .views import EventAdminView
from .models import Event


urlpatterns = patterns('events.views',
    url(r'^new/$', 'new_event', name='new_event'),
    url(r'^admin/(?P<admin_id>[a-zA-Z0-9-]+)/$', EventAdminView.as_view(), name='event_admin'),
    url(r'^(?P<slug>[a-zA-Z0-9-]+)/$', DetailView.as_view(model=Event, template_name="events/event_detail.haml"), name='event_detail'),
)
