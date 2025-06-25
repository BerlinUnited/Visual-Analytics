import pytest
from common.models import Event, Game, Log, Experiment, VideoRecording, LogStatus
from .factories import (
    EventFactory,
    GameFactory,
    ExperimentFactory,
    VideoRecordingFactory,
    LogFactory,
    LogStatusFactory,
)

pytestmark = pytest.mark.unit


class TestCommonModels:
    @pytest.mark.django_db
    def test_event(self):
        EventFactory.create(name="RC2024")
        assert Event.objects.count() == 1
        db_event = Event.objects.first()
        assert str(db_event) == "RC2024"
        assert db_event.name == "RC2024"

    @pytest.mark.django_db
    def test_game(self):
        GameFactory.create(
            half="half1",
            start_time="2024-01-01 12:00:00+00:00",
        )
        assert Game.objects.count() == 1
        db_game = Game.objects.first()
        assert str(db_game) == "2024-01-01 12:00:00+00:00: Team A vs Team B half1"
        assert db_game.team1 == "Team A"
        assert db_game.team2 == "Team B"
        assert db_game.half == "half1"
        assert db_game.event is not None

    @pytest.mark.django_db
    def test_experiment(self):
        ExperimentFactory.create(name="test_experiment", field="Field A")
        assert Experiment.objects.count() == 1
        db_experiment = Experiment.objects.first()
        assert db_experiment.name == "test_experiment"
        assert db_experiment.field == "Field A"
        assert db_experiment.event is not None

    @pytest.mark.django_db
    def test_video_recording_with_game(self):
        url = "https://youtube.com/watch?v=789"
        VideoRecordingFactory.create(url=url)
        assert VideoRecording.objects.count() == 1
        db_recording = VideoRecording.objects.first()
        assert db_recording.url == url
        assert db_recording.game is not None
        assert db_recording.experiment is None

    @pytest.mark.django_db
    def test_video_recording_with_experiment(self):
        url = "https://youtube.com/watch?v=789"
        experiment = ExperimentFactory.create()
        VideoRecordingFactory.create(experiment=experiment, url=url)
        assert VideoRecording.objects.count() == 1
        db_recording = VideoRecording.objects.first()
        assert db_recording.url == url
        assert db_recording.game is None
        assert db_recording.experiment == experiment

    @pytest.mark.django_db
    def test_log_creation(self):
        log = LogFactory.create(
            robot_version="V6",
            player_number=3,
            head_number=42,
            body_serial="B12345678",
            head_serial="H87654321",
            representation_list=["Image", "BallModel"],
        )
        assert Log.objects.count() == 1
        db_log = Log.objects.first()
        assert str(db_log) == log.log_path
        assert db_log.robot_version == "V6"
        assert db_log.player_number == 3
        assert db_log.head_number == 42
        assert db_log.body_serial == "B12345678"
        assert db_log.head_serial == "H87654321"
        assert db_log.representation_list == ["Image", "BallModel"]
        assert db_log.game is not None
        assert db_log.experiment is None

    @pytest.mark.django_db
    def test_log_type_property(self):
        game = GameFactory.create()
        experiment = ExperimentFactory.create()

        game_log = LogFactory.create(game=game, experiment=None)
        experiment_log = LogFactory.create(game=None, experiment=experiment)

        assert game_log.log_type == game
        assert experiment_log.log_type == experiment

    @pytest.mark.django_db
    def test_log_properties(self):
        game = GameFactory.create(
            team1="Team A",
            team2="Team B",
            half="half1",
        )
        log = LogFactory.create(game=game)

        assert log.event_name == game.event.name
        assert log.game_name == "Team A_vs_Team B_half1"

    @pytest.mark.django_db
    def test_log_status(self):
        # Create a LogStatus with specific values
        LogStatusFactory.create(
            AudioData=5000,
            BallModel=3000,
            Image=2500,
            ImageTop=2500,
            num_motion_frames=8000,
        )

        assert LogStatus.objects.count() == 1
        db_log_status = LogStatus.objects.first()

        # Check relationship with Log
        assert db_log_status.log is not None
        assert isinstance(db_log_status.log, Log)

        # Check specific values we set
        assert db_log_status.AudioData == 5000
        assert db_log_status.BallModel == 3000
        assert db_log_status.Image == 2500
        assert db_log_status.ImageTop == 2500
        assert db_log_status.num_motion_frames == 8000

        # Verify some fields are nullable
        log_status_minimal = LogStatusFactory.create(log=LogFactory.create(), AudioData=None, BallModel=None)
        assert log_status_minimal.AudioData is None
        assert log_status_minimal.BallModel is None
