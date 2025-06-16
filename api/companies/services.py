from typing import List
from companies.models import Company


class CompanyService:
    def create(self, email: str, password: str, name: str) -> Company:
        company = Company.objects.create_user(
            email, password, is_active=True, is_admin=False, name=name
        )
        company.save()
        return company

    def get(self, id: int) -> Company:
        company = Company.objects.get(id=id)
        return company

    def list(self) -> List[Company]:
        companys = Company.objects.all()
        return companys
