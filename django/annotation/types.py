from graphene_django import DjangoObjectType
from .models import Annotation


class AnnotationType(DjangoObjectType):
    class Meta:
        model = Annotation
        fields = "__all__"
