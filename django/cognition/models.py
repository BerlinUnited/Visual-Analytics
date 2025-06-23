from django.db import models
from common.models import Log
from django.conf import settings


class CognitionFrame(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="cognitionframe")
    frame_number = models.IntegerField(blank=True, null=True)
    frame_time = models.IntegerField(blank=True, null=True)
    closest_motion_frame = models.ForeignKey(
        "motion.Motionframe",
        on_delete=models.SET_NULL,
        related_name="closest_motion_frame",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Cognition Frames"
        indexes = [
            models.Index(fields=["log", "frame_number"]),
        ]
        unique_together = ("log", "frame_number")


class FrameFilter(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="frame_filter")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="frame_filter")
    name = models.CharField(max_length=100)
    frames = models.JSONField(blank=True, null=True)

    unique_together = ("log", "user", "name")


class AudioData(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="audiodata")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Audio Data"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_audiodata")]


class BallModel(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="ballmodel")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ball Model"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_ballmodel")]


class BallCandidates(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="ballcandidates")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ball Candidates"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_ballcandidates")]


class BallCandidatesTop(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="ballcandidatestop")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ball Candidates Top"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_ballcandidatestop")]


class CameraMatrix(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="cameramatrix")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Camera Matrix"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_cameramatrix")]


class CameraMatrixTop(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="cameramatrixtop")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Camera Matrix Top"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_cameramatrixtop")]


class OdometryData(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="odometrydata")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Odometry Data"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_odometrydata")]


class FieldPercept(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="fieldpercept")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Field Percept"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_fieldpercept")]


class FieldPerceptTop(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="fieldpercepttop")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Field Percept Top"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_fieldpercepttop")]


class GoalPercept(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="goalpercept")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Goal Percept"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_goalpercept")]


class GoalPerceptTop(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="goalpercepttop")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Goal Percept Top"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_goalpercepttop")]


class MultiBallPercept(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="multiballpercept")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Multi Ball Percept"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_multiballpercept")]


class RansacCirclePercept2018(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="ransaccirclepercept2018")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ransac Circle Percept 2018"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_ransaccirclepercept2018")]


class RansacLinePercept(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="ransaclinepercept")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ransac Line Percept"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_ransaclinepercept")]


class RobotInfo(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="robotinfo")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Robot Info"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_robotinfo")]


class ShortLinePercept(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="shortlinepercept")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Short Line Percept"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_shortlinepercept")]


class ScanLineEdgelPercept(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="scanlineedgelpercept")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Scanline Edgel Percept"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_scanlineedgelpercept")]


class ScanLineEdgelPerceptTop(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="scanlineedgelpercepttop")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Scanline Edgel Percept Top"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_scanlineedgelpercepttop")]


class TeamMessageDecision(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="teammessagedecision")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Team Message Decision"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_teammessagedecision")]


class Teamstate(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="teamstate")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Team State"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_teamstate")]


class WhistlePercept(models.Model):
    frame = models.ForeignKey(CognitionFrame, on_delete=models.CASCADE, related_name="whistlepercept")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    @property
    def frame_number(self):
        return self.frame.frame_number

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Whistle Percept"
        constraints = [models.UniqueConstraint(fields=["frame"], name="unique_frame_id_whistlepercept")]
