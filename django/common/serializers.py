from rest_framework import serializers
from . import models


class LogSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField()
    game_name = serializers.ReadOnlyField()

    class Meta:
        model = models.Log
        # we have to list all the fields here since we want to add game_id and experiment id here to __all__
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()

        if "event_name" not in fields:
            fields["event_name"] = serializers.ReadOnlyField()
        if "game_name" not in fields:
            fields["game_name"] = serializers.ReadOnlyField()
        return fields

    def validate(self, data):
        # Ensure either game_id or experiment_id is provided, but not both, only check on creation
        if self.context.get("request").method == "POST":
            game_id = data.get("game")
            experiment_id = data.get("experiment")
            if not game_id and not experiment_id:
                raise serializers.ValidationError(
                    "Either game or experiment is required."
                )
            if game_id and experiment_id:
                raise serializers.ValidationError(
                    "Only one of game or experiment is allowed."
                )

        return data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(read_only=True)

    class Meta:
        model = models.Game
        fields = "__all__"


class ExperimentSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(read_only=True)

    class Meta:
        model = models.Experiment
        fields = "__all__"


class LogStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogStatus
        fields = "__all__"


class VideoRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoRecording
        fields = "__all__"

    def validate(self, data):
        # Ensure either game_id or experiment_id is provided, but not both, only check on creation
        if self.context.get("request").method == "POST":
            game_id = data.get("game")
            experiment_id = data.get("experiment")
            if not game_id and not experiment_id:
                raise serializers.ValidationError(
                    "Either game or experiment is required."
                )
            if game_id and experiment_id:
                raise serializers.ValidationError(
                    "Only one of game or experiment is allowed."
                )

        return data
