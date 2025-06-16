from rest_framework.response import Response
from typing import cast


def res_type(request):
    return cast(Response, request)
