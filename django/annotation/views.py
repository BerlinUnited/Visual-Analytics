from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q, F,Count
import random
from django.conf import settings
from .models import Annotation
from .serializers import AnnotationSerializer


def generic_filter(queryset,query_params):
        filters = Q()
        for field in Annotation._meta.fields:
            param_value = query_params.get(field.name)
            if param_value == "None" or param_value == "null":
                filters &= Q(**{f"{field.name}__isnull": True})
            elif param_value:
                filters &= Q(**{field.name: param_value})
        # apply filters if provided
        return queryset.filter(filters)

class AnnotationTaskMultiple(APIView):
    def get(self,request):

        query_params = request.query_params.copy()

        queryset = Annotation.objects.filter(validated=False)

        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            queryset = queryset.filter(image__frame__log=log_id)

        if "amount" in query_params.keys():
            amount = int(query_params.pop("amount")[0])
        else:
            amount = 50
    
        queryset = generic_filter(queryset,query_params)

        
        image_ids_with_duplicates = Annotation.objects.values('image_id') \
                                        .annotate(annotation_count=Count('id')) \
                                        .filter(annotation_count__gt=1) \
                                        .values_list('image_id', flat=True)
        queryset = queryset.filter(image__in=list(image_ids_with_duplicates))

        links = []
        print(len(queryset))
        if len(queryset) < amount:
            amount= len(queryset)

        queryset = list(queryset)
        for i in range(amount):

            annotation = random.choice(queryset)
            queryset.remove(annotation)
            if settings.DEBUG:
                # Development - use localhost
                domain = "127.0.0.1:8000"
                scheme = "http"
            else:
                # Production - use your actual domain
                domain = "vat.berlin-united.com"  
                scheme = "https"
            links.append(f"{scheme}://{domain}/log/{annotation.image.frame.log.id}/frame/{annotation.image.frame.frame_number}?filter=None")

        return Response({"result": links}, status=status.HTTP_200_OK)

class AnnotationTaskBorder(APIView):
    def get(self,request):

        query_params = request.query_params.copy()

        queryset = Annotation.objects.filter(validated=False)

        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            queryset = queryset.filter(image__frame__log=log_id)

        if "amount" in query_params.keys():
            amount = int(query_params.pop("amount")[0])
        else:
            amount = 50

        COORDINATE_KEYS = ["x", "y", "width", "height"]
       
        LOOKUP_TYPES = {
            "": "",  
            "_gte": "__gte",  
            "_lte": "__lte", 

        }

        active_filters = {}

        for coord_key in COORDINATE_KEYS:
            for query_suffix, orm_lookup_suffix in LOOKUP_TYPES.items():
                param_name = f"{coord_key}{query_suffix}"

                if param_name in query_params:
                    value_str = query_params.get(param_name)

                    if value_str is not None and value_str != '': # Ensure value is present
                        try:
                            value = float(value_str)
                            
                            # Construct the filter key for the ORM
                            # e.g., "data__x__gte"
                            filter_key = f"data__{coord_key}{orm_lookup_suffix}"
                            
                            # Add to our dictionary of active filters
                            active_filters[filter_key] = value
                            
                           
                            query_params.pop(param_name) # Ensure this doesn't affect other logic
                                                        # if query_params is shared.

                        except ValueError:
                            print(f"Warning: Invalid value for query parameter '{param_name}': '{value_str}'. Skipping.")
                            pass

        # Apply all collected filters at once
        if active_filters:
            queryset = queryset.filter(**active_filters)

        queryset = generic_filter(queryset,query_params)

        links = []

        if len(queryset) < amount:
            amount= len(queryset)

        queryset = list(queryset)
        for i in range(amount):

            annotation = random.choice(queryset)
            queryset.remove(annotation)
            if settings.DEBUG:
                # Development - use localhost
                domain = "127.0.0.1:8000"
                scheme = "http"
            else:
                # Production - use your actual domain
                domain = "vat.berlin-united.com"  
                scheme = "https"
            links.append(f"{scheme}://{domain}/log/{annotation.image.frame.log.id}/frame/{annotation.image.frame.frame_number}?filter=None")

        return Response({"result": links}, status=status.HTTP_200_OK)

class AnnotationTask(APIView):
    def get(self,request):

        query_params = request.query_params.copy()

        queryset = Annotation.objects.filter(validated=False)

        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            queryset = queryset.filter(image__frame__log=log_id)

        if "amount" in query_params.keys():
            amount = int(query_params.pop("amount")[0])
        else:
            amount = 50

        queryset = generic_filter(queryset,query_params)

        links = []

        if len(queryset) < amount:
            amount= len(queryset)

        queryset = list(queryset)
        for i in range(amount):

            annotation = random.choice(queryset)
            queryset.remove(annotation)
            if settings.DEBUG:
                # Development - use localhost
                domain = "127.0.0.1:8000"
                scheme = "http"
            else:
                # Production - use your actual domain
                domain = "vat.berlin-united.com"  
                scheme = "https"
            links.append(f"{scheme}://{domain}/log/{annotation.image.frame.log.id}/frame/{annotation.image.frame.frame_number}?filter=None")

        return Response({"result": links}, status=status.HTTP_200_OK)
        
        
class AnnotationCount(APIView):
    def get(self, request):
        # Get filter parameters from query string
        query_params = request.query_params.copy()

        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            qs = Annotation.objects.filter(image__frame__log=log_id)
        else:
            qs = Annotation.objects.all()
        
        # Handle boolean flags here
        if "validated" in query_params.keys():
            validated_value = query_params.pop("validated")[0]
            if validated_value == 'true':
                qs=qs.filter(validated=True)
            elif validated_value == 'false':
                qs= qs.filter(validated=False)
        # TODO we have other boolean flags and maybe there is way to do that better

        filters = Q()
        for field in Annotation._meta.fields:
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

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        qs = Annotation.objects.all()
        # we use copy here so that the QueryDict object query_params become mutable
        query_params = self.request.query_params.copy()
        if "image" in query_params.keys():
            image_id = int(query_params.pop("image")[0])
            qs = qs.filter(image=image_id)
        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            qs = qs.filter(image__frame__log=log_id)

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
        # annotate with frame number - we could solve this also with properties and serializers
        qs = qs.annotate(frame_number=F('image__frame__frame_number'))

        return qs
    
    # TODO write a create function that checks if json is exactly the same and if so ignores the insert
    def create(self, request, *args, **kwargs):
        # Get the data from the request
        image_id = request.data.get('image')
        annotation_type = request.data.get('type')
        class_name = request.data.get('class_name')
        concealed = request.data.get('concealed', False)
        data = request.data.get('data')
        
        # Check if all required fields are present
        if not all([image_id, annotation_type, class_name, data]):
            return Response(
                {"detail": "Missing required fields"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert concealed to boolean if it's a string
        if isinstance(concealed, str):
            concealed = concealed.lower() == 'true'
        
        # TODO when we use a new yolo model we will get slightly different results, we need to catch this here
        # Look for existing annotation with the same fields
        existing_annotation = Annotation.objects.filter(
            image_id=image_id,
            type=annotation_type,
            class_name=class_name,
            concealed=concealed,
            data=data  # JSONField comparison will handle the structure
        ).first()

        if existing_annotation:
            # Return the existing annotation
            serializer = self.get_serializer(existing_annotation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # No existing annotation found, proceed with normal creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)