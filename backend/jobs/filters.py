from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters

from jobs.models import Job
from common.utils import (
    annotate_queryset_with_distance,
    get_postcode_coordinates,
    create_gis_point,
)
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from jobs.utils import JobFilterParams


class JobFilter:
    is_annotated: bool = False

    def __init__(self, jobs, params) -> None:
        self.jobs: QuerySet = jobs
        self.params: JobFilterParams = params

    def filter(self):
        distance = self.params.get("distance")
        postcode = self.params.get("postcode")
        company_id = self.params.get("company_id")

        jobs = self.jobs

        if postcode and not self.is_annotated:
            jobs = annotate_queryset_with_distance(jobs, postcode)

        if distance and postcode:
            jobs = self.filter_by_distance(jobs, postcode, distance)

        if company_id:
            jobs = self.filter_by_company(jobs, company_id)

        self.jobs = jobs

        return self

    def filter_by_distance(self, jobs, postcode, distance) -> QuerySet[Job]:
        point = create_gis_point(get_postcode_coordinates(postcode))
        return jobs.filter(site__coordinates__distance_lte=(point, D(mi=distance)))

    def filter_by_company(self, jobs, company_id) -> QuerySet[Job]:
        return jobs.filter(company_id=company_id)

    def sort(self):
        sort = self.params.get("sort")

        if sort is None:
            return self

        jobs = self.jobs

        # Only annotate the jobs if it is required, and hasnt been done already elsewhere.
        if not self.is_annotated and sort in ["distance_closest", "distance_furthest"]:
            jobs = annotate_queryset_with_distance(jobs, self.params.get("postcode"))

        sort_dict = {
            "distance_closest": "distance",
            "distance_furthest": "-distance",
            "newest": "created_at",
            "oldest": "-created_at",
            "hourly_rate_lowest": "hourly_rate",
            "hourly_rate_highest": "-hourly_rate",
        }

        jobs = jobs.order_by(sort_dict[sort])

        self.jobs = jobs

        return self

    def queryset(self):
        return self.jobs

    @staticmethod
    def validate_params(params):
        distance = params.get("distance")
        postcode = params.get("postcode")
        sort = params.get("sort")

        if (
            distance or sort in ["distance_closest", "distance_furthest"]
        ) and postcode is None:
            raise ValidationError(
                "Include postcode as a query parameter when ordering or filtering by distance."
            )


# Keep this just so i remember how it works.

# class JobFilter(filters.FilterSet):
#     distance = filters.CharFilter(method="filter_distance")
#     sort = filters.OrderingFilter(
#         # Map model fields to custom param names
#         fields={
#             "created_at": "newest",
#             "-created_at": "oldest",
#             "hourly_rate": "hourly_rate_lowest",
#             "-hourly_rate": "hourly_rate_highest",
#             "distance": "distance_closest",
#             "-distance": "distance_furthest",
#         }
#     )
#
#     class Meta:
#         model = Job
#         fields = ["id"]
#
#     def filter_distance(self, queryset, _, distance):
#         if self.request is None:
#             return queryset
#
#         params = self.request.GET
#         postcode = params.get("postcode", None)
#
#         if postcode is None:
#             return queryset
#
#         coordinates = get_postcode_coordinates(postcode)
#         point = create_gis_point(coordinates)
#
#         # mile_converstion_factor = 0.00062137
#
#         # Filtering by the distance using the
#         jobs = queryset.filter(
#             site__coordinates__distance_lte=(point, D(mi=distance))
#         ).order_by("distance", "created_at")
#
#         return jobs
