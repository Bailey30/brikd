from django.db import models

from common.models import BaseUser

# Create your models here.


class Company(models.Model):
    profile = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)

    @property
    def id(self):
        return self.profile_id

    def __str__(self):
        return f"id: {self.id}, account_type: {self.profile.account_type}, name: {self.name}"
