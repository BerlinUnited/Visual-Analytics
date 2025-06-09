from django.contrib.auth import get_user_model

import factory
from factory.django import DjangoModelFactory
from rest_framework.authtoken.models import Token
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')