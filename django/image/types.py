from graphene_django import DjangoObjectType
from .models import NaoImage


class ImageType(DjangoObjectType):
    class Meta:
        model = NaoImage
        fields = "__all__"
