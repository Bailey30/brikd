from django.db import models
from common.models import BaseUser


class User(models.Model):
    profile = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)

    search_postcode = models.CharField(max_length=10, blank=True)
    search_location = models.CharField(max_length=255, blank=True)

    @property
    def id(self):
        # profile_id is defined when "profile" is set as primary_key
        return self.profile_id

    def __str__(self):
        return f"id: {self.id}, account_type: {self.profile.account_type}, name: {self.name}"
