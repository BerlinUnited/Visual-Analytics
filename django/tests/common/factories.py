import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from django.utils import timezone
from datetime import timedelta
import random

from common.models import Event, Game, Experiment, VideoRecording, Log, LogStatus


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker("company")
    start_day = factory.Faker("date_object")
    end_day = factory.LazyAttribute(
        lambda o: o.start_day + timedelta(days=random.randint(1, 5))
    )
    timezone = factory.Faker("timezone")
    country = factory.Faker("country")
    location = '41° 53\'00”,41° 53\'00”,'
    comment = factory.Faker("text")


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game

    event = factory.SubFactory(EventFactory)
    team1 = factory.Faker("company")
    team2 = factory.Faker("company")
    half = fuzzy.FuzzyChoice(["half1", "half2"])
    is_testgame = factory.Faker("boolean")
    head_ref = factory.Faker("name")
    assistent_ref = factory.Faker("name")
    field = fuzzy.FuzzyChoice(["Field A", "Field B", "Field C"])
    start_time = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    score = factory.LazyAttribute(
        lambda _: f"{random.randint(0, 10)}:{random.randint(0, 10)}"
    )
    comment = factory.Faker("text")


class ExperimentFactory(DjangoModelFactory):
    class Meta:
        model = Experiment

    event = factory.SubFactory(EventFactory)
    name = factory.Faker("file_name")
    field = fuzzy.FuzzyChoice(["Field A", "Field B", "Field C"])
    comment = factory.Faker("text")


class VideoRecordingFactory(DjangoModelFactory):
    class Meta:
        model = VideoRecording

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        game_is_set = "game" in kwargs and kwargs.get("game")
        experiment_is_set = "experiment" in kwargs and kwargs.get("experiment")

        if not game_is_set and not experiment_is_set:
            kwargs["game"] = GameFactory()

        return super()._create(model_class, *args, **kwargs)

    url = factory.Faker("url")
    comment = factory.Faker("text")


class LogFactory(DjangoModelFactory):
    class Meta:
        model = Log

    game = factory.SubFactory(GameFactory)
    experiment = None
    robot_version = fuzzy.FuzzyChoice(["V5", "V6"])
    player_number = fuzzy.FuzzyInteger(1, 11)
    head_number = fuzzy.FuzzyInteger(1, 100)
    body_serial = factory.LazyAttribute(
        lambda _: f"B{''.join(random.choices('0123456789', k=8))}"
    )
    head_serial = factory.LazyAttribute(
        lambda _: f"H{''.join(random.choices('0123456789', k=8))}"
    )
    representation_list = factory.LazyAttribute(
        lambda _: ["Image", "BallModel", "TeamState"]
    )
    log_path = factory.Faker("file_path", extension="log")
    combined_log_path = factory.Faker("file_path", extension="log")
    sensor_log_path = factory.Faker("file_path", extension="log")
    is_favourite = factory.Faker("boolean")


class LogStatusFactory(DjangoModelFactory):
    class Meta:
        model = LogStatus

    log = factory.SubFactory(LogFactory)
    AudioData = fuzzy.FuzzyInteger(1000, 10000)
    BallCandidates = fuzzy.FuzzyInteger(1000, 10000)
    BallCandidatesTop = fuzzy.FuzzyInteger(1000, 10000)
    BallModel = fuzzy.FuzzyInteger(1000, 10000)
    BehaviorStateComplete = fuzzy.FuzzyInteger(1000, 10000)
    BehaviorStateSparse = fuzzy.FuzzyInteger(1000, 10000)
    CameraMatrix = fuzzy.FuzzyInteger(1000, 10000)
    CameraMatrixTop = fuzzy.FuzzyInteger(1000, 10000)
    FieldPercept = fuzzy.FuzzyInteger(1000, 10000)
    FieldPerceptTop = fuzzy.FuzzyInteger(1000, 10000)
    FrameInfo = fuzzy.FuzzyInteger(1000, 10000)
    GoalPercept = fuzzy.FuzzyInteger(1000, 10000)
    GoalPerceptTop = fuzzy.FuzzyInteger(1000, 10000)
    MultiBallPercept = fuzzy.FuzzyInteger(1000, 10000)
    RansacCirclePercept2018 = fuzzy.FuzzyInteger(1000, 10000)
    RansacLinePercept = fuzzy.FuzzyInteger(1000, 10000)
    RobotInfo = fuzzy.FuzzyInteger(1000, 10000)
    ShortLinePercept = fuzzy.FuzzyInteger(1000, 10000)
    ScanLineEdgelPercept = fuzzy.FuzzyInteger(1000, 10000)
    ScanLineEdgelPerceptTop = fuzzy.FuzzyInteger(1000, 10000)
    TeamMessageDecision = fuzzy.FuzzyInteger(1000, 10000)
    TeamState = fuzzy.FuzzyInteger(1000, 10000)
    OdometryData = fuzzy.FuzzyInteger(1000, 10000)
    Image = fuzzy.FuzzyInteger(1000, 10000)
    ImageTop = fuzzy.FuzzyInteger(1000, 10000)
    ImageJPEG = fuzzy.FuzzyInteger(1000, 10000)
    ImageJPEGTop = fuzzy.FuzzyInteger(1000, 10000)
    WhistlePercept = fuzzy.FuzzyInteger(1000, 10000)
    IMUData = fuzzy.FuzzyInteger(1000, 10000)
    FSRData = fuzzy.FuzzyInteger(1000, 10000)
    ButtonData = fuzzy.FuzzyInteger(1000, 10000)
    SensorJointData = fuzzy.FuzzyInteger(1000, 10000)
    AccelerometerData = fuzzy.FuzzyInteger(1000, 10000)
    InertialSensorData = fuzzy.FuzzyInteger(1000, 10000)
    MotionStatus = fuzzy.FuzzyInteger(1000, 10000)
    MotorJointData = fuzzy.FuzzyInteger(1000, 10000)
    GyrometerData = fuzzy.FuzzyInteger(1000, 10000)
    num_motion_frames = fuzzy.FuzzyInteger(1000, 10000)
