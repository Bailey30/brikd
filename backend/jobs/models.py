from django.db import models

from common.models import BaseModel
from companies.models import Company
from sites.models import Site

# Create your models here.


class Job(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    daily_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        rate = (
            (f"£{self.hourly_rate}/hr" if self.hourly_rate else None)
            or (f"£{self.daily_rate}/day" if self.daily_rate else None)
            or "Rate not set"
        )

        return f"{self.title} - {self.company.name} - {rate}"

    @property
    def id(self):
        return self.id
