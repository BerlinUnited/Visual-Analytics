from rest_framework import serializers
from .models import Annotation, AnnotationClass


class AnnotationClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationClass
        fields = "__all__"


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = "__all__"
