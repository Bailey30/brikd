from django_filters import rest_framework as filters

from jobs.models import Job
from common.utils import get_postcode_coordinates, create_gis_point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D


class JobFilter(filters.FilterSet):
    distance = filters.CharFilter(method="filter_distance")
    sort = filters.OrderingFilter(
        # Map model fields to custom param names
        fields={
            "created_at": "newest",
            "-created_at": "oldest",
            "hourly_rate": "hourly_rate_lowest",
            "-hourly_rate": "hourly_rate_highest",
            "distance": "distance_closest",
            "-distance": "distance_furthest",
        }
    )

    class Meta:
        model = Job
        fields = ["id"]

    def filter_distance(self, queryset, _, distance):
        if self.request is None:
            return queryset

        params = self.request.GET
        postcode = params.get("postcode", None)

        if postcode is None:
            return queryset

        coordinates = get_postcode_coordinates(postcode)
        point = create_gis_point(coordinates)

        mile_converstion_factor = 0.00062137

        jobs = (
            queryset.annotate(
                distance=Distance("site__coordinates", point) * mile_converstion_factor
            )
            .filter(site__coordinates__distance_lte=(point, D(mi=distance)))
            .order_by("distance", "created_at")
        )

        return jobs
