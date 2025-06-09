from rest_framework import serializers
from .models import (
    CognitionFrame,
    FrameFilter,
    AudioData,
    BallModel,
    BallCandidates,
    BallCandidatesTop,
    CameraMatrix,
    CameraMatrixTop,
    OdometryData,
    FieldPercept,
    FieldPerceptTop,
    GoalPercept,
    GoalPerceptTop,
    MultiBallPercept,
    RansacCirclePercept2018,
    RansacLinePercept,
    RobotInfo,
    ShortLinePercept,
    ScanLineEdgelPercept,
    ScanLineEdgelPerceptTop,
    TeamMessageDecision,
    Teamstate,
    WhistlePercept,
)


class CognitionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CognitionFrame
        fields = "__all__"


class FrameFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameFilter
        fields = ["log", "frames", "name"]

    def create(self, validated_data):
        user = self.context["request"].user

        # Using update_or_create instead of create
        instance, created = FrameFilter.objects.update_or_create(
            log=validated_data["log"],
            name=validated_data["name"],
            user=user,
            defaults={"frames": validated_data["frames"]},
        )
        return instance


class AudioDataSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = AudioData
        fields = "__all__"


class BallModelSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = BallModel
        fields = "__all__"


class BallCandidatesSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = BallCandidates
        fields = "__all__"


class BallCandidatesTopSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = BallCandidatesTop
        fields = "__all__"


class CameraMatrixSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = CameraMatrix
        fields = "__all__"


class CameraMatrixTopSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = CameraMatrixTop
        fields = "__all__"


class OdometryDataSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = OdometryData
        fields = "__all__"


class FieldPerceptSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = FieldPercept
        fields = "__all__"


class FieldPerceptTopSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = FieldPerceptTop
        fields = "__all__"


class GoalPerceptSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = GoalPercept
        fields = "__all__"


class GoalPerceptTopSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = GoalPerceptTop
        fields = "__all__"


class MultiBallPerceptSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = MultiBallPercept
        fields = "__all__"


class RansacCirclePercept2018Serializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = RansacCirclePercept2018
        fields = "__all__"


class RansacLinePerceptSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = RansacLinePercept
        fields = "__all__"


class RobotInfoSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = RobotInfo
        fields = "__all__"


class ShortLinePerceptSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = ShortLinePercept
        fields = "__all__"


class ScanLineEdgelPerceptSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = ScanLineEdgelPercept
        fields = "__all__"


class ScanLineEdgelPerceptTopSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = ScanLineEdgelPerceptTop
        fields = "__all__"


class TeamMessageDecisionSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = TeamMessageDecision
        fields = "__all__"


class TeamstateSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = Teamstate
        fields = "__all__"


class WhistlePerceptSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = WhistlePercept
        fields = "__all__"
