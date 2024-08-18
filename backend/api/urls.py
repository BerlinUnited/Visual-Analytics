from django.urls import path
from . import views
from rest_framework import routers
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('health/',views.health_check,name="health_check"),
    path('api/image-count/', views.ImageCountView.as_view(), name='image-count'),
]

router = routers.DefaultRouter()
router.register('events',views.EventViewSet)
router.register('games', views.GameViewSet)
router.register('robotdata',views.RobotDataViewSet)
router.register('image',views.ImageViewSet)
router.register('imageannotation',views.ImageAnnotationViewSet)
router.register("sensorlogs",views.SensorLogViewSet)

urlpatterns += router.urls
