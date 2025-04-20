from django.db import models
from common.models import Log

"""
    All Models for Motion Representations
"""


class MotionFrame(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="motionframe")
    frame_number = models.IntegerField(blank=True, null=True)
    frame_time = models.IntegerField(blank=True, null=True)
    closest_cognition_frame = models.ForeignKey('cognition.CognitionFrame',on_delete=models.DO_NOTHING,related_name="closest_cognition_frame",null=True,
        blank=True)
    class Meta:
        verbose_name_plural = "Motion Frames"
        indexes = [
            models.Index(fields=["log", "frame_number"]),
        ]
        unique_together = ("log", "frame_number")


class IMUData(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="imudata"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "IMU Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_imudata")
        ]


class FSRData(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="fsrdata"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "FSR Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_fsrdata")
        ]


class ButtonData(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="buttondata"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Button Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_buttondata")
        ]


class SensorJointData(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="sensorjointdata"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Sensor Joint Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_sensorjointdata")
        ]


class AccelerometerData(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="accelerometerdata"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Accelerometer Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_accelerometerdata")
        ]


class InertialSensorData(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="inertialsensordata"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Inertial Sensor Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_inertialsensordata")
        ]


class MotionStatus(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="motionstatus"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Motion Status"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_motionstatus")
        ]


class MotorJointData(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="motorjointdata"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Motor Joint Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_motorjointdata")
        ]


class GyrometerData(models.Model):
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="gyrometerdata"
    )
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Gyrometer Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_gyrometerdata")
        ]
