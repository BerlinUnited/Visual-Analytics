from rest_framework import serializers
from .models import CognitionFrame, FrameFilter


# TODO add serializer for all the generic cognition models
class CognitionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CognitionFrame
        fields = "__all__"


class FrameFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameFilter
        fields = ["log", "frames","name"]

    def create(self, validated_data):
        user = self.context["request"].user

        # Using update_or_create instead of create
        instance, created = FrameFilter.objects.update_or_create(
            log=validated_data["log"],
            name = validated_data["name"],
            user=user,
            defaults={"frames": validated_data["frames"]},
        )
        return instance
