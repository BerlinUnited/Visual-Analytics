from django.urls import path
from . import views
from rest_framework import routers

app_name = "motion"

urlpatterns = [
    path(
        "motionframe/count/", views.MotionFrameCount.as_view(), name="motionframe-count"
    ),
]

router = routers.DefaultRouter()
router.register("motionframe", views.MotionFrameViewSet)
router.register(
    "motion/(?P<model_name>[^/.]+)",
    views.DynamicModelViewSet,
    basename="dynamicmodel",
)

urlpatterns += router.urls
