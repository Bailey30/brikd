import factory

from common.factories import BaseUserFactory
from companies.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:  # pyright: ignore
        model = Company

    name = factory.declarations.Sequence(lambda n: "company%d" % n)

    @factory.helpers.lazy_attribute
    def profile(self):
        email = f"{self.name}@email.com"
        return BaseUserFactory(email=email, account_type="company")
