from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render
from drf_yasg.utils import APIView, swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.views import BaseAuthenticatedView
from favourites.exceptions import AlreadyFavouritedError
from favourites.serializers import FavouriteInputSerializer, FavouriteOutputSerializer
from favourites.services import FavouriteService
from jobs.models import Job
from favourites.swagger import (
    create_favourite_view_schema,
    delete_favourite_view_schema,
    list_favourite_view_schema,
)


class ListFavouritesView(BaseAuthenticatedView):
    @swagger_auto_schema(**list_favourite_view_schema)
    def get(self, request) -> Response:
        favourites = FavouriteService().list(request.user)

        return Response(
            status=status.HTTP_200_OK,
            data=FavouriteOutputSerializer(favourites, many=True).data,
        )


class CreateFavouriteView(BaseAuthenticatedView):
    @swagger_auto_schema(**create_favourite_view_schema)
    def post(self, request) -> Response:
        serializer = FavouriteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job_id = serializer.validated_data["job_id"]

        try:
            FavouriteService().create(job_id, request.user)
        except Job.DoesNotExist:
            raise NotFound("Job with this ID does not exist.")
        except IntegrityError:
            raise AlreadyFavouritedError()

        return Response(status=status.HTTP_201_CREATED)


class DeleteFavouriteView(BaseAuthenticatedView):
    @swagger_auto_schema(**delete_favourite_view_schema)
    def delete(self, request) -> Response:
        serializer = FavouriteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job_id = serializer.validated_data["job_id"]

        try:
            FavouriteService().delete(job_id, request.user)
        except ObjectDoesNotExist as e:
            raise NotFound(f"{e}")

        return Response(status=status.HTTP_204_NO_CONTENT)
