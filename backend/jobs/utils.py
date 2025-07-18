from dataclasses import dataclass
from typing import Optional

from django.http.request import QueryDict


@dataclass()
class JobFilterParams(QueryDict):
    """
    A QueryDict representing the potential query parameters for GET /jobs
    """

    sort: Optional[str] = None
    distance: Optional[str] = None
    postcode: Optional[str] = None
    limit: Optional[str] = None
    offset: Optional[str] = None
    company_id: Optional[str] = None

    def get(self, key: str, default=None) -> str | None:
        try:
            param = self.__dict__[key]
        except KeyError:
            return default
        if param == []:
            return default
        return param
