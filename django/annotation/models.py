from django.db import models
from image.models import NaoImage
from common.models import VideoRecording
from django.utils.translation import gettext_lazy as _


class Annotation(models.Model):
    class Types(models.TextChoices):
        bbox = "bbox", _("Bounding Box")
        segmentation = "segmentation", _("Segmentation")
        polygon = (
            "polygon",
            _("Polygon"),
        )  # idea is to convert segmentation masks to polygon
        pose = "pose", _("Pose")
        point = "point", _("Point")

    class Classes(models.TextChoices):
        nao = "nao", _("Nao")
        ball = "ball", _("Ball")
        penaltymark = "penaltymark", _("Penalty Mark")
        referee = "referee", _("Referee")
        goalpost = "goalpost", _("Goalpost")
        t_cross = "t_cross", _("T Cross")
        center_cross = "center_cross", _("Center Cross")
        circle_cross = "circle_cross", _("Circle Cross")
        l_cross = "l_cross", _("L Cross")
        line = "line", _("Line")
        own_contour = "own_contour", _("Own_Contour")

        @classmethod
        def get_color(cls, class_name):
            colors = {
                cls.nao: "#134dab",
                cls.ball: "#b31290",
                cls.penaltymark: "#f51b1f",
                cls.referee: "#ffffff",
                cls.goalpost: "#1de6f5",
                cls.t_cross: "#6608c4",
                cls.center_cross: "#6608c4",
                cls.circle_cross: "#6608c4",
                cls.l_cross: "#6608c4",
                cls.line: "#ff0000",
                cls.own_contour: "#0000ff",
            }
            return colors.get(class_name)

    image = models.ForeignKey(
        NaoImage, on_delete=models.CASCADE, related_name="annotation"
    )
    # TODO: maybe add log as extra foreign key (needs to be changed in api and on insert scripts)
    type = models.CharField(max_length=20, choices=Types, blank=True, null=True)
    class_name = models.CharField(max_length=20, choices=Classes, blank=True, null=True)
    concealed = models.BooleanField(default=False)
    # we want to say that an image does not contain any of the classes
    is_empty = models.BooleanField(
        blank=True, null=True
    )  # TODO proably not that useful
    # labels = models.JSONField(blank=True, null=True)
    validated = models.BooleanField(default=False)
    data = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)



class VideoFrame(models.Model):
    video = models.ForeignKey(
        VideoRecording, on_delete=models.CASCADE, related_name="frame"
    )
    frame_number = models.IntegerField(blank=True, null=True)


class VideoAnnotation(models.Model):
    """
    type can be encoded in the json as box = {data} or mask = {data} or kpts = {data} allowing for flexibility in the data we represent.
    it could happen that we have a couple different mask formats down the line

    In the end we can have a bounding box, mask and keypoint for each instance of a class. For example a Nao robot might first be annotated with a single keypoint
    which will be used as input for a bounding box detection model and which then will be used as input for an segmentation model. For classes like
    Nao and Ball this makes sense. It makes less sense for lines.

    there are no unique constraints here but on insert we should try to check if something with a high IOU already exist
    """
    frame = models.ForeignKey(
        VideoFrame, on_delete=models.CASCADE, related_name="videoannotation"
    )
    class_name = models.CharField(max_length=30, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    concealed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


# TODO build models for labeling situations

# TODO build models for ball patches
# class BallPatches(models.Model):
#    # TODO how can i use the information about which sha is best, like ordering or figuring out in which branches they are etc.
#    image = models.ForeignKey(NaoImage, on_delete=models.CASCADE, related_name="ballpatches")
#    commit = models.CharField(max_length=40, blank=True, null=True)
#    data = models.JSONField(blank=True, null=True)
