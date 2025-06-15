import pytest
from .factories import EventFactory
from common.models import Event
import json
pytestmark = pytest.mark.unit

class TestCommonViews:
    
    def test_health_check(self,client):
        response = client.get('/api/health/')
        assert response.status_code == 200
        assert json.loads(response.content) == {"message": "UP"}
    
    @pytest.mark.django_db
    def test_event_list(self,auth_client):
        EventFactory.create_batch(size=3)
        response = auth_client.get('/api/events/')

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    @pytest.mark.django_db
    def test_event_create(self, admin_client):
        # Create event data using factory but don't save to DB
        event_data = EventFactory.build()
        
        # Convert the factory-generated data to a dictionary for JSON serialization
        event_json = {
            'name': event_data.name,
            'start_day': event_data.start_day.isoformat() if event_data.start_day else None,
            'end_day': event_data.end_day.isoformat() if event_data.end_day else None,
            'timezone': event_data.timezone,
            'country': event_data.country,
            'location': event_data.location,
            'comment': event_data.comment
        }
        # Make POST request to create event
        response = admin_client.post('/api/events/', event_json, format='json')
        
        # Assert successful creation
        assert response.status_code == 201
        response_data = json.loads(response.content)
        
        # Verify the created event data matches what we sent
        assert response_data['name'] == event_json['name']
        assert response_data['start_day'] == event_json['start_day']
        assert response_data['end_day'] == event_json['end_day']
        assert response_data['timezone'] == event_json['timezone']
        assert response_data['country'] == event_json['country']
        assert response_data['location'] == event_json['location']
        assert response_data['comment'] == event_json['comment']
        
        # Verify the event was actually created in the database
        assert Event.objects.filter(name=event_json['name']).exists()

    @pytest.mark.django_db
    def test_event_bulk_create(self, admin_client):
        # Create event data using factory but don't save to DB
        event_data = EventFactory.build_batch(5)
        
        payload = []
        for event in event_data:
            # Convert the factory-generated data to a dictionary for JSON serialization
            event_json = {
                'name': event.name,
                'start_day': event.start_day.isoformat(),
                'end_day': event.end_day.isoformat(),
                'timezone': event.timezone,
                'country': event.country,
                'location': event.location,
                'comment': event.comment
            }
            payload.append(event_json)
        # Make POST request to create event
        response = admin_client.post('/api/events/', payload, format='json')
        
        # Assert successful creation
        assert response.status_code == 200
        response_data = json.loads(response.content)
        
        # Assert correct return values
        assert response_data["created"] == 5
        assert response_data["existing"] == 0
        for idx,data in enumerate(response_data["events"]):
            assert data['name'] == payload[idx]['name']
            assert data['start_day'] == payload[idx]['start_day']
            assert data['end_day'] == payload[idx]['end_day']
            assert data['timezone'] == payload[idx]['timezone']
            assert data['country'] == payload[idx]['country']
            assert data['location'] == payload[idx]['location']
            assert data['comment'] == payload[idx]['comment']

        #Verify the event was actually created in the database
        assert Event.objects.count() == 5
