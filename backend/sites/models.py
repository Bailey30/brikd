from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import Point

from common.models import BaseModel
from companies.models import Company


class Site(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sites")
    name = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    location = geomodels.PointField(geography=True, default=Point(0, 0))

    def __str__(self):
        return f"id: {self.id} - {self.name} - {self.postcode}"

    def id(self):
        return self.id
