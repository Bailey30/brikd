from companies.models import Company
from companies.services import CompanyService
from rest_framework.response import Response
from typing import cast


def res_type(request):
    return cast(Response, request)


def create_test_company(
    email="test@email.com", password="password", name="name"
) -> Company:
    company = CompanyService().create(email, password, name)
    return company


test_company_credentials = {
    "email": "test@email.com",
    "password": "password",
    "name": "org",
}

test_site_credentials = {"name": "test_site", "postcode": "NW2555"}
