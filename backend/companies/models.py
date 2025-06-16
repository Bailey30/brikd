from django.db import models

from common.models import BaseUser

# Create your models here.


class Company(BaseUser):
    name = models.CharField(max_length=255)
