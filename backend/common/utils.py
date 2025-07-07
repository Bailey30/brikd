import requests
from rest_framework.exceptions import ValidationError

from django.contrib.gis.geos.geometry import GEOSGeometry


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
