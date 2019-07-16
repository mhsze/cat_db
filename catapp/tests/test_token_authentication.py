from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from catapp import views


# Create your tests here.
class TokenAuthenticationAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("admin", "admin@example.com", "bar")
        self.token = Token.objects.create(user=self.user)

    def test_valid_token(self):
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"get": "list"})
        request = factory.get(
            "/human/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_token(self):
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"get": "list"})
        request = factory.get("/human/")
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Check error detail
        self.assertEqual(
            str(response.data["detail"]),
            "Authentication credentials were not provided.",
        )

    def test_invalid_token(self):
        # Save token key into variable
        key = self.token.key
        # Delete token object
        self.token.delete()
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"get": "list"})
        request = factory.get("/human/", HTTP_AUTHORIZATION="Token {}".format(key))
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Check error detail
        self.assertEqual(str(response.data["detail"]), "Invalid Token")

    def test_expired_token(self):
        # Set token created date to -1day, 10hours, Default token expiry time is 1day
        self.token.created = timezone.now() - timedelta(days=1, hours=10)
        # Save token with modified created date
        self.token.save()
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"get": "list"})
        request = factory.get(
            "/human/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Check error detail
        self.assertEqual(str(response.data["detail"]), "The Token is expired")
