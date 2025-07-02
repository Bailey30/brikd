import factory

from common.utils import get_postcode_coordinates
from companies.factories import CompanyFactory
from sites.models import Site

from django.contrib.gis.geos import Point


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:  # pyright: ignore
        model = Site

    name = factory.declarations.Sequence(lambda n: "site%d" % n)
    company = factory.declarations.SubFactory(CompanyFactory)
    postcode = "CR0 3RL"

    @factory.helpers.lazy_attribute
    def coordinates(self):
        coordinates = get_postcode_coordinates(self.postcode)
        return Point(coordinates["longitude"], coordinates["latitude"])
