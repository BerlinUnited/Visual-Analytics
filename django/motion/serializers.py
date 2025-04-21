from rest_framework import serializers
from .models import MotionFrame, IMUData


class MotionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotionFrame
        fields = "__all__"


class IMUDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMUData
        fields = "__all__"