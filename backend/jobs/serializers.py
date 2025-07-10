from sites.views import SiteDetailView
from rest_framework import serializers
from jobs.models import Job


class JobOutputSerializer(serializers.ModelSerializer):
    site = SiteDetailView().OutputSerializer()

    class Meta:  # pyright: ignore
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "hourly_rate",
            "daily_rate",
            "site",
        ]


class JobListOutputSerializer(serializers.ModelSerializer):
    site = SiteDetailView().OutputSerializer()
    distance = serializers.CharField(required=False)

    class Meta:  # pyright: ignore
        ref_name = "JobListOutputSerializer"
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "hourly_rate",
            "daily_rate",
            "site",
            "distance",
        ]


class CreateJobInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    hourly_rate = serializers.IntegerField(required=False)
    daily_rate = serializers.IntegerField(required=False)
    company_id = serializers.CharField()
    site_id = serializers.CharField()


class UpdateJobInputSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    hourly_rate = serializers.IntegerField(required=False)
    daily_rate = serializers.IntegerField(required=False)
    company_id = serializers.CharField(required=False)
    site_id = serializers.CharField(required=False)
