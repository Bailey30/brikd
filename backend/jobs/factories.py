import factory

from companies.factories import CompanyFactory
from jobs.models import Job
from sites.factories import SiteFactory


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:  # pyright: ignore
        model = Job

    company = factory.declarations.SubFactory(CompanyFactory)
    site = factory.declarations.SubFactory(SiteFactory)
    title = factory.declarations.Sequence(lambda n: "site%d" % n)
    description = factory.declarations.Sequence(lambda n: "site%d" % n)
    hourly_rate = 1.00
    daily_Rate = None
