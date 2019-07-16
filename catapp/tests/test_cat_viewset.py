from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from catapp import views

from ..models import Breed, Cat, Home, Human
from ..serializers import CatSerializer


# Create your tests here.
class CatViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("admin", "admin@example.com", "bar")
        self.token = Token.objects.create(user=self.user)
        self.home = Home.objects.create(name="My Home", address="My Address")
        self.owner = Human.objects.create(
            name="John",
            gender="M",
            date_of_birth="1992-01-24",
            description="",
            home=self.home,
        )
        self.breed = Breed.objects.create(
            name="Japanese Bobtail", origin="Japan", description="Born in japan"
        )
        self.kitty = Cat.objects.create(
            name="Kitty",
            gender="M",
            date_of_birth="2002-01-24",
            description="",
            breed=self.breed,
            owner=self.owner,
        )
        self.summer = Cat.objects.create(
            name="Summer",
            gender="M",
            date_of_birth="2003-12-24",
            description="Just some description.",
            breed=self.breed,
            owner=self.owner,
        )

    def test_get_list(self):
        factory = APIRequestFactory()
        view = views.CatViewSet.as_view(actions={"get": "list"})
        request = factory.get(
            "/cat/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the object and data count match
        self.assertEqual(len(response.data), Cat.objects.all().count())

    def test_get_retrieve(self):
        factory = APIRequestFactory()
        view = views.CatViewSet.as_view(actions={"get": "retrieve"})
        request = factory.get(
            "/cat/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.kitty.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if attributes in cat object and response is same
        cat = CatSerializer(self.kitty, context={"request": request}).data
        self.assertDictContainsSubset(response.data, cat)

    def test_get_retrieve_invalid_pk(self):
        factory = APIRequestFactory()
        view = views.CatViewSet.as_view(actions={"get": "retrieve"})
        request = factory.get(
            "/cat/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        # Negative pk to test for invalid value
        response = view(request, pk=-2)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check error code
        self.assertEqual(response.data["detail"].code, "not_found")

    def test_post_create(self):
        # Build test server url
        owner_url = "http://testserver{path}{id}/".format(
            path=reverse("human-list"), id=self.owner.id
        )
        breed_url = "http://testserver{path}{id}/".format(
            path=reverse("breed-list"), id=self.breed.id
        )
        # Data to be created
        data = {
            "name": "Kitty Created",
            "gender": "M",
            "date_of_birth": "2010-06-17",
            "description": "Dummy kitty for post create.",
            "breed": breed_url,
            "owner": owner_url,
        }
        factory = APIRequestFactory()
        view = views.CatViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/cat/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
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
        view = views.CatViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/cat/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
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
        owner_url = "http://testserver{path}{id}/".format(
            path=reverse("human-list"), id=self.owner.id
        )
        breed_url = "http://testserver{path}{id}/".format(
            path=reverse("breed-list"), id=self.breed.id
        )
        # Data to be created
        data = {
            "name": "Kitty Edited",
            "gender": "M",
            "date_of_birth": "2000-06-17",
            "description": "Dummy kitty for put update.",
            "breed": breed_url,
            "owner": owner_url,
        }
        factory = APIRequestFactory()
        view = views.CatViewSet.as_view(actions={"put": "update"})
        request = factory.put(
            "/cat/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.kitty.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if updated object matches 'put' data
        self.assertDictContainsSubset(data, response.data)

    def test_patch_partial_update(self):
        # Data to be updated
        data = {
            "name": "Kitty Edited",
            "description": "Dummy kitty for patch partial update.",
        }
        factory = APIRequestFactory()
        view = views.CatViewSet.as_view(actions={"patch": "partial_update"})
        request = factory.patch(
            "/cat/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.kitty.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh updated object from db
        self.kitty.refresh_from_db()
        # Check if updated object matches 'patch' data
        self.assertEqual((Cat.objects.get(pk=self.kitty.id).name), data["name"])
        # Check that fields that are not 'patched' remains the same
        cat = CatSerializer(self.kitty, context={"request": request}).data
        self.assertDictContainsSubset(cat, response.data)
