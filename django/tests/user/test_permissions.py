import pytest
from ..common.factories import EventFactory
from common.models import Event
pytestmark = pytest.mark.unit

class TestPermissions:
    event_url = "/api/events/"

    def test_no_user(self,client):
        response = client.get(self.event_url)
        # FIXME : 401 should be the status code for this request
        assert response.status_code == 403
        assert response.data == {"detail": "Authentication credentials were not provided."}
    
    @pytest.mark.django_db
    def test_wrong_token(self,client):
        client.credentials(
            HTTP_AUTHORIZATION="Token " + "642bcac87fd25e8719d48cf144e13653fb015ae"
        )
        response = client.get(self.event_url)
        assert response.status_code == 403
        assert response.data ==  {"detail": "Invalid token."}
    @pytest.mark.django_db
    def test_get_w_token(self,auth_client):
        response = auth_client.get(self.event_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_post_normal_user(self,auth_client):

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


        response = auth_client.post(self.event_url, event_json)
        assert response.status_code == 403
        assert response.data == {"detail": "You do not have permission to perform this action."}
    
    @pytest.mark.django_db
    def test_post_berlin_user(self,admin_client):
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
        
        response = admin_client.post(self.event_url, event_json)
       
        assert response.status_code == 201
        assert Event.objects.filter(name=event_json["name"]).exists()