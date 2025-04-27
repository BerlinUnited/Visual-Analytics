from . import views
from rest_framework import routers

app_name = "annotation"

urlpatterns = []

router = routers.DefaultRouter()
router.register("annotations", views.AnnotationViewSet)

urlpatterns += router.urls
