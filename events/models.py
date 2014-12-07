from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now_add=True)

    admin_id = models.EmailField(null=True, blank=True)

    date = models.DateField()
    time = models.TimeField()

    location_address = models.CharField(max_length=255)

    location_gps_lat = models.FloatField()
    location_gps_lon = models.FloatField()
