from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from ..models import Breed
from ..serializers import BreedSerializer
from ..views import BreedViewSet


class BreedSerializerTestCase(TestCase):
    def setUp(self):
        self.bobtail = Breed.objects.create(
            name="Japanese Bobtail", origin="Japan", description="Dummy description."
        )
        self.factory = APIRequestFactory()
        self.request = self.factory.get("/breed/")
        # Build hyperlinked breed instance url
        self.breed_url = "http://testserver{path}{id}/".format(
            path=reverse("breed-list"), id=self.bobtail.id
        )

    def test_serializer_retrieve(self):
        # Generate token
        self.user = User.objects.create_user("admin", "admin@example.com", "bar")
        self.token = Token.objects.create(user=self.user)
        # Overwrite setup request to include auth token for data retrieval
        self.request = self.factory.get(
            "/breed/", HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        view = BreedViewSet.as_view(actions={"get": "retrieve"})
        response = view(self.request, pk=self.bobtail.id)
        # Initialize serializer instance
        bobtail = BreedSerializer(self.bobtail, context={"request": self.request})
        # Check if serializer and response data is the same
        self.assertDictContainsSubset(bobtail.data, response.data)

    def test_serializer_update(self):
        # Initialize serializer instance
        data = {
            "name": "Breed Edited",
            "origin": "Origin Edited",
            "description": "Dummy Edited Description.",
        }
        bobtail = BreedSerializer(
            self.bobtail, data=data, context={"request": self.request}
        )
        if bobtail.is_valid(raise_exception=True):
            bobtail.save()
        # Check if serializer and model object is the same
        self.assertDictContainsSubset(data, bobtail.data)

    def test_serializer_create(self):
        # Prepare data to create
        data = {
            "name": "New Breed",
            "origin": "New Origin",
            "description": "New Dummy Description.",
        }
        # Serialize data
        new_breed = BreedSerializer(data=data, context={"request": self.request})
        # Save new breed object is data is valid
        if new_breed.is_valid(raise_exception=True):
            created_breed = new_breed.save()
        # Extract created object
        db_breed = Breed.objects.get(id=created_breed.id)
        # Assert if created data matches correctly
        self.assertDictContainsSubset(data, db_breed.__dict__)
