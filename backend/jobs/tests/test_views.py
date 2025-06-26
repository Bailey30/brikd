from pprint import pprint
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from jobs.models import Job

from common.test_utils import (
    create_test_company,
    create_test_site,
    test_job_details,
    test_company_credentials,
)


class TestJobViews(APITestCase):
    def setUp(self):
        self.company = create_test_company()

        self.client.post(reverse("auth:token_obtain_pair"), test_company_credentials)

    def test_should_list_no_jobs(self):
        res = self.client.get(reverse("jobs:list"), format="json")
        self.assertEqual(0, len(res.data["jobs"]))

    def test_should_get_one_job(self):
        company = self.company
        site = create_test_site(company=company)

        job = {**test_job_details, "site_id": site.id, "company_id": company.id}

        res = self.client.post(reverse("jobs:create"), job, format="json")

        created_job = res.data["job"]

        res = self.client.get(reverse("jobs:get", args=[created_job["id"]]))

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(res.data["job"]["id"], created_job["id"])
        self.assertIn("distance", created_job)

    def test_should_create_job(self):
        company = self.company
        site = create_test_site(company=company)

        job = {**test_job_details, "site_id": site.id, "company_id": company.id}

        res = self.client.post(reverse("jobs:create"), job, format="json")

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

    def test_should_update_job(self):
        company = self.company
        site = create_test_site(company=company)

        job = {**test_job_details, "site_id": site.id, "company_id": company.id}

        create_res = self.client.post(reverse("jobs:create"), job, format="json")
        created_job = create_res.data["job"]

        updated_fields = {"title": "new_title", "description": "new_description"}

        update_res = self.client.patch(
            reverse("jobs:update", args=[created_job["id"]]),
            updated_fields,
            format="json",
        )

        updated_job = update_res.data["job"]

        self.assertEqual(status.HTTP_200_OK, update_res.status_code)
        self.assertNotEqual(updated_job["title"], job["title"])
        self.assertEqual(created_job["id"], updated_job["id"])
        self.assertEqual(updated_job["title"], updated_fields["title"])
        self.assertEqual(updated_job["description"], updated_fields["description"])

    def test_should_delete_job(self):
        company = self.company
        site = create_test_site(company=company)

        job = {**test_job_details, "site_id": site.id, "company_id": company.id}

        create_res = self.client.post(reverse("jobs:create"), job, format="json")

        self.assertEqual(1, Job.objects.count())

        created_job = create_res.data["job"]

        res = self.client.post(
            reverse("jobs:delete", args=[created_job["id"]]),
            format="json",
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
        self.assertEqual(0, Job.objects.count())

    def test_should_get_jobs_within_radius(self):
        company = self.company
        site_1 = create_test_site(company=company)
        site_2 = create_test_site(company=company, postcode="M15 5Ab")

        job_1 = {**test_job_details, "site_id": site_1.id, "company_id": company.id}
        job_2 = {**test_job_details, "site_id": site_2.id, "company_id": company.id}

        self.client.post(reverse("jobs:create"), job_1, format="json")
        self.client.post(reverse("jobs:create"), job_2, format="json")

        res = self.client.get(
            reverse("jobs:filter", query=[("postcode", "M146UF"), ("radius", 10)])
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(1, len(res.data["jobs"]))
