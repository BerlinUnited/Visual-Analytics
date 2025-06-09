import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from django.utils import timezone
from datetime import timedelta
import random
import pytest
from common.models import Event, Game, Experiment, VideoRecording, Log, LogStatus


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker('company')
    start_day = factory.Faker('date_object')
    end_day = factory.LazyAttribute(lambda o: o.start_day + timedelta(days=random.randint(1, 5)))
    timezone = factory.Faker('timezone')
    country = factory.Faker('country')
    location = factory.Faker('local_latlng')
    comment = factory.Faker('text')


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game

    event = factory.SubFactory(EventFactory)
    team1 = factory.Faker('company')
    team2 = factory.Faker('company')
    half = factory.fuzzy.FuzzyChoice(['half1', 'half2'])
    is_testgame = factory.Faker('boolean')
    head_ref = factory.Faker('name')
    assistent_ref = factory.Faker('name')
    field = factory.fuzzy.FuzzyChoice(['Field A', 'Field B', 'Field C'])
    start_time = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
    score = factory.LazyAttribute(lambda _: f"{random.randint(0,10)}:{random.randint(0,10)}")
    comment = factory.Faker('text')


class ExperimentFactory(DjangoModelFactory):
    class Meta:
        model = Experiment

    event = factory.SubFactory(EventFactory)
    name = factory.Faker('file_name')
    field = factory.fuzzy.FuzzyChoice(['Field A', 'Field B', 'Field C'])
    comment = factory.Faker('text')


class VideoRecordingFactory(DjangoModelFactory):
    class Meta:
        model = VideoRecording

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        game_is_set = 'game' in kwargs and kwargs.get('game')
        experiment_is_set = 'experiment' in kwargs and kwargs.get('experiment')
        
        if not game_is_set and not experiment_is_set:
            kwargs['game'] = GameFactory()

        return super()._create(model_class, *args, **kwargs)

    urls = factory.LazyAttribute(lambda _: {
        'main': f"https://youtube.com/watch?v={''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=11))}",
        'alternate': f"https://youtube.com/watch?v={''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=11))}"
    })
    comment = factory.Faker('text')


class LogFactory(DjangoModelFactory):
    class Meta:
        model = Log

    game = factory.SubFactory(GameFactory)
    experiment = None
    robot_version = factory.fuzzy.FuzzyChoice(['V5', 'V6'])
    player_number = factory.fuzzy.FuzzyInteger(1, 11)
    head_number = factory.fuzzy.FuzzyInteger(1, 100)
    body_serial = factory.LazyAttribute(lambda _: f"B{''.join(random.choices('0123456789', k=8))}")
    head_serial = factory.LazyAttribute(lambda _: f"H{''.join(random.choices('0123456789', k=8))}")
    representation_list = factory.LazyAttribute(lambda _: ['Image', 'BallModel', 'TeamState'])
    log_path = factory.Faker('file_path', extension='log')
    combined_log_path = factory.Faker('file_path', extension='log')
    sensor_log_path = factory.Faker('file_path', extension='log')
    is_favourite = factory.Faker('boolean')


class LogStatusFactory(DjangoModelFactory):
    class Meta:
        model = LogStatus

    log = factory.SubFactory(LogFactory)
    AudioData = factory.fuzzy.FuzzyInteger(1000, 10000)
    BallCandidates = factory.fuzzy.FuzzyInteger(1000, 10000)
    BallCandidatesTop = factory.fuzzy.FuzzyInteger(1000, 10000)
    BallModel = factory.fuzzy.FuzzyInteger(1000, 10000)
    BehaviorStateComplete = factory.fuzzy.FuzzyInteger(1000, 10000)
    BehaviorStateSparse = factory.fuzzy.FuzzyInteger(1000, 10000)
    CameraMatrix = factory.fuzzy.FuzzyInteger(1000, 10000)
    CameraMatrixTop = factory.fuzzy.FuzzyInteger(1000, 10000)
    FieldPercept = factory.fuzzy.FuzzyInteger(1000, 10000)
    FieldPerceptTop = factory.fuzzy.FuzzyInteger(1000, 10000)
    FrameInfo = factory.fuzzy.FuzzyInteger(1000, 10000)
    GoalPercept = factory.fuzzy.FuzzyInteger(1000, 10000)
    GoalPerceptTop = factory.fuzzy.FuzzyInteger(1000, 10000)
    MultiBallPercept = factory.fuzzy.FuzzyInteger(1000, 10000)
    RansacCirclePercept2018 = factory.fuzzy.FuzzyInteger(1000, 10000)
    RansacLinePercept = factory.fuzzy.FuzzyInteger(1000, 10000)
    RobotInfo = factory.fuzzy.FuzzyInteger(1000, 10000)
    ShortLinePercept = factory.fuzzy.FuzzyInteger(1000, 10000)
    ScanLineEdgelPercept = factory.fuzzy.FuzzyInteger(1000, 10000)
    ScanLineEdgelPerceptTop = factory.fuzzy.FuzzyInteger(1000, 10000)
    TeamMessageDecision = factory.fuzzy.FuzzyInteger(1000, 10000)
    TeamState = factory.fuzzy.FuzzyInteger(1000, 10000)
    OdometryData = factory.fuzzy.FuzzyInteger(1000, 10000)
    Image = factory.fuzzy.FuzzyInteger(1000, 10000)
    ImageTop = factory.fuzzy.FuzzyInteger(1000, 10000)
    ImageJPEG = factory.fuzzy.FuzzyInteger(1000, 10000)
    ImageJPEGTop = factory.fuzzy.FuzzyInteger(1000, 10000)
    WhistlePercept = factory.fuzzy.FuzzyInteger(1000, 10000)
    IMUData = factory.fuzzy.FuzzyInteger(1000, 10000)
    FSRData = factory.fuzzy.FuzzyInteger(1000, 10000)
    ButtonData = factory.fuzzy.FuzzyInteger(1000, 10000)
    SensorJointData = factory.fuzzy.FuzzyInteger(1000, 10000)
    AccelerometerData = factory.fuzzy.FuzzyInteger(1000, 10000)
    InertialSensorData = factory.fuzzy.FuzzyInteger(1000, 10000)
    MotionStatus = factory.fuzzy.FuzzyInteger(1000, 10000)
    MotorJointData = factory.fuzzy.FuzzyInteger(1000, 10000)
    GyrometerData = factory.fuzzy.FuzzyInteger(1000, 10000)
    num_motion_frames = factory.fuzzy.FuzzyInteger(1000, 10000)
