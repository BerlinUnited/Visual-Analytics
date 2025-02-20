from django.urls import path
from . import views
from rest_framework import routers

app_name = 'cognition'

urlpatterns = [
    path('cognitionframe/count/', views.CognitionFrameCount.as_view(), name='cognitionframe-count'),
]

router = routers.DefaultRouter()
router.register("cognitionframe",views.CognitionFrameViewSet)

urlpatterns += router.urls