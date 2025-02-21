from django.db import models
from api.models import Log

"""
    All Models for Cognition Representations
"""
class CognitionFrame(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='cognitionframe')
    frame_number = models.IntegerField(blank=True, null=True)
    frame_time = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Cognition Frames"
        indexes = [
            models.Index(fields=['log_id', 'frame_number']),
        ]
        unique_together = ('log_id', 'frame_number')


class BallModel(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='ballmodel')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Ball Model"


class BallCandidates(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='ballcandidates')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Ball Candidates"


class BallCandidatesTop(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='ballcandidatestop')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Ball Candidates Top"


class CameraMatrix(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='cameramatrix')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Camera Matrix"


class CameraMatrixTop(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='cameramatrixtop')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Camera Matrix Top"


class OdometryData(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='odometrydata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Odometry Data"


class FieldPercept(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='fieldpercept')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Field Percept"


class FieldPerceptTop(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='fieldpercepttop')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Field Percept Top"


class GoalPercept(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='goalpercept')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Goal Percept"


class GoalPerceptTop(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='goalpercepttop')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Goal Percept Top"


class MultiBallPercept(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='multiballpercept')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Multi Ball Percept"


class RansacLinePercept(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='ransaclinepercept')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Ransac Line Percept"


class ShortLinePercept(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='shortlinepercept')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Short Line Percept"


class ScanLineEdgelPercept(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='scanlineedgelpercept')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Scanline Edgel Percept"


class ScanLineEdgelPerceptTop(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='scanlineedgelpercepttop')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Scanline Edgel Percept Top"


class RansacCirclePercept2018(models.Model):
    frame = models.ForeignKey(CognitionFrame,on_delete=models.CASCADE, related_name='ransaccirclepercept2018')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Ransac Circle Percept 2018"
