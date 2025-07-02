from pprint import pprint
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from common.test_utils import test_user_credentials


class TestUserViews(APITestCase):
    def test_create_user(self):
        res = self.client.post(
            reverse("users:create"), test_user_credentials, format="json"
        )

        user = res.data["user"]
        print("User:", user)

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(user["name"], test_user_credentials["name"])
        self.assertEqual(user["profile"]["email"], test_user_credentials["email"])
        self.assertEqual(user["profile"]["account_type"], "jobseeker")
