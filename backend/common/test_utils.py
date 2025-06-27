from companies.models import Company
from sites.models import Site
from companies.services import CompanyService
from rest_framework.response import Response
from typing import cast

from sites.services import SiteService


def res_type(request):
    return cast(Response, request)


def create_test_company(
    email="test@email.com", password="password", name="name"
) -> Company:
    """
    Creates a BaseUser and Company object in the database.
    """
    company = CompanyService().create(email, password, name)
    return company


def create_test_site(name="test_site", postcode="CR0 3RL", company=None) -> Site:
    if company is None:
        company = create_test_company()

    site = SiteService().create(name, postcode, company)
    return site


test_company_credentials = {
    "email": "test@email.com",
    "password": "password",
    "name": "org",
}

test_site_credentials = {"name": "test_site", "postcode": "CR0 3RL"}

test_job_details = {
    "title": "test_job",
    "description": "description",
    "hourly_rate": "10.00",
}
