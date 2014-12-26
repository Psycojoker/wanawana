from django.conf.urls import patterns, url


urlpatterns = patterns('events.views',
    url(r'^new/$', 'new_event', name='new_event'),
    url(r'^event_admin/(?P<admin_id>[a-zA-Z0-9-]+)/$', 'event_admin', name='event_admin'),
    url(r'^(?P<slug>[a-zA-Z0-9-]+)/(?P<user_uuid>[a-zA-Z0-9-]+)/$', 'event_view', name='event_detail_uuid'),
    url(r'^(?P<slug>[a-zA-Z0-9-]+)/$', 'event_view', name='event_detail'),
)
