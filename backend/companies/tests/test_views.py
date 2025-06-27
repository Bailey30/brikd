from rest_framework.response import Response
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from common.test_utils import res_type
from companies.tests.utils import create_test_company

from typing import cast


class TestCompanyViews(APITestCase):
    def test_list_users(self):
        create_test_company()

        res = cast(Response, self.client.get(reverse("companies:")))

        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(cast(list[dict], res.data)))

    def test_create_company(self):
        company = {
            "email": "test2@email.com",
            "name": "org_2",
            "password": "password",
        }

        res = res_type(
            self.client.post(reverse("companies:create"), company, format="json")
        )

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(company["email"], res.data["company"]["profile"]["email"])
        self.assertEqual(company["name"], res.data["company"]["name"])
        self.assertEqual(
            res.data["company"]["id"], res.data["company"]["profile"]["id"]
        )
