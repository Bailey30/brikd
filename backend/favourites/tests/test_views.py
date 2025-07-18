from pprint import pprint
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from common.test_utils import test_user_credentials
from favourites.exceptions import AlreadyFavouritedError
from favourites.models import Favourite
from jobs.factories import JobFactory


class TestFavouritesViews(APITestCase):
    def test_should_create_favourite(self):
        jobseeker_client = APIClient()

        res = jobseeker_client.post(reverse("users:create"), test_user_credentials)
        res = jobseeker_client.post(
            reverse("auth:login"), test_user_credentials, format="json"
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)

        job = JobFactory()

        res = jobseeker_client.post(reverse("favourites:create"), {"job_id": job.id})

        self.assertEqual(1, Favourite.objects.count())

        res = jobseeker_client.post(reverse("favourites:create"), {"job_id": job.id})

        self.assertEqual(status.HTTP_409_CONFLICT, res.status_code)
        self.assertEqual(
            AlreadyFavouritedError.default_detail, res.data["errors"][0]["detail"]
        )

    def test_should_delete_favourite(self):
        jobseeker_client = APIClient()

        res = jobseeker_client.post(reverse("users:create"), test_user_credentials)
        res = jobseeker_client.post(
            reverse("auth:login"), test_user_credentials, format="json"
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)

        job = JobFactory()

        res = jobseeker_client.post(reverse("favourites:create"), {"job_id": job.id})

        self.assertEqual(1, Favourite.objects.count())

        res = jobseeker_client.delete(reverse("favourites:delete"), {"job_id": job.id})

        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
        self.assertEqual(0, Favourite.objects.count())

        res = jobseeker_client.delete(reverse("favourites:delete"), {"job_id": job.id})

        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)
        self.assertEqual(
            "Favourite matching query does not exist.", res.data["errors"][0]["detail"]
        )

        job_id = job.id
        job.delete()

        res = jobseeker_client.delete(reverse("favourites:delete"), {"job_id": job_id})

        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)
        self.assertEqual(
            "Job matching query does not exist.", res.data["errors"][0]["detail"]
        )

    def test_should_list_user_favourites(self):
        jobseeker_client = APIClient()

        res = jobseeker_client.post(reverse("users:create"), test_user_credentials)
        res = jobseeker_client.post(
            reverse("auth:login"), test_user_credentials, format="json"
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)

        job_1 = JobFactory()
        job_2 = JobFactory()
        job_3 = JobFactory()

        res = jobseeker_client.post(reverse("favourites:create"), {"job_id": job_1.id})
        res = jobseeker_client.post(reverse("favourites:create"), {"job_id": job_2.id})
        res = jobseeker_client.post(reverse("favourites:create"), {"job_id": job_3.id})

        self.assertEqual(3, Favourite.objects.count())

        res = jobseeker_client.get(reverse("favourites:list"), format="json")

        self.assertEqual(200, res.status_code)
        self.assertEqual(3, len(res.data))
