from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(
        max_length=100, blank=True, null=True
    )  # latitude and longitude in Degrees, minutes, and seconds (DMS)
    event_folder = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    team_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"


class Game(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="games")
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1", null=True)
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2", null=True)
    half = models.CharField(max_length=100, blank=True, null=True)
    is_testgame = models.BooleanField(blank=True, null=True)
    head_ref = models.CharField(max_length=100, blank=True, null=True)
    assistent_ref = models.CharField(max_length=100, blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    score = models.CharField(max_length=100, blank=True, null=True)
    game_folder = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("event_id", "start_time", "half")

    def __str__(self):
        return f"{self.start_time}: {self.team1} vs {self.team2} {self.half}"


class Experiment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="experiments")
    # either the folder name if its an experiment of multiple robots or the logfile name
    name = models.CharField(max_length=100, blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("event_id", "name")


class VideoRecording(models.Model):
    class Camera(models.TextChoices):
        GoPro = "GoPro", _("GoPro")
        PiCam = "PiCam", _("PiCam")

    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.CASCADE, related_name="recordings")
    experiment = models.ForeignKey(Experiment, null=True, blank=True, on_delete=models.CASCADE)
    video_path = models.CharField(max_length=200, blank=True, null=True)
    # urls should optionally include the youtube links
    url = models.CharField(max_length=120, blank=True, null=True)
    type = models.CharField(max_length=10, choices=Camera, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class Log(models.Model):
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, null=True, blank=True, on_delete=models.CASCADE)
    robot_version = models.CharField(max_length=5, blank=True, null=True)
    player_number = models.IntegerField(blank=True, null=True)
    head_number = models.IntegerField(blank=True, null=True)
    body_serial = models.CharField(max_length=20, blank=True, null=True)
    head_serial = models.CharField(max_length=20, blank=True, null=True)
    representation_list = models.JSONField(blank=True, null=True)
    log_path = models.CharField(max_length=200, blank=True, null=True)
    combined_log_path = models.CharField(max_length=200, blank=True, null=True)
    sensor_log_path = models.CharField(max_length=200, blank=True, null=True)

    git_commit = models.CharField(max_length=60, blank=True, null=True)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.log_path}"

    @property
    def log_type(self):
        # TODO how is this supposed to work?
        if self.game_id is not None:
            return self.game
        if self.experiment_id is not None:
            return self.experiment
        raise AssertionError("Neither 'log_game_id' nor 'log_experiment_id' is set")

    @property
    def event_name(self):
        return self.game.event.name

    @property
    def game_name(self):
        game_name = f"{self.game.team1}_vs_{self.game.team2}_{self.game.half}"
        return game_name


class LogStatus(models.Model):
    log = models.OneToOneField(Log, on_delete=models.CASCADE, related_name="log_status", primary_key=True)
    # holds the number of frames that should be in the db for each representation
    AudioData = models.IntegerField(blank=True, null=True)
    BallCandidates = models.IntegerField(blank=True, null=True)
    BallCandidatesTop = models.IntegerField(blank=True, null=True)
    BallModel = models.IntegerField(blank=True, null=True)
    BehaviorStateComplete = models.IntegerField(blank=True, null=True)
    BehaviorStateSparse = models.IntegerField(blank=True, null=True)
    CameraMatrix = models.IntegerField(blank=True, null=True)
    CameraMatrixTop = models.IntegerField(blank=True, null=True)
    FieldPercept = models.IntegerField(blank=True, null=True)
    FieldPerceptTop = models.IntegerField(blank=True, null=True)
    FrameInfo = models.IntegerField(blank=True, null=True)
    GoalPercept = models.IntegerField(blank=True, null=True)
    GoalPerceptTop = models.IntegerField(blank=True, null=True)
    MultiBallPercept = models.IntegerField(blank=True, null=True)
    RansacCirclePercept2018 = models.IntegerField(blank=True, null=True)
    RansacLinePercept = models.IntegerField(blank=True, null=True)
    RobotInfo = models.IntegerField(blank=True, null=True)
    ShortLinePercept = models.IntegerField(blank=True, null=True)
    ScanLineEdgelPercept = models.IntegerField(blank=True, null=True)
    ScanLineEdgelPerceptTop = models.IntegerField(blank=True, null=True)
    TeamMessageDecision = models.IntegerField(blank=True, null=True)
    TeamState = models.IntegerField(blank=True, null=True)
    OdometryData = models.IntegerField(blank=True, null=True)
    Image = models.IntegerField(blank=True, null=True)
    ImageTop = models.IntegerField(blank=True, null=True)
    ImageJPEG = models.IntegerField(blank=True, null=True)
    ImageJPEGTop = models.IntegerField(blank=True, null=True)
    WhistlePercept = models.IntegerField(blank=True, null=True)

    IMUData = models.IntegerField(blank=True, null=True)
    FSRData = models.IntegerField(blank=True, null=True)
    ButtonData = models.IntegerField(blank=True, null=True)
    SensorJointData = models.IntegerField(blank=True, null=True)
    AccelerometerData = models.IntegerField(blank=True, null=True)
    InertialSensorData = models.IntegerField(blank=True, null=True)
    MotionStatus = models.IntegerField(blank=True, null=True)
    MotorJointData = models.IntegerField(blank=True, null=True)
    GyrometerData = models.IntegerField(blank=True, null=True)

    num_motion_frames = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Log status"
