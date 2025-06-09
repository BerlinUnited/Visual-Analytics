from django.db import models
from cognition.models import CognitionFrame
from django.utils.translation import gettext_lazy as _


class NaoImage(models.Model):
    class Camera(models.TextChoices):
        TOP = "TOP", _("Top")
        BOTTOM = "BOTTOM", _("Bottom")

    class Type(models.TextChoices):
        raw = "RAW", _("raw")
        jpeg = "JPEG", _("jpeg")

    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="images"
    )
    camera = models.CharField(max_length=10, choices=Camera, blank=True, null=True)
    type = models.CharField(max_length=10, choices=Type, blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    blurredness_value = models.IntegerField(blank=True, null=True)
    brightness_value = models.IntegerField(blank=True, null=True)
    resolution = models.CharField(max_length=11, blank=True, null=True)  # 1640x1480x2

    class Meta:
        unique_together = ("frame", "camera", "type")

    def __str__(self):
        return f"{self.frame}-{self.camera}-{self.type}"

    @property
    def frame_number(self):
        return self.frame.frame_number
