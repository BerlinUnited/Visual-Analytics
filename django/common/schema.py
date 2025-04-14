import graphene

from .types import EventType, GameType, LogType, LogStatusType
from .models import Event, Game, Log, LogStatus
from .serializers import EventSerializer
from graphene_django.rest_framework.mutation import SerializerMutation
from core.generic_filter import GenericFilterInput, apply_generic_filters


class CreateEvent(SerializerMutation):
    class Meta:
        serializer_class = EventSerializer

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # Extract the unique field (e.g., 'name') from the input
        name = input.get("name")

        # Use get_or_create to fetch or create the event
        event, created = Event.objects.get_or_create(name=name, defaults=input)

        # Return the event instance
        return event


class Query(graphene.ObjectType):
    # extra argument for each Type is a list of Filter Type so we can filter for multiple fields
    events = graphene.List(EventType, filters=graphene.List(GenericFilterInput))
    games = graphene.List(GameType, filters=graphene.List(GenericFilterInput))
    logs = graphene.List(LogType, filters=graphene.List(GenericFilterInput))
    logstatus = graphene.List(LogStatusType, filters=graphene.List(GenericFilterInput))

    def resolve_events(self, info, filters=None):
        queryset = Event.objects.all()
        return apply_generic_filters(Event, queryset, filters)

    def resolve_games(self, info, filters=None):
        queryset = Game.objects.all()
        return apply_generic_filters(Game, queryset, filters)

    def resolve_logs(self, info, filters=None):
        queryset = Log.objects.all()
        return apply_generic_filters(Log, queryset, filters)

    def resolve_logstatus(self, info, filters=None):
        queryset = LogStatus.objects.all()
        return apply_generic_filters(LogStatus, queryset, filters)


class Mutation(graphene.ObjectType):
    bla = CreateEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
