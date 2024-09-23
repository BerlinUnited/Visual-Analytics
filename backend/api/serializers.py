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


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Annotation
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Logs
        fields = '__all__'

    def create(self, validated_data):
        # TODO figure out why this works
        instance, created = models.Logs.objects.get_or_create(
            game=validated_data.get('game'),
            player_number=validated_data.get('player_number'),
            head_number=validated_data.get('head_number'),
            log_path=validated_data.get('log_path'),
            defaults=validated_data
        )
        return instance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = '__all__'


class CognitionRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CognitionRepresentation
        fields = '__all__'


class MotionRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MotionRepresentation
        fields = '__all__'