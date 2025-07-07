from django.contrib.gis.geos.geometry import GEOSGeometry
from common.service_utils import update_model
from common.utils import get_postcode_coordinates
from companies.services import CompanyService
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import (
    Distance,
)  # For DB distance annotation
from jobs.filters import JobFilter
from jobs.models import Job
from common.models import BaseUser
from django.conf import settings
from django.db.models import QuerySet

from sites.services import SiteService
from users.models import User
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

    def list(self, request_user, params) -> QuerySet[Job]:
        limit = params.get("limit", settings.PAGINATION["default_limit"])

        jobs = Job.objects.all()[: int(limit)]

        # TODO: create one filtering service based off of query parameters

        try:
            # If the request was made by a jobseeker, annotate the jobs with
            # the distance from their saved location.
            # TODO: handle if they saved a location instead of a postcode.
            if (
                isinstance(request_user, BaseUser)
                and request_user.account_type == "jobseeker"
            ):
                user = UserService().get(request_user.id)  # pyright: ignore
                coordinates = get_postcode_coordinates(user.search_postcode)
                point = self.create_gis_point(coordinates)

                jobs = jobs.annotate(distance=Distance("site__coordinates", point))
        except Exception as e:
            raise e

        return jobs

    def list_within_radius(self, radius, coordinates):
        # TODO: make generic filtering service that only does this if radius and postcode params are present.

        point = self.create_gis_point(coordinates)

        jobs = (
            Job.objects.annotate(distance=Distance("site__coordinates", point))
            .filter(site__coordinates__distance_lte=(point, D(mi=radius)))
            .order_by("distance")
            .order_by("created_at")
        )

        return jobs

    def filter(self, params, request) -> QuerySet[Job]:
        jobs = Job.objects.all()
        filtered_jobs = JobFilter(params, jobs, request=request).qs
        return filtered_jobs

    def update(self, job: Job, data: dict) -> Job:
        updated_job, _ = update_model(job, data)
        return updated_job

    def delete(self, job: Job) -> None:
        job.delete()

    def create_gis_point(self, coordinates) -> GEOSGeometry:
        return GEOSGeometry(
            f"POINT ({coordinates['longitude']} {coordinates['latitude']})", srid=4326
        )
