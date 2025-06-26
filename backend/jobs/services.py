from django.contrib.gis.geos import Point
from django.contrib.gis.geos.geometry import GEOSGeometry
from common.service_utils import update_model
from companies.services import CompanyService
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import (
    Distance,
)  # For DB distance annotation
from jobs.models import Job

from django.db.models import QuerySet

from sites.services import SiteService


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

    def list(self) -> QuerySet[Job]:
        # TODO: annotate jobs with distance to users saved location.
        job = Job.objects.get(id=id)
        jobs = Job.objects.all()
        return jobs

    def list_within_radius(self, radius, coordinates):
        point = GEOSGeometry(
            f"POINT ({coordinates['longitude']} {coordinates['latitude']})", srid=4326
        )
        jobs = (
            Job.objects.annotate(distance=Distance("site__coordinates", point))
            .filter(site__coordinates__distance_lte=(point, D(mi=radius)))
            .order_by("distance")
        )
        print("jobs:", jobs)

        return jobs

    def update(self, job: Job, data: dict) -> Job:
        updated_job, _ = update_model(job, data)
        return updated_job

    def delete(self, job: Job) -> None:
        job.delete()
