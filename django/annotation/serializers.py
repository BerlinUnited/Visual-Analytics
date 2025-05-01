from rest_framework import serializers
from .models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    frame_number = serializers.CharField(read_only=True)

    class Meta:
        model = Annotation
        fields = "__all__"

    def get_color(self, obj):
        return Annotation.Classes.get_color(obj.class_name)