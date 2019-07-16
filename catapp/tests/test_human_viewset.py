from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from catapp import views

from ..models import Home, Human
from ..serializers import HumanSerializer


# Create your tests here.
class HumanViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("admin", "admin@example.com", "bar")
        self.token = Token.objects.create(user=self.user)
        self.home = Home.objects.create(name="My Home", address="My Address")
        self.john = Human.objects.create(
            name="John",
            gender="M",
            date_of_birth="1992-01-24",
            description="",
            home=self.home,
        )
        self.jane = Human.objects.create(
            name="Jane",
            gender="F",
            date_of_birth="1996-12-24",
            description="Just some description.",
            home=self.home,
        )

    def test_get_list(self):
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"get": "list"})
        request = factory.get(
            "/human/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the object and data count match
        self.assertEqual(len(response.data), Human.objects.all().count())

    def test_get_retrieve(self):
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"get": "retrieve"})
        request = factory.get(
            "/human/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.john.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if attributes in human object and response is same
        human = HumanSerializer(self.john, context={"request": request}).data
        self.assertDictContainsSubset(response.data, human)

    def test_get_retrieve_invalid_pk(self):
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"get": "retrieve"})
        request = factory.get(
            "/human/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        # Negative pk to test for invalid value
        response = view(request, pk=-2)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check error code
        self.assertEqual(response.data["detail"].code, "not_found")

    def test_post_create(self):
        # Build test server url
        url = "http://testserver{path}{id}/".format(
            path=reverse("home-list"), id=self.home.id
        )
        # Data to be created
        data = {
            "name": "Kitty",
            "gender": "F",
            "date_of_birth": "2000-06-17",
            "description": "Fictional cartoon character",
            "home": url,
        }
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/human/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # print(response.data)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if created object data matches 'post' data
        self.assertDictContainsSubset(data, response.data)

    def test_post_create_blank_data(self):
        # Data to be created
        data = {
            "name": "",
            "gender": "",
            "date_of_birth": "",
            "description": "",
            "home": "",
        }
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/human/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check error code
        for value in response.data.values():
            self.assertIn(
                value[0].code, ["blank", "required", "invalid_choice", "null"]
            )

    def test_put_update(self):
        # Build test server url
        url = "http://testserver{path}{id}/".format(
            path=reverse("home-list"), id=self.home.id
        )
        # Data to be created
        data = {
            "name": "John Edited",
            "gender": "M",
            "date_of_birth": "2000-06-17",
            "description": "",
            "home": url,
        }
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"put": "update"})
        request = factory.put(
            "/human/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.john.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if updated object matches 'put' data
        self.assertDictContainsSubset(data, response.data)

    def test_patch_partial_update(self):
        # Data to be updated
        data = {"name": "John Edited"}
        factory = APIRequestFactory()
        view = views.HumanViewSet.as_view(actions={"patch": "partial_update"})
        request = factory.patch(
            "/human/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.john.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh updated object from db
        self.john.refresh_from_db()
        # Check if updated object matches 'patch' data
        self.assertEqual((Human.objects.get(pk=self.john.id).name), data["name"])
        # Check that fields that are not 'patched' remains the same
        human = HumanSerializer(self.john, context={"request": request}).data
        self.assertDictContainsSubset(human, response.data)
