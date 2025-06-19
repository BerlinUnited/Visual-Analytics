from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q, Count
from django.db import connection
from psycopg2.extras import execute_values
import random
from . import serializers
from . import models
from rest_framework.decorators import authentication_classes, permission_classes
import time
from behavior.models import BehaviorFrameOption
from cognition.models import CognitionFrame
from django.forms.models import model_to_dict
import numpy as np


class ImageCountView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        # Get filter parameters from query string
        query_params = request.query_params.copy()
        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])

            qs = models.NaoImage.objects.filter(frame__log=log_id)
        else:
            qs = models.NaoImage.objects.all()

        filters = Q()
        for field in models.NaoImage._meta.fields:
            param_value = query_params.get(field.name)
            if param_value == "None" or param_value == "null":
                filters &= Q(**{f"{field.name}__isnull": True})
                # print(f"filter with {field.name} = {param_value}")
            elif param_value:
                # print(f"filter with {field.name} = {param_value}")
                filters &= Q(**{field.name: param_value})

        # apply filters if provided
        qs = qs.filter(filters)

        # get the count
        count = qs.count()

        return Response({"count": count}, status=status.HTTP_200_OK)


class SynchronizedImage(APIView):

    def get(self, request):
        # Get filter parameters from query string
        query_params = request.query_params.copy()
        print(query_params)
        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
        else:
            return Response({"g": "Error World"}, status=status.HTTP_200_OK)

        if "time" in query_params.keys():
            time = float(query_params.pop("time")[0]) * 1000
        else:
            return Response({"g": "Error World"}, status=status.HTTP_200_OK)

        if "camera" in query_params.keys():
            camera = query_params.pop("camera")[0]
        else:
            return Response({"g": "Error World"}, status=status.HTTP_200_OK)

        behavior_data_combined = BehaviorFrameOption.objects.select_related(
            "options_id",  # Joins BehaviorOption
            "active_state",  # Joins BehaviorOptionState
            "active_state__option_id",  # Joins BehaviorOption via BehaviorOptionState
        )
        behavior_frame_options = behavior_data_combined.filter(
            frame__log=log_id,
            options_id__option_name="decide_game_state",
            active_state__name="standby",
        )
        # FIXME we have robots where the behavior logging is broken this breaks this whole thing here
        # TODO can we always use first here? - we want the instance with the lowest frame number, but we get only ids.
        # ids work probably as well - but almost impossible to debug if not, also breaks if data is not entered sequentially,
        print("first value", model_to_dict(behavior_frame_options.first()))

        first_standby_frame_id = behavior_frame_options.values_list("frame", flat=True).first()
        print("first_standby_frame_id", first_standby_frame_id)
        first_standby_frame = CognitionFrame.objects.get(id=first_standby_frame_id)
        print("standby frame", model_to_dict(first_standby_frame))

        cognition_frames = CognitionFrame.objects.filter(log=log_id).order_by("frame_number")
        cognition_frames = list(cognition_frames)
        print()
        print(cognition_frames[0].frame_time)
        frame_time_diffs = [frame.frame_time - (first_standby_frame.frame_time + time) for frame in cognition_frames]
        frame_time_diffs = np.array(frame_time_diffs)

        target_frame_index = np.argmin(np.abs(frame_time_diffs))
        print("target: ", cognition_frames[target_frame_index].frame_number)

        # TODO lets return the image path here
        target_image = models.NaoImage.objects.filter(
            frame__log=log_id, frame__frame_number=cognition_frames[target_frame_index].frame_number, camera=camera
        ).first()
        return Response({"url": target_image.image_url}, status=status.HTTP_200_OK)


class ImageUpdateView(APIView):
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
                case_stmt = f"""{field} = (CASE {" ".join(case_when_parts)} ELSE {field} END)"""
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


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 10
    page_size_query_param = "page_size"


class ImagePageSet(viewsets.ModelViewSet):
    queryset = models.NaoImage.objects.all()
    serializer_class = serializers.ImageSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        # we use copy here so that the QueryDict object query_params become mutable
        query_params = self.request.query_params.copy()

        qs = self.queryset

        print(query_params)
        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            qs = qs.filter(frame__log=log_id)

        if "frame_number" in query_params.keys():
            frame_number = int(query_params.pop("frame_number")[0])
            qs = qs.filter(frame__frame_number=frame_number)

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

        qs = qs.filter(filters)

        # check if the frontend wants to use a frame filter
        # FIXME select frame_filter by name
        if "use_filter" in query_params and query_params.get("use_filter") == "1":
            # check if we have a list of frames set here
            frames = models.FrameFilter.objects.filter(
                log_id=query_params.get("log"),
                user=self.request.user,
            ).first()

            if frames:
                qs = qs.filter(frame_number__in=frames.frames["frame_list"])

        return qs.order_by("frame")


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.NaoImage.objects.all()
    serializer_class = serializers.ImageSerializer

    def get_queryset(self):
        # we use copy here so that the QueryDict object query_params become mutable
        query_params = self.request.query_params.copy()

        qs = models.NaoImage.objects.all()
        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            qs = qs.filter(frame__log=log_id)

        if "frame_number" in query_params.keys():
            frame_number = int(query_params.pop("frame_number")[0])
            qs = qs.filter(frame__frame_number=frame_number)

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

        qs = qs.filter(filters)

        # check if the frontend wants to use a frame filter
        # FIXME select frame_filter by name
        if "use_filter" in query_params and query_params.get("use_filter") == "1":
            # check if we have a list of frames set here
            frames = models.FrameFilter.objects.filter(
                log_id=query_params.get("log"),
                user=self.request.user,
            ).first()

            if frames:
                qs = qs.filter(frame_number__in=frames.frames["frame_list"])

        return qs.order_by("frame")

        # if the exclude_annotated parameter is set all images with an existing annotation are not included in the response
        if "exclude_annotated" in query_params:
            qs = qs.annotate(metadata_count=Count("Annotation")).filter(metadata_count=0)

        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return qs.order_by("frame")

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

        #
        update_fields = {k: v for k, v in data.items()}
        updated = models.NaoImage.objects.filter(id=image_id).update(**update_fields)
        # FIXME can we use get instead of filter and can we return the image we updated here???
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
