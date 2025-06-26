import requests
from rest_framework.exceptions import ValidationError


def get_postcode_coordinates(postcode):
    response = requests.get(
        f"https://api.postcodes.io/postcodes/{postcode.replace(' ', '')}", postcode
    )
    data = response.json()

    if data["status"] != 200:
        raise ValidationError(data["error"])

    result = data["result"]

    return {"longitude": result["longitude"], "latitude": result["latitude"]}
