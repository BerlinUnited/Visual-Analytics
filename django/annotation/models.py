from django.db import models
from image.models import NaoImage
from django.utils.translation import gettext_lazy as _


class Annotation(models.Model):
    class Types(models.TextChoices):
        bbox = "bbox", _("Bounding Box")
        segmentation = "segmentation", _("Segmentation")
        polygon = "polygon", _("Polygon")

    class Classes(models.TextChoices):
        nao = "nao", _("Nao")
        ball = "ball", _("Ball")
        penaltymark = "penaltymark", _("Penalty Mark")

        @classmethod
        def get_color(cls, class_name):
            colors = {
                cls.nao: '#134dab',
                cls.ball: '#b31290',
                cls.penaltymark: '#f51b1f',
            }
            return colors.get(class_name)

    image = models.ForeignKey(NaoImage, on_delete=models.CASCADE, related_name="annotation")
    type = models.CharField(max_length=20, choices=Types, blank=True, null=True)
    class_name = models.CharField(max_length=20, choices=Classes, blank=True, null=True)
    concealed = models.BooleanField(default=False)
    data = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


# TODO build models for labeling situations
