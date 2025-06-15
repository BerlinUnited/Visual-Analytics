from django.contrib.auth import get_user_model
from user.models import Organization

import factory
from factory.django import DjangoModelFactory



class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("company")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    organization = factory.SubFactory(OrganizationFactory)
