from pprint import pprint

from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from companies.factories import CompanyFactory
from jobs.factories import JobFactory
from jobs.models import Job
from sites.factories import SiteFactory
from users.factories import UserFactory
from users.models import User

from common.test_utils import (
    create_test_company,
    create_test_site,
    test_job_details,
    test_company_credentials,
    test_user_credentials,
)


class TestJobViews(APITestCase):
    def setUp(self):
        """
        Create a company account and log it in so it can create jobs and sites for the tests.
        """

        self.company = create_test_company()

        self.client.post(reverse("auth:token_obtain_pair"), test_company_credentials)

    def test_should_list_no_jobs(self):
        res = self.client.get(reverse("jobs:list"), format="json")

        self.assertEqual(0, len(res.data["results"]))

    def test_should_get_one_job(self):
        company = self.company
        site = create_test_site(company=company)

        job = {**test_job_details, "site_id": site.id, "company_id": company.id}

        res = self.client.post(reverse("jobs:create"), job, format="json")

        created_job = res.data["job"]
        res = self.client.get(reverse("jobs:get", args=[created_job["id"]]))

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(res.data["job"]["id"], created_job["id"])

        res = self.client.get(reverse("jobs:get", args=[9999999999]))

        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)

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

        res = self.client.delete(
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
            reverse("jobs:list", query=[("postcode", "M146UF"), ("distance", 10)])
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(1, len(res.data["results"]))

    def test_should_list_jobs_with_correct_distance_value(self):
        company = CompanyFactory()
        company_client = APIClient()
        company_client.post(reverse("auth:token_obtain_pair"), test_company_credentials)

        site_1 = SiteFactory(company=company)
        site_2 = SiteFactory(company=company, postcode="M15 5Ab")

        JobFactory.create_batch(25, site=site_1, company=company)
        JobFactory.create_batch(25, site=site_2, company=company)

        self.assertEqual(50, Job.objects.count())

        res = company_client.get(reverse("jobs:list"), format="json")

        # Distance will not be in the properties of Job when listed by a company
        for job in res.data["results"]:
            self.assertNotIn("distance", job)

        # Create and log in a jobseeker account
        jobseeker_client = APIClient()
        res = jobseeker_client.post(
            reverse("users:create"), test_user_credentials, format="json"
        )
        jobseeker = UserFactory()
        res = jobseeker_client.post(
            reverse("auth:token_obtain_pair"), test_user_credentials
        )
        self.assertEqual(status.HTTP_200_OK, res.status_code)

        jobseeker = User.objects.get(profile_id=jobseeker.id)
        jobseeker_client.force_authenticate(user=jobseeker.profile)

        # Get the jobs as jobseeker
        res = jobseeker_client.get(
            reverse(
                "jobs:list",
                query=[("postcode", "M146UF")],
            )
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)

        for job in res.data["results"]:
            self.assertIn("distance", job)

    def test_should_paginate_correct_amount(self):
        company = CompanyFactory()
        company_client = APIClient()
        company_client.post(reverse("auth:token_obtain_pair"), test_company_credentials)

        site_1 = SiteFactory(company=company)

        JobFactory.create_batch(100, site=site_1, company=company)

        res = self.client.get(reverse("jobs:list"))

        self.assertEqual(settings.PAGINATION["default_limit"], res.data["limit"])
        self.assertEqual(100, len(res.data["results"]))

        res = self.client.get(reverse("jobs:list", query=[("limit", 25)]))

        self.assertEqual(25, res.data["limit"])
        self.assertEqual(25, len(res.data["results"]))

    def test_should_sort_and_filter_correcty_with_search_params(self):
        company = CompanyFactory()

        site_1 = SiteFactory(company=company, postcode="M1 1AE")
        site_2 = SiteFactory(company=company, postcode="M2 3HQ")
        site_3 = SiteFactory(company=company, postcode="M3 5GS")
        site_4 = SiteFactory(company=company, postcode="M4 6BB")
        site_5 = SiteFactory(company=company, postcode="M5 4WT")
        site_6 = SiteFactory(company=company, postcode="M6 7RT")
        site_7 = SiteFactory(company=company, postcode="SK1 1EB")
        site_8 = SiteFactory(company=company, postcode="WA1 4RW")
        site_9 = SiteFactory(company=company, postcode="OL1 3LG")
        site_10 = SiteFactory(company=company, postcode="L1 8JQ")

        JobFactory(site=site_1, company=company, hourly_rate=10)
        JobFactory(site=site_2, company=company, hourly_rate=12)
        JobFactory(site=site_3, company=company, hourly_rate=15)
        JobFactory(site=site_4, company=company, hourly_rate=9)
        JobFactory(site=site_5, company=company, hourly_rate=20)
        JobFactory(site=site_6, company=company, hourly_rate=8)
        JobFactory(site=site_7, company=company, hourly_rate=11)
        JobFactory(site=site_8, company=company, hourly_rate=14)
        JobFactory(site=site_9, company=company, hourly_rate=13)
        JobFactory(site=site_10, company=company, hourly_rate=7)

        # Should order jobs starting with highest hourly_rate first.
        res = self.client.get(
            reverse(
                "jobs:list",
                query=[
                    ("postcode", "M146UF"),
                    ("distance", 10),
                    ("sort", "hourly_rate_highest"),
                ],
            )
        )

        jobs = res.data["results"]

        for i in range(len(jobs) - 1):
            self.assertGreaterEqual(
                float(jobs[i]["hourly_rate"]), float(jobs[i + 1]["hourly_rate"])
            )

        self.assertEqual(200, res.status_code)

        self.assertEqual(8, len(jobs))

        # Should order jobs with closest first.
        res = self.client.get(
            reverse(
                "jobs:list",
                query=[
                    ("sort", "distance_closest"),
                    ("postcode", "M146UF"),
                    ("distance", 10),
                ],
            )
        )

        jobs = res.data["results"]
        for job in jobs:
            print(
                "title:",
                job["title"],
                "hourly_rate:",
                job["hourly_rate"],
                "distance:",
                job["distance"],
                "postcode:",
                job["site"]["postcode"],
            )

        for i in range(len(jobs) - 1):
            self.assertLessEqual(jobs[i]["distance"], jobs[i + 1]["distance"])

        # Should return error if including distance filtering or sorting without postcode
        res = self.client.get(
            reverse(
                "jobs:list",
                query=[
                    ("sort", "distance_closest"),
                ],
            )
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual(
            "Include postcode as a query parameter when ordering or filtering by distance.",
            res.data["errors"][0]["detail"],
        )

        # Should get jobs without any query params.
        res = self.client.get(reverse("jobs:list"))

        jobs = res.data["results"]

        self.assertEqual(10, len(jobs))
        for job in res.data["results"]:
            self.assertNotIn("distance", job)
