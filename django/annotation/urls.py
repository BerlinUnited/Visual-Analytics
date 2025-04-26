from . import views
from rest_framework import routers

app_name = "annotation"

urlpatterns = []

router = routers.DefaultRouter()
router.register("annotations", views.AnnotationViewSet)
router.register("annotationclass", views.AnnotationClassViewSet)

urlpatterns += router.urls
