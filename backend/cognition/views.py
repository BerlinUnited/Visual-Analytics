from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CognitionFrame
from . import serializers

from django.db import connection
from django.db.models import Q
from django.apps import apps
from psycopg2.extras import execute_values
import json


class DynamicModelMixin:
    def get_model(self):
        # Get the model name from the URL kwargs
        model_name = self.kwargs.get('model_name')
        # Get the model class from the app's models
        return apps.get_model('cognition', model_name)

    def get_queryset(self):
        # Override get_queryset to use the dynamic model
        model = self.get_model()
        queryset = model.objects.all()
        query_params = self.request.query_params

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
        rows_tuples = [
            (row['frame'], json.dumps(row['representation_data']))
            for row in request.data
        ]

        with connection.cursor() as cursor:
            query = f"""
            INSERT INTO cognition_{model.__name__.lower()} (frame_id, representation_data)
            VALUES %s
            ON CONFLICT (frame_id) DO UPDATE SET representation_data = EXCLUDED.representation_data;
            """
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=500)

        return Response({}, status=status.HTTP_200_OK)


class CognitionFrameCount(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get('log_id')

        # start with all images
        queryset = CognitionFrame.objects.all()

        # apply filters if provided
        queryset = queryset.filter(log_id=log_id)

        # get the count
        count = queryset.count()
        return Response({'count': count}, status=status.HTTP_200_OK)
    

class CognitionFrameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CognitionFrameSerializer
    queryset = CognitionFrame.objects.all()

    def get_queryset(self):
        queryset = CognitionFrame.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in CognitionFrame._meta.fields:
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

        rows_tuples = [(row['log_id'], row['frame_number'], row['frame_time']) for row in request.data]

        with connection.cursor() as cursor:
            query = """
            INSERT INTO cognition_cognitionframe (log_id_id, frame_number, frame_time)
            VALUES %s
            ON CONFLICT (log_id_id, frame_number) DO NOTHING;
            """ 
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=500)

        return Response({
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get('pk') == 'all':
            deleted_count, _ = self.get_queryset().delete()
            return Response({'message': f'Deleted {deleted_count} objects'}, status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)