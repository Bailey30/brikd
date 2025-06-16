from rest_framework.response import Response
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import TestCase
from rest_framework.views import status
from common.test_utils import res_type
from companies.models import Company
from companies.tests.utils import test_credentials


class TestAuthViews(TestCase):
    def test_should_create_jwt_for_valid_user(self):
        """
        Create user.
        Log in user.
        Get user data to check if token is in request cookies.
        """

        Company.objects.create_user(
            test_credentials["email"],
            test_credentials["password"],
            is_active=True,
            is_admin=False,
            name=test_credentials["name"],
        )

        res = res_type(
            self.client.post(reverse("auth:token_obtain_pair"), test_credentials)
        )

        self.assertEqual(200, res.status_code)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

        res = res_type(self.client.get(reverse("auth:user")))

        self.assertEqual(200, res.status_code)

    def test_should_logout_valid_user(self):
        """
        Create user.
        Log out user.
        Try to get user data to check if token is in request cookies.
        """

        Company.objects.create_user(
            test_credentials["email"],
            test_credentials["password"],
            is_active=True,
            is_admin=False,
            name=test_credentials["name"],
        )

        res = res_type(
            self.client.post(reverse("auth:token_obtain_pair"), test_credentials)
        )
        self.assertEqual(200, res.status_code)

        res = res_type(self.client.post(reverse("auth:logout")))
        self.assertEqual(204, res.status_code)

        res = res_type(self.client.get(reverse("auth:user")))
        self.assertEqual(401, res.status_code)
