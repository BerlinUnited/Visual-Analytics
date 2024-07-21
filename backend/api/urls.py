from django.urls import path
from . import views
from rest_framework import routers
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui')
]

router = routers.DefaultRouter()
router.register('events',views.EventViewSet)
router.register('games', views.GameViewSet)
router.register('logs',views.LogViewSet)


urlpatterns += router.urls