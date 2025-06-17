from typing import List

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from companies.models import Company
from common.models import BaseUser


User = get_user_model()


class CompanyService:
    def create(self, email: str, password: str, name: str) -> Company:
        # 1. Create the BaseUser
        user = User.objects.create_user(
            email=email,
            password=password,
            is_active=True,
            is_admin=False,
        )

        # 2. Create the Company that links to this user
        company = Company.objects.create(profile=user, name=name)

        return company

    def get(self, id: int) -> Company:
        company = Company.objects.get(id=id)
        return company

    def list(self) -> QuerySet[Company]:
        companys = Company.objects.all()
        return companys
