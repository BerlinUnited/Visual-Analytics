from django.urls import path
from . import views
from rest_framework import routers

app_name = "common"

urlpatterns = [
    path("", views.scalar_doc, name="scalar_doc"),
    path("health/", views.health_check, name="health_check"),
    path('upload/model/', views.ModelUploadView.as_view(), name='upload-model'),
    path('upload/dataset/', views.DatasetUploadView.as_view(), name='upload-dataset'),
]

router = routers.DefaultRouter()
router.register("events", views.EventViewSet)
router.register("games", views.GameViewSet)
router.register("experiments", views.ExperimentViewSet)
router.register("logs", views.LogViewSet)
router.register("log-status", views.LogStatusViewSet)
router.register("video", views.VideoViewSet)


urlpatterns += router.urls
