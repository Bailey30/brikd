from pprint import pprint
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from common.test_utils import test_user_credentials
from users.factories import UserFactory
import os


class TestUserViews(APITestCase):
    def test_create_user(self):
        user_credentials = {
            **test_user_credentials,
            "distance_alerts": True,
            "alert_radius": 10,
            "phone_number": os.environ.get("TEST_PHONE_NUMBER"),
        }
        del user_credentials["search_postcode"]
        print("user_credentials:", user_credentials)

        res = self.client.post(reverse("users:create"), user_credentials, format="json")

        user = res.data["user"]
        print("user:", user)

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(user["name"], test_user_credentials["name"])
        self.assertEqual(user["phone_number"], os.environ.get("TEST_PHONE_NUMBER"))
        self.assertEqual(user["distance_alerts"], True)
        self.assertEqual(user["alert_radius"], 10)
        self.assertEqual(user["profile"]["email"], test_user_credentials["email"])
        self.assertEqual(user["profile"]["account_type"], "jobseeker")

        default_value_user = {
            **test_user_credentials,
            "email": "user2@email.com",
        }

        res = res.client.post(
            reverse("users:create"), default_value_user, format="json"
        )

        defaults_users = res.data["user"]
        print("defaults_users:", defaults_users)
        self.assertEqual(defaults_users["phone_number"], None)
        self.assertEqual(defaults_users["distance_alerts"], False)
        self.assertEqual(defaults_users["alert_radius"], 0)

    def test_update_user(self):
        user = UserFactory()

        res = self.client.post(
            reverse("auth:login"),
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
