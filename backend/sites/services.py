from companies.models import Company
from sites.models import Site

from django.db.models import QuerySet


class SiteService:
    def create(self, name: str, postcode: str, company: Company) -> Site:
        site = Site.objects.create(name=name, postcode=postcode, company=company)
        return site

    def get(self, id: int) -> Site:
        site = Site.objects.get(id=id)
        return site

    def list(self) -> QuerySet[Site]:
        companys = Site.objects.all()
        return companys
