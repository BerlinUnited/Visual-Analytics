from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        # we have to list all the fields here since we want to add game_id and experiment id here to __all__
        fields = '__all__'

    def validate(self, data):
        # Ensure either game_id or experiment_id is provided, but not both
        game_id = data.get('log_game')
        experiment_id = data.get('log_experiment')

        if not game_id and not experiment_id:
            raise serializers.ValidationError("Either log_game or log_experiment is required.")
        if game_id and experiment_id:
            raise serializers.ValidationError("Only one of log_game or log_experiment is allowed.")

        return data

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(read_only=True)
    class Meta:
        model = models.Game
        fields = '__all__'

class ExperimentSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(read_only=True)
    class Meta:
        model = models.Experiment
        fields = '__all__'

class LogStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogStatus
        fields = '__all__'

