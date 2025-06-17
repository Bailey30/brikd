from django.db import models
from django.core.validators import RegexValidator

from common.models import BaseModel
from companies.models import Company

# Create your models here.

uk_postcode_validator = RegexValidator(
    regex=r"^[A-Z]{1,2}[0-9R][0-9A-Z]?\s?[0-9][A-Z]{2}$",
    message="Invalid UK postcodel ",
    code="invalid_postcode",
)


class Site(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sites")
    name = models.CharField(max_length=255)
    post_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.post_code}"
