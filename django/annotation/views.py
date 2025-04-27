from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from django.db import connection
from psycopg2.extras import execute_values
from .models import Annotation
from .serializers import AnnotationSerializer

import datetime


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        # we use copy here so that the QueryDict object query_params become mutable
        query_params = self.request.query_params.copy()
        image_id = int(query_params.pop("image")[0])

        qs = Annotation.objects.filter(image=image_id)

         # This is a generic filter on the queryset, the supplied filter must be a field in the Image model
        filters = Q()
        for field in Annotation._meta.fields:
            param_value = query_params.get(field.name)
            if param_value == "None" or param_value == "null":
                filters &= Q(**{f"{field.name}__isnull": True})
                # print(f"filter with {field.name} = {param_value}")
            elif param_value:
                # print(f"filter with {field.name} = {param_value}")
                filters &= Q(**{field.name: param_value})

        qs = qs.filter(filters)
        return qs