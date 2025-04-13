from django.test import TestCase
from common.models import Event,Game,Experiment,Log

class LogTypeTestCase(TestCase):
    def setUp(self):
        TestEvent = Event.objects.create(name="Test Event")
        self.game = Game.objects.create(event=TestEvent,team1='Berlin Test',team2='Nao Test',half='half2')
        self.experiment = Experiment.objects.create(event=TestEvent,name='Test Experiment')
        return super().setUp()
        
    def test_log_type_returns_game_or_experiment_instance(self):
        game_log = Log.objects.create(game=self.game,player_number=3)
        experiment_log = Log.objects.create(experiment=self.experiment,player_number=3)
        self.assertEqual(experiment_log.log_type,self.experiment)
        self.assertEqual(game_log.log_type,self.game)