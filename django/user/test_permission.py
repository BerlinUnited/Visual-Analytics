from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from common.models import Event

# get VATUser model
User = get_user_model()


class PermissionTest(APITestCase):
    """test for the IsBerlinUnitedOrReadOnly permission class
    following https://www.django-rest-framework.org/api-guide/testing/
    """

    # setup function is called before every test
    def setUp(self):
        self.event_url = "/api/events/"
        self.normal_user = User.objects.create_user(
            username="john", email="john@doe.com", password="js.sj"
        )
        self.user_token = Token.objects.get(user=self.normal_user)
        self.super_user = User.objects.create_superuser(
            username="jane", email="jane@doe.com", password="jane123"
        )
        self.admin_token = Token.objects.get(user=self.super_user)
        self.test_data = {"name": "RoboCup 2027"}
        return super().setUp()

    def test_no_user(self):
        response = self.client.get(self.event_url)
        #FIXME : 401 should be the status code for this request
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )

    def test_wrong_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + "642bcac87fd25e8719d48cf144e13653fb015ae"
        )
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "Invalid token."})

    # def test_expired_jwt(self):
    #     refresh = RefreshToken.for_user(self.normal_user)
    #     time.sleep(61)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    #     response = self.client.get(self.event_url)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_w_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_w_jwt(self):
        refresh = RefreshToken.for_user(self.normal_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(self.event_url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )

    def test_post_berlin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response = self.client.post(self.event_url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(name=self.test_data["name"]).exists())
