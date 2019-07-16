from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from catapp import views

from ..models import Breed
from ..serializers import BreedSerializer


# Create your tests here.
class BreedViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("admin", "admin@example.com", "bar")
        self.token = Token.objects.create(user=self.user)
        self.persian = Breed.objects.create(
            name="Persian", origin="Europe", description="Cute fluffy kitty"
        )
        self.bobtail = Breed.objects.create(
            name="Japanese Bobtail", origin="Japan", description="Born in japan"
        )

    def test_get_list(self):
        factory = APIRequestFactory()
        view = views.BreedViewSet.as_view(actions={"get": "list"})
        request = factory.get(
            "/breed/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the object and data count match
        self.assertEqual(len(response.data), Breed.objects.all().count())

    def test_get_retrieve(self):
        factory = APIRequestFactory()
        view = views.BreedViewSet.as_view(actions={"get": "retrieve"})
        request = factory.get(
            "/breed/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.persian.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if attributes in breed object and response is same
        breed = BreedSerializer(self.persian, context={"request": request}).data
        self.assertDictContainsSubset(response.data, breed)

    def test_get_retrieve_invalid_pk(self):
        factory = APIRequestFactory()
        view = views.BreedViewSet.as_view(actions={"get": "retrieve"})
        request = factory.get(
            "/breed/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        # Negative pk to test for invalid value
        response = view(request, pk=-2)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check error code
        self.assertEqual(response.data["detail"].code, "not_found")

    def test_post_create(self):
        # Data to be created
        data = {
            "name": "Kitty",
            "origin": "Hello Kitty",
            "description": "Fictional cartoon character",
        }
        factory = APIRequestFactory()
        view = views.BreedViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/breed/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if created object data matches 'post' data
        self.assertDictContainsSubset(data, response.data)

    def test_post_create_blank_data(self):
        # Data to be created
        data = {"name": "", "origin": "", "description": ""}
        factory = APIRequestFactory()
        view = views.BreedViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/breed/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check error code
        for value in response.data.values():
            self.assertEqual(value[0].code, "blank")

    def test_put_update(self):
        # Data to be updated
        data = {
            "name": "Kitty Edited",
            "origin": "Hello Kitty",
            "description": "Fictional cartoon character",
        }
        factory = APIRequestFactory()
        view = views.BreedViewSet.as_view(actions={"put": "update"})
        request = factory.put(
            "/breed/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.persian.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if updated object matches 'put' data
        self.assertDictContainsSubset(data, response.data)

    def test_patch_partial_update(self):
        # Data to be updated
        data = {"origin": "Hello Kitty Edited"}
        factory = APIRequestFactory()
        view = views.BreedViewSet.as_view(actions={"patch": "partial_update"})
        request = factory.patch(
            "/breed/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.persian.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh updated object from db
        self.persian.refresh_from_db()
        # Check if updated object matches 'patch' data
        self.assertEqual((Breed.objects.get(pk=self.persian.id).origin), data["origin"])
        # Check that fields that are not 'patched' remains the same
        breed = BreedSerializer(self.persian, context={"request": request}).data
        self.assertDictContainsSubset(breed, response.data)
