from graphene_django import DjangoObjectType
from .models import Event, Game, Log, VideoRecording, Experiment, LogStatus


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"


class GameType(DjangoObjectType):
    class Meta:
        model = Game
        fields = "__all__"


class LogType(DjangoObjectType):
    class Meta:
        model = Log
        fields = "__all__"


class VideoRecordingType(DjangoObjectType):
    class Meta:
        model = VideoRecording
        fields = "__all__"


class ExperimentType(DjangoObjectType):
    class Meta:
        model = Experiment
        fields = "__all__"


class LogStatusType(DjangoObjectType):
    class Meta:
        model = LogStatus
        fields = "__all__"
