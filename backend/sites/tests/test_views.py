from django.urls import reverse
from rest_framework.test import APITestCase
from common.test_utils import test_site_credentials, create_test_company


class TestSiteViews(APITestCase):
    def test_should_create_site(self):
        site = {**test_site_credentials, "company": create_test_company()}

        res = self.client.post(reverse("sites:create"), site, format="json")
