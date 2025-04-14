from graphene_django import DjangoObjectType
from .models import CognitionFrame, FrameFilter


class CognitionFrameType(DjangoObjectType):
    class Meta:
        model = CognitionFrame
        fields = "__all__"


class FrameFilterType(DjangoObjectType):
    class Meta:
        model = FrameFilter
        fields = "__all__"


# FIXME find a way to dynamically deal with all the models that are the same
"""
class CognitionRepresentationType(DjangoObjectType):
    class Meta:
        model = models.CognitionRepresentation
        fields = "__all__"
"""
