from graphene_django import DjangoObjectType
from .models import (
    BehaviorOptionState,
    BehaviorFrameOption,
    XabslSymbolComplete,
    XabslSymbolSparse,
)


class BehaviorOptionStateType(DjangoObjectType):
    class Meta:
        model = BehaviorOptionState
        fields = "__all__"


class BehaviorFrameOptionType(DjangoObjectType):
    class Meta:
        model = BehaviorFrameOption
        fields = "__all__"


class XabslSymbolCompleteType(DjangoObjectType):
    class Meta:
        model = XabslSymbolComplete
        fields = "__all__"


class XabslSymbolSparseType(DjangoObjectType):
    class Meta:
        model = XabslSymbolSparse
        fields = "__all__"
