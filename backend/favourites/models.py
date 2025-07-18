from django.db import models

from common.models import BaseModel, BaseUser
from jobs.models import Job


class Favourite(BaseModel):
    user = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name="favourites"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="favourited_by",  # Job.favourited_by
    )

    class Meta:  # pyright: ignore
        unique_together = ("user", "job")  # Prevent duplicate favorites
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.job.title}"
