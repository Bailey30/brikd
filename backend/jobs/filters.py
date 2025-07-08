from django.db.models import QuerySet
from django_filters import rest_framework as filters

from jobs.models import Job
from common.utils import (
    annotate_queryset_with_distance,
    get_postcode_coordinates,
    create_gis_point,
)
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D


class CustomJobFilter:
    qs: QuerySet[Job]

    def __init__(self, params, jobs):
        sort = params.get("sort")
        distance = params.get("distance")
        postcode = params.get("postcode")

        if postcode:
            jobs = annotate_queryset_with_distance(jobs, postcode)

        # Distance filtering only allowed when postcode is provided.
        if distance:
            jobs = self.filter_by_distance(params, jobs)

        if sort:
            jobs = self.sort(params, jobs, bool(distance))

        self.qs = jobs

    def filter_by_distance(self, params, jobs):
        distance = params.get("distance")
        postcode = params.get("postcode")

        point = create_gis_point(get_postcode_coordinates(postcode))

        jobs = jobs.filter(site__coordinates__distance_lte=(point, D(mi=distance)))

        return jobs

    def sort(self, params, jobs, is_annotated):
        sort = params.get("sort")

        # Only annotate the jobs if it is required, and hasnt been done already elsewhere.
        if not is_annotated and sort in ["distance_closest", "distance_furthest"]:
            jobs = annotate_queryset_with_distance(jobs, params.get("postcode"))

        sort_dict = {
            "distance_closest": "distance",
            "distance_furthest": "-distance",
            "newest": "created_at",
            "oldest": "-created_at",
            "hourly_rate_lowest": "hourly_rate",
            "hourly_rate_highest": "-hourly_rate",
        }

        jobs = jobs.order_by(sort_dict[sort])

        return jobs


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
