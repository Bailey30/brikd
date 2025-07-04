from pprint import pprint
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from common.test_utils import test_user_credentials
from users.factories import UserFactory


class TestUserViews(APITestCase):
    def test_create_user(self):
        res = self.client.post(
            reverse("users:create"), test_user_credentials, format="json"
        )

        user = res.data["user"]

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(user["name"], test_user_credentials["name"])
        self.assertEqual(user["profile"]["email"], test_user_credentials["email"])
        self.assertEqual(user["profile"]["account_type"], "jobseeker")

    def test_update_user(self):
        user = UserFactory()

        res = self.client.post(
            reverse("auth:token_obtain_pair"),
            {"email": user.profile.email, "password": "password"},
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)

        res = self.client.patch(
            reverse("users:update", args=[user.id]),
            {"name": "john", "search_postcode": "OX39 4RB"},
        )

        updated_user = res.data["user"]

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertNotEqual(user.name, updated_user["name"])
        self.assertNotEqual(user.search_postcode, updated_user["search_postcode"])
