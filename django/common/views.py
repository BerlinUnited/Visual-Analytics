from rest_framework import generics, viewsets, status
from django.shortcuts import get_object_or_404
from . import serializers
from rest_framework.permissions import AllowAny
from . import models
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q, F
from django.db import connection
from psycopg2.extras import execute_values
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
)
from django.db import models as django_models
from django.template import loader
from utils.generic_filter import generic_filter
User = get_user_model()


@require_GET
def scalar_doc(request):
    template = loader.get_template("api/api_scalar.html")
    return HttpResponse(template.render())


@require_GET
def health_check(request):
    return JsonResponse({"message": "UP"}, status=200)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]


# we use tags to group endpoints and sort them by order in settings.py
@extend_schema(tags=["Events"])
@extend_schema_view(
    list=extend_schema(
        description="List all events",
        responses={200: serializers.EventSerializer(many=True)},
    )
)
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    @extend_schema(
        description="Create single or multiple events",
        request=serializers.EventSerializer(many=True),
        # Example data for test requests
        examples=[
            OpenApiExample(
                "Single Event Creation",
                value={"name": "Conference 2024", "date": "2024-12-25"},
                request_only=True,
                summary="Create one event",
                description="",
            ),
            OpenApiExample(
                "Bulk Event Creation",
                value=[
                    {"name": "Conference 2024", "date": "2024-12-25"},
                    {"name": "Workshop 2024", "date": "2024-12-26"},
                ],
                request_only=True,
                summary="Create multiple events",
            ),
        ],
        # displaying responses for single and bulk create but only response schema for single create
        responses={
            201: OpenApiResponse(
                # response=[
                #     inline_serializer(
                #         name='BulkEventResponse',
                #         fields={
                #             'created': s.IntegerField(),
                #             'existing': s.IntegerField(),
                #             'events': serializers.EventSerializer(many=True)
                #         }
                #     ),
                #     serializers.EventSerializer],
                response=serializers.EventSerializer,
                description="Response for single or bulk create",
                examples=[
                    OpenApiExample(
                        name="Response for bulk create",
                        value={
                            "created": 2,
                            "existing": 0,
                            "events": [
                                {"id": 1, "name": "Event 1", "date": "2024-12-23"},
                                {"id": 2, "name": "Event 2", "date": "2024-12-24"},
                            ],
                        },
                    ),
                    OpenApiExample(
                        name="Response for single create",
                        value={"id": 1, "name": "Event 1", "date": "2024-12-23"},
                    ),
                ],
            )
        },
    )
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)

        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data

        instance, created = models.Event.objects.get_or_create(
            name=validated_data.get("name"), defaults=validated_data
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing names
            existing_names = set(
                models.Event.objects.filter(
                    name__in=[item["name"] for item in validated_data]
                ).values_list("name", flat=True)
            )

            # Separate new and existing events
            new_events = []
            existing_events = []
            for item in validated_data:
                if item["name"] not in existing_names:
                    new_events.append(models.Event(**item))
                    existing_names.add(
                        item["name"]
                    )  # Add to set to catch duplicates within the input
                else:
                    existing_events.append(models.Event.objects.get(name=item["name"]))

            # Bulk create new events
            created_events = models.Event.objects.bulk_create(new_events)

        # Combine created and existing events
        all_events = created_events + existing_events

        # Serialize the results
        result_serializer = self.get_serializer(all_events, many=True)

        return Response(
            {
                "created": len(created_events),
                "existing": len(existing_events),
                "events": result_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer

    def get_queryset(self):
        event_id = self.request.query_params.get("event")

        queryset = models.Game.objects.select_related("event").annotate(
            event_name=F("event__name")
        )

        if event_id is not None:
            queryset = queryset.filter(event=event_id)

        return queryset

    def create(self, request, *args, **kwargs):
        row_tuple = [
            (
                request.data.get("event"),
                request.data.get("team1"),
                request.data.get("team2"),
                request.data.get("half"),
                request.data.get("is_testgame"),
                request.data.get("head_ref"),
                request.data.get("assistent_ref"),
                request.data.get("field"),
                request.data.get("start_time"),
                request.data.get("score"),
                request.data.get("comment"),
            )
        ]
        with connection.cursor() as cursor:
            query = """
            INSERT INTO common_game (event_id, team1, team2, half, is_testgame, head_ref, assistent_ref, field, start_time, score, comment)
            VALUES %s
            ON CONFLICT (event_id, start_time, half) DO NOTHING
            RETURNING id;
            """

            execute_values(cursor, query, row_tuple, page_size=1)
            result = cursor.fetchone()
            if result:
                serializer = self.get_serializer(models.Game.objects.get(id=result[0]))
                # If insert was successful, get the object
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If ON CONFLICT DO NOTHING prevented insert, get the existing object
                instance = models.Game.objects.get(
                    event_id=request.data.get("event"),
                    start_time=request.data.get("start_time"),
                    half=request.data.get("half"),
                )
                serializer = self.get_serializer(instance)

                return Response(serializer.data, status=status.HTTP_200_OK)


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = models.Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer

    def get_queryset(self):
        event_id = self.request.query_params.get("event")

        queryset = models.Experiment.objects.select_related("event").annotate(
            event_name=F("event__name")
        )

        if event_id is not None:
            queryset = queryset.filter(event=event_id)

        return queryset

    def create(self, request, *args, **kwargs):
        row_tuple = [
            (
                request.data.get("event"),
                request.data.get("name"),
                request.data.get("field"),
                request.data.get("comment"),
            )
        ]
        with connection.cursor() as cursor:
            query = """
            INSERT INTO common_experiment (event_id, name, field, comment)
            VALUES %s
            ON CONFLICT (event_id, name) DO NOTHING
            RETURNING id;
            """

            execute_values(cursor, query, row_tuple, page_size=1)
            result = cursor.fetchone()
            if result:
                serializer = self.get_serializer(
                    models.Experiment.objects.get(id=result[0])
                )
                # If insert was successful, get the object
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If ON CONFLICT DO NOTHING prevented insert, get the existing object
                instance = models.Experiment.objects.get(
                    event_id=request.data.get("event"), name=request.data.get("name")
                )
                serializer = self.get_serializer(instance)

                return Response(serializer.data, status=status.HTTP_200_OK)


class LogViewSet(viewsets.ModelViewSet):
    queryset = models.Log.objects.all()
    serializer_class = serializers.LogSerializer

    def get_queryset(self):
        queryset = models.Log.objects.all()
        query_params = self.request.query_params

        queryset = generic_filter(models.Log,queryset,query_params)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        instance, created = models.Log.objects.get_or_create(
            game=validated_data.get("game"),
            experiment=validated_data.get("experiment"),
            player_number=validated_data.get("player_number"),
            head_number=validated_data.get("head_number"),
            log_path=validated_data.get("log_path"),
            defaults=validated_data,
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)


class LogStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LogStatusSerializer
    queryset = models.LogStatus.objects.all()

    def get_queryset(self):
        queryset = models.LogStatus.objects.all()
        query_params = self.request.query_params

        queryset = generic_filter(models.Log,queryset,query_params)
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset

    def create(self, request, *args, **kwargs):
        # we get and remove log_id from the request data before validating the rest of the data
        # other we get an error because log_id is 1:1 field to log.id
        log = request.data.pop("log")
        log_instance = get_object_or_404(models.Log, id=int(log))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        validated_data = serializer.validated_data

        instance, created = models.LogStatus.objects.update_or_create(
            log=log_instance, defaults=validated_data
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)
