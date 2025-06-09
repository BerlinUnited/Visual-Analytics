from django.urls import path
from . import views
from rest_framework import routers

app_name = "image"

urlpatterns = [
    path("image-count/", views.ImageCountView.as_view(), name="image-count"),
    path("image/update/", views.ImageUpdateView.as_view(), name="image-update"),
]

router = routers.DefaultRouter()
router.register("image", views.ImageViewSet)
router.register("image-list", views.ImagePageSet, "image-list")

urlpatterns += router.urls
