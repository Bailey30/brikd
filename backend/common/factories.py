import factory
from django.db.models.signals import post_save

from common.models import BaseUser


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:  # pyright: ignore
        model = BaseUser

    email = factory.declarations.LazyAttribute(lambda n: "email%d@email.com" % n)
    password = factory.django.Password("password")
    is_active = True
    is_admin = False
