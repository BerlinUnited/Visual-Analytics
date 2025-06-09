from rest_framework import serializers
from . import models
from cognition.serializers import CognitionFrameSerializer


class BehaviorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorOption
        fields = "__all__"


class BehaviorOptionsStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorOptionState
        fields = "__all__"


class BehaviorFrameOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorFrameOption
        fields = "__all__"


class BehaviorFrameOptionCustomSerializer(serializers.ModelSerializer):
    # those lines are really important otherwise you cant return the fields here
    # option_name = serializers.CharField(source='options_id.option_name')  # Gets option_name from BehaviorOption
    # state_name = serializers.CharField(source='active_state.name')        # Gets name from BehaviorOptionState
    # frame = serializers.IntegerField()  # frame from BehaviorFrameOption
    frame = CognitionFrameSerializer(read_only=True)

    def to_representation(self, instance):
        # Get the serialized frame data (skips the outer "frame" wrapper)
        return self.fields["frame"].to_representation(instance.frame)

    class Meta:
        model = models.BehaviorFrameOption
        fields = ["frame"]


class XabslSymbolCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.XabslSymbolComplete
        fields = "__all__"


class XabslSymbolSparseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.XabslSymbolSparse
        fields = "__all__"
