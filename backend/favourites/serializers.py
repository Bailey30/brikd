from rest_framework import serializers

from favourites.models import Favourite
from jobs.serializers import JobOutputSerializer
from jobs.views import JobDetailView
from users.serializers import UserOutputSerializer


class FavouriteInputSerializer(serializers.Serializer):
    job_id = serializers.CharField(required=True)


class FavouriteOutputSerializer(serializers.Serializer):
    job = JobOutputSerializer()
