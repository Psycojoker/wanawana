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
