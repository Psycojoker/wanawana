from django.conf.urls import patterns, url


urlpatterns = patterns('events.views',
    url(r'^new/$', 'new_event', name='new_event'),
)
