from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from django.db.models import Q, Count
from django.db import connection
from psycopg2.extras import execute_values

from common.models import Log
from . import serializers
from . import models

import time


class ImageCountView(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get("log")
        camera = request.query_params.get("camera")
        image_type = request.query_params.get("type")

        # get log instance
        log_instance = Log.objects.get(id=log_id)

        # apply filters if provided
        queryset = models.NaoImage.objects.filter(
            frame__log=log_instance, camera=camera, type=image_type
        )

        # get the count
        count = queryset.count()

        return Response({"count": count}, status=status.HTTP_200_OK)


class ImageUpdateView(APIView):
    def patch(self, request):
        data = self.request.data
        try:
            rows_updated = self.bulk_insert(data)

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

    def bulk_insert(self, data):
        update_fields = set()

        for item in data:
            update_fields.update(key for key in item.keys() if key != "id")

        starttime = time.time()
        # Build the case statements for each field
        case_statements = []
        for field in update_fields:
            case_when_parts = []
            for item in data:
                if field in item and item[field] is not None:
                    case_when_parts.append(f"WHEN id = {item['id']} THEN %s")

            if case_when_parts:
                case_stmt = (
                    f"""{field} = (CASE {" ".join(case_when_parts)} ELSE {field} END)"""
                )
                case_statements.append(case_stmt)

        # Collect all values for the parameterized query
        update_values = []
        for field in update_fields:
            for item in data:
                if field in item and item[field] is not None:
                    update_values.append(item[field])

        # Build the complete SQL query
        ids = [str(item["id"]) for item in data]
        sql = f"""
            UPDATE image_naoimage
            SET {", ".join(case_statements)}
            WHERE id IN ({",".join(ids)})
        """
        # print(sql)

        with connection.cursor() as cursor:
            cursor.execute(sql, update_values)
            return cursor.rowcount
        print(time.time() - starttime)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.NaoImage.objects.all()
    serializer_class = serializers.ImageSerializer

    def get_queryset(self):
        queryset = models.NaoImage.objects.all()
        # we use copy here so that the QueryDict object query_params become mutable
        query_params = self.request.query_params.copy()

        # This is a generic filter on the queryset, the supplied filter must be a field in the Image model
        filters = Q()
        for field in models.NaoImage._meta.fields:
            param_value = query_params.get(field.name)
            if param_value == "None" or param_value == "null":
                filters &= Q(**{f"{field.name}__isnull": True})
                # print(f"filter with {field.name} = {param_value}")
            elif param_value:
                # print(f"filter with {field.name} = {param_value}")
                filters &= Q(**{field.name: param_value})

        qs = queryset.filter(filters)

        # check if the frontend wants to use a frame filter
        if "use_filter" in query_params and query_params.get("use_filter") == "1":
            # check if we have a list of frames set here
            frames = models.FrameFilter.objects.filter(
                log_id=query_params.get("log"),
                user=self.request.user,
            ).first()

            if frames:
                qs = qs.filter(frame_number__in=frames.frames["frame_list"])

        # if the exclude_annotated parameter is set all images with an existing annotation are not included in the response
        if "exclude_annotated" in query_params:
            qs = qs.annotate(metadata_count=Count("Annotation")).filter(
                metadata_count=0
            )

        # print(qs.order_by('frame_number').count())
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return qs.order_by("frame_number")

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)

        if is_many:
            return self.bulk_create(request.data)
        else:
            return self.single_create(request.data)

    # FIXME combine with ImageUpdateView
    def update(self, request, *args, **kwargs):
        # Check if the data is a list (bulk update) or dict (single update)
        is_many = isinstance(request.data, list)
        print(is_many)
        if is_many:
            return self.bulk_update()
        else:
            return self.single_update()

    def single_update(self):
        image_id = self.kwargs["pk"]  # image id from the url: /api/image/17018/
        data = self.request.data

        # we ignore the fields that act as unique identifiers here
        update_fields = {
            k: v for k, v in data.items() if k not in ["frame", "camera", "type"]
        }
        updated = models.NaoImage.objects.filter(id=image_id).update(**update_fields)

        status_code = status.HTTP_201_CREATED if updated else status.HTTP_200_OK
        return Response({}, status=status_code)

    def single_create(self, data):
        serializer = self.get_serializer(data, many=False)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        instance, created = models.NaoImage.objects.get_or_create(
            frame=validated_data.get("frame"),
            camera=validated_data.get("camera"),
            type=validated_data.get("type"),
            defaults=validated_data,
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, data):
        # validated_data = serializer.validated_data
        starttime = time.time()
        rows_tuples = [
            (
                row["frame"],
                row["camera"],
                row["type"],
                row["image_url"],
                row["blurredness_value"],
                row["brightness_value"],
                row["resolution"],
            )
            for row in data
        ]
        with connection.cursor() as cursor:
            query = """
            INSERT INTO image_naoimage (frame_id, camera, type, image_url, blurredness_value, brightness_value, resolution)
            VALUES %s
            ON CONFLICT (frame_id, camera, type) DO NOTHING;
            """
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=1000)
        print(time.time() - starttime)
        # TODO calculate some statistics similar to what we did before here
        return Response({}, status=status.HTTP_200_OK)
