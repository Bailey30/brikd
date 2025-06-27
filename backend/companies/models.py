from django.db import models

from common.models import BaseUser

# Create your models here.


class Company(models.Model):
    profile = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    @property
    def id(self):
        return self.id
