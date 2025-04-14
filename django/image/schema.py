import graphene
from .types import ImageType
from image.models import NaoImage
from core.generic_filter import GenericFilterInput, apply_generic_filters


class Query(graphene.ObjectType):
    images = graphene.List(ImageType, filters=graphene.List(GenericFilterInput))

    def resolve_images(self, info, filters=None):
        queryset = NaoImage.objects.all()
        return apply_generic_filters(NaoImage, queryset, filters)


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
