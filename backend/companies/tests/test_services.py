from django.test import TestCase
from companies.models import Company
from companies.services import CompanyService

from companies.tests.utils import create_test_company


class CompanyServiceTests(TestCase):
    def test_no_company(self):
        self.assertEqual(0, Company.objects.count())

    def test_company_create(self):
        company = create_test_company()
        self.assertEqual(1, Company.objects.count())
        self.assertEqual("test@email.com", company.profile.email)
        self.assertEqual("name", company.name)

    def test_company_get(self):
        company = create_test_company()

        get_companies = CompanyService().get(company.id)

        self.assertEqual("test@email.com", get_companies.profile.email)
