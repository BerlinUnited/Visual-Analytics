import pytest
from common.serializers import EventSerializer, GameSerializer, ExperimentSerializer, LogSerializer, LogStatusSerializer
from .factories import EventFactory, GameFactory, ExperimentFactory, LogFactory, LogStatusFactory

pytestmark = pytest.mark.unit

class TestSerializers:
    
    @pytest.mark.django_db
    def test_event_serializer(self):
        event = EventFactory.create()
        serializer = EventSerializer(event)
        data = serializer.data
        
        assert data['name'] == event.name
        assert data['country'] == event.country
        assert data['timezone'] == event.timezone
        
        # Test deserialization
        new_data = {
            'name': 'New Event',
            'country': 'Germany',
            'timezone': 'Europe/Berlin'
        }
        serializer = EventSerializer(data=new_data)
        assert serializer.is_valid()

    @pytest.mark.django_db
    def test_game_serializer(self):
        game = GameFactory.create()
        serializer = GameSerializer(game)
        data = serializer.data
        
        assert data['team1'] == game.team1
        assert data['team2'] == game.team2
        assert data['half'] == game.half
        assert data['event'] == game.event.id
        
        # Test deserialization
        event = EventFactory.create()
        new_data = {
            'event': event.id,
            'team1': 'Team X',
            'team2': 'Team Y',
            'half': 'half1'
        }
        serializer = GameSerializer(data=new_data)
        assert serializer.is_valid()

    @pytest.mark.django_db
    def test_experiment_serializer(self):
        experiment = ExperimentFactory.create()
        serializer = ExperimentSerializer(experiment)
        data = serializer.data
        
        assert data['name'] == experiment.name
        assert data['field'] == experiment.field
        assert data['event'] == experiment.event.id

    @pytest.mark.django_db
    def test_log_serializer_validation(self):
        game = GameFactory.create()
        experiment = ExperimentFactory.create()
        
        # Test valid data with game
        valid_game_data = {
            'game': game.id,
            'robot_version': 'V6',
            'player_number': 1
        }
        serializer = LogSerializer(data=valid_game_data, context={'request': type('Request', (), {'method': 'POST'})})
        assert serializer.is_valid()
        
        # Test valid data with experiment
        valid_exp_data = {
            'experiment': experiment.id,
            'robot_version': 'V6',
            'player_number': 1
        }
        serializer = LogSerializer(data=valid_exp_data, context={'request': type('Request', (), {'method': 'POST'})})
        assert serializer.is_valid()
        
        # Test invalid data with both game and experiment
        invalid_data = {
            'game': game.id,
            'experiment': experiment.id,
            'robot_version': 'V6'
        }
        serializer = LogSerializer(data=invalid_data, context={'request': type('Request', (), {'method': 'POST'})})
        assert not serializer.is_valid()
        assert 'Only one of game or experiment is allowed' in str(serializer.errors)

    @pytest.mark.django_db
    def test_log_serializer_properties(self):
        log = LogFactory.create()
        serializer = LogSerializer(log)
        data = serializer.data
        
        assert data['event_name'] == log.event_name
        assert data['game_name'] == log.game_name

    @pytest.mark.django_db
    def test_log_status_serializer(self):
        log_status = LogStatusFactory.create()
        serializer = LogStatusSerializer(log_status)
        data = serializer.data
        
        assert data['log'] == log_status.log.id
        assert data['AudioData'] == log_status.AudioData
        assert data['BallModel'] == log_status.BallModel
        assert data['num_motion_frames'] == log_status.num_motion_frames
        
        # Test deserialization
        new_log = LogFactory.create()
        new_data = {
            'log': new_log.id,
            'AudioData': 5000,
            'BallModel': 3000,
            'num_motion_frames': 8000
        }
        serializer = LogStatusSerializer(data=new_data)
        assert serializer.is_valid()
