from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import MotionFrame
from . import serializers

from django.db import connection
from django.db.models import Q
from django.apps import apps
from psycopg2.extras import execute_values
import json


class DynamicModelMixin:
    def get_model(self):
        # Get the model name from the URL kwargs
        model_name = self.kwargs.get("model_name")
        # Get the model class from the app's models
        return apps.get_model("motion", model_name)

    def get_queryset(self):
        # Override get_queryset to use the dynamic model
        model = self.get_model()
        query_params = self.request.query_params.copy()

        # if log was set filter for it
        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            queryset = model.objects.filter(frame__log=log_id)

        filters = Q()
        for field in model._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        return queryset.filter(filters)


class DynamicModelViewSet(DynamicModelMixin, viewsets.ModelViewSet):
    # No need to define queryset or serializer_class here; they will be set dynamically
    def get_serializer_class(self):
        # Dynamically set the serializer class based on the model
        model = self.get_model()
        # Assuming you have a naming convention for serializers, e.g., <ModelName>Serializer
        serializer_class_name = f"{model.__name__}Serializer"
        return getattr(serializers, serializer_class_name)

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        if not is_many:
            print("error: input not a list")
            return Response({}, status=status.HTTP_411_LENGTH_REQUIRED)

        # Dynamically get the model
        model = self.get_model()

        # Prepare the data for bulk insert
        rows_tuples = [(row["frame"], row["start_pos"], row["size"]) for row in request.data]

        with connection.cursor() as cursor:
            query = f"""
            INSERT INTO motion_{model.__name__.lower()} (frame_id, start_pos, size)
            VALUES %s
            ON CONFLICT (frame_id) DO UPDATE SET start_pos = EXCLUDED.start_pos, size = EXCLUDED.size;
            """
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=500)

        return Response({}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="count")
    def count_records(self, request, *args, **kwargs):
        """
        Custom action to count records in the dynamic model.
        Accessible at /api/motion/<modelname>/count/
        """
        # Get filter parameters from query string
        log_id = request.query_params.get("log")

        model = self.get_model()
        queryset = model.objects.filter(frame__log=log_id)

        # You can add any additional filtering here if needed
        count = queryset.count()

        return Response({"count": count})


class MotionFrameCount(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get("log")

        # start with all images
        queryset = MotionFrame.objects.all()

        # apply filters if provided
        queryset = queryset.filter(log=log_id)

        # get the count
        count = queryset.count()
        return Response({"count": count}, status=status.HTTP_200_OK)


class MotionFrameUpdate(APIView):
    def patch(self, request):
        data = self.request.data
        try:
            rows_updated = self.bulk_update(data)

            return Response(
                {
                    "success": True,
                    "rows_updated": rows_updated,
                    "message": f"Successfully updated {rows_updated} images",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "rows_updated": 0, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def bulk_update(self, data):
        update_fields = set()

        # since closest_cognition_frame is a foreign key and therefore has not the same name in the db
        # as it has in django we need to take care of the transformation manually here
        transformed_data = []

        for item in data:
            new_item = {}
            for key, value in item.items():
                if key == "closest_cognition_frame":
                    new_item["closest_cognition_frame_id"] = value
                else:
                    new_item[key] = value
            transformed_data.append(new_item)

        for item in transformed_data:
            update_fields.update(key for key in item.keys() if key != "id")

        # Build the case statements for each field
        case_statements = []
        for field in update_fields:
            case_when_parts = []
            for item in transformed_data:
                print("item", item)
                if field in item and item[field] is not None:
                    case_when_parts.append(f"WHEN id = {item['id']} THEN %s")

            if case_when_parts:
                case_stmt = f"""{field} = (CASE {" ".join(case_when_parts)} ELSE {field} END)"""
                case_statements.append(case_stmt)

        # Collect all values for the parameterized query
        update_values = []
        for field in update_fields:
            for item in transformed_data:
                if field in item and item[field] is not None:
                    update_values.append(item[field])

        # Build the complete SQL query
        ids = [str(item["id"]) for item in transformed_data]
        sql = f"""
            UPDATE motion_motionframe
            SET {", ".join(case_statements)}
            WHERE id IN ({",".join(ids)})
        """
        print(sql)

        with connection.cursor() as cursor:
            cursor.execute(sql, update_values)
            return cursor.rowcount


class MotionFrameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MotionFrameSerializer
    queryset = MotionFrame.objects.all()

    def get_queryset(self):
        queryset = MotionFrame.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in MotionFrame._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        if not is_many:
            print("error: input not a list")
            return Response({}, status=status.HTTP_411_LENGTH_REQUIRED)

        rows_tuples = [(row["log"], row["frame_number"], row["frame_time"]) for row in request.data]

        with connection.cursor() as cursor:
            query = """
            INSERT INTO motion_motionframe (log_id, frame_number, frame_time)
            VALUES %s
            ON CONFLICT (log_id, frame_number) DO NOTHING;
            """
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=500)

        return Response({}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get("pk") == "all":
            deleted_count, _ = self.get_queryset().delete()
            return Response(
                {"message": f"Deleted {deleted_count} objects"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return super().destroy(request, *args, **kwargs)
