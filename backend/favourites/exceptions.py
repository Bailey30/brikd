from rest_framework.exceptions import APIException


class AlreadyFavouritedError(APIException):
    status_code = 409
    default_detail = "Job is already favourited by this user."
    default_code = "already_favourited"
