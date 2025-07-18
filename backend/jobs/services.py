from django.http.request import QueryDict
from common.models import BaseUser
from rest_framework.exceptions import ValidationError
from common.service_utils import update_model
from companies.services import CompanyService
from django.db.models import QuerySet
from sites.services import SiteService

from jobs.filters import JobFilter
from jobs.models import Job


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
        # TODO: annotate jobs with distance to users saved location or query param.
        job = Job.objects.get(id=id)
        return job

    def list(self, params) -> QuerySet[Job]:
        JobFilter.validate_params(params)

        jobs = Job.objects.all()

        filtered_jobs = JobFilter(jobs, params).filter().sort().queryset()

        return filtered_jobs

    def update(self, job: Job, data: dict) -> Job:
        updated_job, _ = update_model(job, data)
        return updated_job

    def delete(self, job: Job) -> None:
        job.delete()
