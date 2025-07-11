from rest_framework import serializers
from companies.serializers import CompanyDetailOutputSerializer
from companies.views import CompanyDetailView
from sites.models import Site
from common.utils import uk_postcode_validator


class SiteDetailOutputSerializer(serializers.ModelSerializer):
    company = CompanyDetailOutputSerializer()

    class Meta:  # pyright: ignore
        ref_name = "SiteDetailOutputSerializer"
        model = Site
        fields = ["id", "name", "postcode", "company", "coordinates"]
        depth = 1

    def to_representation(self, model):  # pyright: ignore
        values = super().to_representation(model)
        values["coordinates"] = {
            "longitude": model.coordinates[0],
            "latitude": model.coordinates[1],
        }
        return values


class CreateSiteInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    postcode = serializers.CharField(validators=[uk_postcode_validator])


class UpdateSiteInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    postcode = serializers.CharField(required=False, validators=[uk_postcode_validator])
