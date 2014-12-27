from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now_add=True)

    admin_id = models.CharField(max_length=30, db_index=True, unique=True)

    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    location_address = models.CharField(max_length=255, null=True, blank=True)

    # location_gps_lat = models.FloatField(null=True, blank=True)
    # location_gps_lon = models.FloatField(null=True, blank=True)

    def yes_attending(self):
        return self.eventattending_set.filter(choice="yes")

    def maybe_attending(self):
        return self.eventattending_set.filter(choice="maybe")

    def no_attending(self):
        return self.eventattending_set.filter(choice="no")

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.slug)


class EventAttending(models.Model):
    name = models.CharField(max_length=255)
    choice = models.CharField(max_length=255, choices=(('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')))
    event = models.ForeignKey(Event)
    uuid = models.CharField(max_length=255, db_index=True)
    answered_at = models.DateTimeField(auto_now_add=True)
    private_answer = models.BooleanField(default=False)


class Comment(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    event = models.ForeignKey(Event)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']
