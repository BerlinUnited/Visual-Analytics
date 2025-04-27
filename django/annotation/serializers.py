from rest_framework import serializers
from .models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()

    class Meta:
        model = Annotation
        fields = "__all__"

    def get_color(self, obj):
        return Annotation.Classes.get_color(obj.class_name)