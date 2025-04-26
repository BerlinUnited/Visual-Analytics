from django.db import models
from image.models import NaoImage


class AnnotationClass(models.Model):
    name = models.CharField(max_length=40, unique=True)
    color = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Annotation Classes"


class Annotation(models.Model):
    image = models.OneToOneField(
        NaoImage, on_delete=models.CASCADE, related_name="annotation", primary_key=True
    )
    annotation = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


# TODO build models for labeling situations