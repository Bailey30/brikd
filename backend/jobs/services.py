from django.contrib.gis.geos import Point
from django.contrib.gis.geos.geometry import GEOSGeometry
from requests import request
from rest_framework.exceptions import APIException
from common.service_utils import update_model
from common.utils import get_postcode_coordinates
from companies.services import CompanyService
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import (
    Distance,
)  # For DB distance annotation
from jobs.models import Job

from django.db.models import QuerySet

from sites.services import SiteService
from users.services import UserService


class JobService:
    def create(
        self,
        title: str,
        description: str,
        company_id: str,
        site_id: str,
        hourly_rate=None,
        daily_rate=None,
    ) -> Job:
        site = SiteService().get(site_id)
        company = CompanyService().get(company_id)
        job = Job.objects.create(
            title=title,
            description=description,
            hourly_rate=hourly_rate,
            daily_rate=daily_rate,
            site=site,
            company=company,
        )
        return job

    def get(self, id: str) -> Job:
        # TODO: annotate jobs with distance to users saved location.
        job = Job.objects.get(id=id)
        return job

    def list(self, request_user) -> QuerySet[Job]:
        jobs = Job.objects.all()

        try:
            # If the request was made by a jobseeker, annotate the jobs with the distance from their saved location.
            # TODO: handle if they saved a location instead of a postcode.
            if (
                hasattr(request_user, "account_type")
                and request_user.account_type == "jobseeker"
            ):
                print("User is jobseeker to annotating with distance")
                user = UserService().get(request_user.id)
                print(user.search_postcode)
                coordinates = get_postcode_coordinates(user.search_postcode)
                point = self.create_gis_point(coordinates)

                jobs = jobs.annotate(distance=Distance("site__coordinates", point))
                print("jobs query", jobs.query)
        except Exception as e:
            raise e

        return jobs

    def list_within_radius(self, radius, coordinates):
        point = self.create_gis_point(coordinates)

        jobs = (
            Job.objects.annotate(distance=Distance("site__coordinates", point))
            .filter(site__coordinates__distance_lte=(point, D(mi=radius)))
            .order_by("distance")
        )

        return jobs

    def update(self, job: Job, data: dict) -> Job:
        updated_job, _ = update_model(job, data)
        return updated_job

    def delete(self, job: Job) -> None:
        job.delete()

    def create_gis_point(self, coordinates) -> GEOSGeometry:
        return GEOSGeometry(
            f"POINT ({coordinates['longitude']} {coordinates['latitude']})", srid=4326
        )
