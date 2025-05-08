from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q, F

from .models import Annotation
from .serializers import AnnotationSerializer


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
        print(qs.values().first())

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