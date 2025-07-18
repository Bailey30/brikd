import re
from django.contrib.gis.db.models.functions import Distance
from django.db.models import QuerySet
import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.gis.geos.geometry import GEOSGeometry

from jobs.models import Job


def get_postcode_coordinates(postcode):
    response = requests.get(
        f"https://api.postcodes.io/postcodes/{postcode.replace(' ', '')}", postcode
    )
    data = response.json()

    if data["status"] != 200:
        raise ValidationError(data["error"] + " " + "Postcode: ", postcode)

    result = data["result"]

    return {"longitude": result["longitude"], "latitude": result["latitude"]}


def create_gis_point(coordinates) -> GEOSGeometry:
    return GEOSGeometry(
        f"POINT ({coordinates['longitude']} {coordinates['latitude']})", srid=4326
    )


def annotate_queryset_with_distance(queryset, postcode) -> QuerySet[Job]:
    coordinates = get_postcode_coordinates(postcode)
    point = create_gis_point(coordinates)

    mile_converstion_factor = 0.00062137

    jobs = queryset.annotate(
        distance=Distance("site__coordinates", point) * mile_converstion_factor
    )

    return jobs

def uk_postcode_validator(postcode):
    if re.match(r"^([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})$", postcode) is None:
        raise serializers.ValidationError("Invalid UK postcode.")

