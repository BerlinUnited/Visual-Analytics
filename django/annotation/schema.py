import graphene
from image.models import NaoImage
from .models import Annotation
from .types import AnnotationType
from .serializers import AnnotationSerializer
from graphene_django.rest_framework.mutation import SerializerMutation
from core.generic_filter import GenericFilterInput, apply_generic_filters


class CreateAnnotation(SerializerMutation):
    class Meta:
        serializer_class = AnnotationSerializer

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        image_id = input.get("image")
        # remove image from defaults because this overwrites the retrieved image_instance otherwise
        input.pop("image")
        # Fetch the Image instance using the provided ID
        try:
            image_instance = NaoImage.objects.get(id=image_id)
        except NaoImage.DoesNotExist:
            raise Exception("Image with id %s does not exist" % image_id)

        # Use the Image instance in get_or_create
        annotation, created = Annotation.objects.get_or_create(
            image=image_instance, defaults=input
        )
        return annotation


class UpdateAnnotation(SerializerMutation):
    class Meta:
        serializer_class = AnnotationSerializer

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        image_id = input.get("image")
        # remove image from defaults because this overwrites the retrieved image_instance otherwise
        input.pop("image")
        # Fetch the Image instance using the provided ID
        try:
            image_instance = NaoImage.objects.get(id=image_id)
        except NaoImage.DoesNotExist:
            raise Exception(f"Image with id {image_id} does not exist")

        try:
            annotation_instance = Annotation.objects.get(image=image_instance)
        except Annotation.DoesNotExist:
            raise Exception(f"Annotation for image with id {image_id} does not exist")

        annotation_instance.annotation = input.get("annotation")
        annotation_instance.save()
        return annotation_instance


class Query(graphene.ObjectType):
    annotations = graphene.List(
        AnnotationType, filters=graphene.List(GenericFilterInput)
    )

    def resolve_annotations(self, info, filters=None):
        queryset = Annotation.objects.all()
        return apply_generic_filters(Annotation, queryset, filters)


class Mutation(graphene.ObjectType):
    CreateAnnotation = CreateAnnotation.Field()
    UpdateAnnotation = UpdateAnnotation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
