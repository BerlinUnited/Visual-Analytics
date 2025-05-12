from django.urls import path
from . import views
from rest_framework import routers

app_name = "annotation"

urlpatterns = [
    path("annotation-count/", views.AnnotationCount.as_view(), name="annotation-count"),
    path("annotation-unvalidated/",views.AnnotationsUnvalidated.as_view(),name="unvalidated_annotations")
]

router = routers.DefaultRouter()
router.register("annotations", views.AnnotationViewSet)

urlpatterns += router.urls
