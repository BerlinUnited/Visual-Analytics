from rest_framework import serializers
from .models import MotionFrame, IMUData, FSRData, AccelerometerData, InertialSensorData, MotionStatus, MotorJointData, GyrometerData


class MotionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotionFrame
        fields = "__all__"


class IMUDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMUData
        fields = "__all__"


class FSRDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FSRData
        fields = "__all__"


class AccelerometerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccelerometerData
        fields = "__all__"


class InertialSensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InertialSensorData
        fields = "__all__"



class MotionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotionStatus
        fields = "__all__"


class MotorJointDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorJointData
        fields = "__all__"


class GyrometerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GyrometerData
        fields = "__all__"