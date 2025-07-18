from pprint import pprint
from django.urls import reverse
from sites.models import Site
from rest_framework.test import APITestCase
from common.test_utils import (
    test_site_credentials,
    create_test_company,
    test_company_credentials,
)
from rest_framework import status


class TestSiteViews(APITestCase):
    def setUp(self):
        create_test_company()

        self.client.post(reverse("auth:login"), test_company_credentials)

    def test_should_create_site_for_logged_in_account(self):
        res = self.client.post(
            reverse("sites:create"), test_site_credentials, format="json"
        )

        # print("Site:", res.data["site"])

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(test_site_credentials["name"], res.data["site"]["name"])
        self.assertIsNotNone(res.data["site"]["coordinates"])

    def test_cannot_create_site_when_unauthenticated(self):
        self.client.post(reverse("auth:logout"))
        res = self.client.post(
            reverse("sites:create"), test_site_credentials, format="json"
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, res.status_code)

    def test_cannot_create_site_with_invalid_postcode(self):
        site = {**test_site_credentials, "postcode": "123456"}

        res = self.client.post(reverse("sites:create"), site, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_cannot_create_site_without_postcode(self):
        site = {"name": "test_site"}
        res = self.client.post(reverse("sites:create"), site, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_should_get_one_site(self):
        site_1 = test_site_credentials
        res = self.client.post(reverse("sites:create"), site_1, format="json")
        site = res.data["site"]

        res = self.client.get(reverse("sites:get", args=[site["id"]]), format="json")
        self.assertEqual(status.HTTP_200_OK, res.status_code)

    def test_list_sites(self):
        site_1 = {"name": "test_site_1", "postcode": "M14 6UF"}
        site_2 = test_site_credentials

        self.client.post(reverse("sites:create"), site_1, format="json")
        self.client.post(reverse("sites:create"), site_2, format="json")

        res = self.client.get(reverse("sites:list"), format="json")

        # print("RES:", pprint(vars(res)))
        self.assertEqual(2, Site.objects.count())
        self.assertEqual(2, len(res.data["sites"]))

    def test_update_site(self):
        res = self.client.post(
            reverse("sites:create"), test_site_credentials, format="json"
        )

        updated_fields = {"postcode": "M14 6UF"}

        first_site = res.data["site"]

        res = self.client.patch(
            f"/sites/{first_site['id']}/update",
            updated_fields,
            format="json",
        )

        updated_site = res.data["site"]

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(updated_site["postcode"], updated_fields["postcode"])
        self.assertNotEqual(updated_site["postcode"], first_site["postcode"])

    def test_delete_site(self):
        res = self.client.post(
            reverse("sites:create"), test_site_credentials, format="json"
        )

        self.assertEqual(1, Site.objects.count())

        first_site = res.data["site"]

        res = self.client.delete(
            f"/sites/{first_site['id']}/delete",
            format="json",
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
        self.assertEqual(0, Site.objects.count())
