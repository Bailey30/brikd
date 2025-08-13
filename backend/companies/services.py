from typing import List

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from companies.models import Company
from common.models import BaseUser
from jobs.alerts import JobAlertsClient


BaseUser = get_user_model()


class CompanyService:
    def create(self, email: str, password: str, name: str) -> Company:
        # Create the BaseUser
        user = BaseUser.objects.create_user(  # pyright: ignore
            email=email,
            password=password,
            is_active=True,
            is_admin=False,
            account_type="company",
        )

        # Create the Company that links to this user
        company = Company.objects.create(profile=user, name=name)

        # Creates an sns topic
        # JobAlerts().create_topic(company)

        return company

    def get(self, id: str) -> Company:
        company = Company.objects.get(profile_id=id)
        return company

    def list(self) -> QuerySet[Company]:
        companys = Company.objects.all()
        return companys
