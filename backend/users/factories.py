import factory
from common.factories import BaseUserFactory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:  # pyright: ignore
        model = User

    name = factory.declarations.Sequence(lambda n: "jobseeker%d" % n)
    search_postcode = "M14 6UF"

    @factory.helpers.lazy_attribute
    def profile(self):
        email = f"{self.name}@email.com"
        return BaseUserFactory(email=email, account_type="jobseeker")
