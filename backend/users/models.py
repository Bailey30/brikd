from django.db import models
from common.models import BaseUser
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import Point


class User(models.Model):
    profile = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    search_postcode = models.CharField(max_length=10, blank=True, null=True)
    search_location = models.CharField(max_length=255, blank=True, null=True)

    # TODO: make sure this is created and updated when the search postcode is created and updated.
    search_postcode_coordinates = geomodels.PointField(
        geography=True, default=Point(0, 0)
    )

    distance_alerts = models.BooleanField(default=False)
    alert_radius = models.IntegerField(default=0)

    @property
    def id(self):
        # profile_id is defined when "profile" is set as primary_key
        return self.profile_id

    def __str__(self):
        return f"id: {self.id}, account_type: {self.profile.account_type}, name: {self.name}"
