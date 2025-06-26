from common.service_utils import update_model
from common.utils import get_postcode_coordinates
from companies.models import Company
from sites.models import Site

from django.contrib.gis.geos import Point
from django.db.models import QuerySet


class SiteService:
    def create(self, name: str, postcode: str, company: Company) -> Site:
        coordinates = get_postcode_coordinates(postcode)

        site = Site.objects.create(
            name=name,
            postcode=postcode,
            company=company,
            coordinates=Point(coordinates["longitude"], coordinates["latitude"]),
        )
        return site

    def get(self, id: str) -> Site:
        site = Site.objects.get(id=id)
        return site

    def list(self) -> QuerySet[Site]:
        companys = Site.objects.all()
        return companys

    def update(self, site: Site, data: dict) -> Site:
        updated_site, _ = update_model(site, data)
        return updated_site

    def delete(self, site: Site) -> None:
        site.delete()
