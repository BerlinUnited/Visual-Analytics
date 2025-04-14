from graphene_django import DjangoObjectType
from .models import MotionFrame


class MotionFrameType(DjangoObjectType):
    class Meta:
        model = MotionFrame
        fields = "__all__"


# FIXME find a way to dynamically deal with all the models that are the same
"""
class MotionRepresentationType(DjangoObjectType):
    class Meta:
        model = models.MotionRepresentation
        fields = "__all__"
"""
