from django.contrib.auth.models import User
from rest_framework import serializers
from . import models
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Annotation
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'


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

class CognitionRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CognitionRepresentation
        fields = '__all__'


class MotionRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MotionRepresentation
        fields = '__all__'


class BehaviorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorOption
        fields = '__all__'


class BehaviorOptionsStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorOptionState
        fields = '__all__'

class BehaviorFrameOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorFrameOption
        fields = '__all__'

class BehaviorFrameOptionCustomSerializer(serializers.ModelSerializer):
    # those lines are really important otherwise you cant return the fields here
    #option_name = serializers.CharField(source='options_id.option_name')  # Gets option_name from BehaviorOption
    #state_name = serializers.CharField(source='active_state.name')        # Gets name from BehaviorOptionState
    frame = serializers.IntegerField()                                    # frame from BehaviorFrameOption
    def to_representation(self, data):
        return data.frame
    
    class Meta:
        model = models.BehaviorFrameOption
        fields = ['frame']

class XabslSymbolCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.XabslSymbolComplete
        fields = '__all__'

class XabslSymbolSparseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.XabslSymbolSparse
        fields = '__all__'

class LogStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogStatus
        fields = '__all__'

class FrameFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FrameFilter
        fields = ['log_id', 'frames']

    def create(self, validated_data):
        user = self.context['request'].user
        
        # Using update_or_create instead of create
        instance, created = models.FrameFilter.objects.update_or_create(
            log_id=validated_data['log_id'],
            user=user,
            defaults={
                'frames': validated_data['frames']
            }
        )
        return instance
    
class CognitionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CognitionFrame
        fields = '__all__'

class MotionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MotionFrame
        fields = '__all__'