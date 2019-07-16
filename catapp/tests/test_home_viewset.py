from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from catapp import views

from ..models import Home
from ..serializers import HomeSerializer


# Create your tests here.
class HomeViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("admin", "admin@example.com", "bar")
        self.token = Token.objects.create(user=self.user)
        self.home = Home.objects.create(name="My Home", address="My Address")
        self.office = Home.objects.create(
            name="Office", address="Wisma Goshen", type=Home.CONDO
        )

    def test_get_list(self):
        factory = APIRequestFactory()
        view = views.HomeViewSet.as_view(actions={"get": "list"})
        request = factory.get(
            "/home/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the object and data count match
        self.assertEqual(len(response.data), Home.objects.all().count())

    def test_get_retrieve(self):
        factory = APIRequestFactory()
        view = views.HomeViewSet.as_view(actions={"get": "retrieve"})
        request = factory.get(
            "/home/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.home.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if attributes in home object and response is same
        home = HomeSerializer(self.home, context={"request": request}).data
        self.assertDictContainsSubset(response.data, home)

    def test_get_retrieve_invalid_pk(self):
        factory = APIRequestFactory()
        view = views.HomeViewSet.as_view(actions={"get": "retrieve"})
        request = factory.get(
            "/home/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        # Negative pk to test for invalid value
        response = view(request, pk=-2)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check error code
        self.assertEqual(response.data["detail"].code, "not_found")

    def test_post_create(self):
        # Data to be created
        data = {"name": "Garden", "address": "Happy Garden 1", "type": Home.CONDO}
        factory = APIRequestFactory()
        view = views.HomeViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/home/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if created object data matches 'post' data
        self.assertDictContainsSubset(data, response.data)

    def test_post_create_blank_data(self):
        # Data to be created
        data = {"name": "", "address": "", "type": ""}
        factory = APIRequestFactory()
        view = views.HomeViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/home/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check error code
        for value in response.data.values():
            self.assertEqual(value[0].code, "blank")

    def test_post_create_invalid_choice(self):
        # Data to be created
        data = {"name": "Garden", "address": "Happy Garden 1", "type": "BLABLA"}
        factory = APIRequestFactory()
        view = views.HomeViewSet.as_view(actions={"post": "create"})
        request = factory.post(
            "/home/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check error code
        self.assertEqual(response.data["type"][0].code, "invalid_choice")

    def test_put_update(self):
        # Data to be updated
        data = {"name": "Home Edited", "address": "Home Sweet Home", "type": Home.CONDO}
        # Check that initial Home object data is not equal to data to be updated
        self.assertNotEqual(self.home.address, data["address"])
        factory = APIRequestFactory()
        view = views.HomeViewSet.as_view(actions={"put": "update"})
        request = factory.put(
            "/home/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.home.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if updated object matches 'put' data
        self.assertDictContainsSubset(data, response.data)

    def test_patch_partial_update(self):
        # Data to be updated
        data = {"address": "Home Sweet Home"}
        # Check that initial Home object data is not equal to data to be updated
        self.assertNotEqual(self.home.address, data["address"])
        factory = APIRequestFactory()
        view = views.HomeViewSet.as_view(actions={"patch": "partial_update"})
        request = factory.patch(
            "/home/", data=data, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        response = view(request, pk=self.home.id)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh updated object from db
        self.home.refresh_from_db()
        # Check if updated object matches 'patch' data
        self.assertEqual((Home.objects.get(pk=self.home.id).address), data["address"])
        # Check that fields that are not 'patched' remains the same
        home = HomeSerializer(self.home, context={"request": request}).data
        self.assertDictContainsSubset(home, response.data)
