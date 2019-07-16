from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from ..models import Home
from ..serializers import HomeSerializer


class HomeSerializerTestCase(TestCase):
    def setUp(self):
        self.office = Home.objects.create(
            name="Office", address="Wisma Goshen", type=Home.CONDO
        )
        self.factory = APIRequestFactory()
        self.request = self.factory.get("/home/")
        # Build hyperlinked home instance url
        self.home_url = "http://testserver{path}{id}/".format(
            path=reverse("home-list"), id=self.office.id
        )

    def test_serializer_retrieve(self):
        # Initialize serializer instance
        office = HomeSerializer(self.office, context={"request": self.request})
        # Add url to office object due to using hyperlinked serializer
        self.office.url = self.home_url
        # Check if serializer and model object is the same
        self.assertDictContainsSubset(office.data, self.office.__dict__)

    def test_serializer_update(self):
        # Initialize serializer instance
        data = {
            "name": "Office Edited",
            "address": "Address Edited",
            "type": Home.LANDED,
        }
        office = HomeSerializer(
            self.office, data=data, context={"request": self.request}
        )
        if office.is_valid(raise_exception=True):
            office.save()
        # Refresh from db
        self.office.refresh_from_db()
        # Add url to office object due to using hyperlinked serializer
        self.office.url = self.home_url
        # Check if serializer and model object is the same
        self.assertDictContainsSubset(office.data, self.office.__dict__)

    def test_serializer_create(self):
        # Prepare data to create
        data = {"name": "New Home", "address": "New Address", "type": Home.LANDED}
        # Serialize data
        new_home = HomeSerializer(data=data, context={"request": self.request})
        # Save new home object is data is valid
        if new_home.is_valid(raise_exception=True):
            created_home = new_home.save()
        # Extract created object
        db_home = Home.objects.get(id=created_home.id)
        # Assert if created data matches correctly
        self.assertDictContainsSubset(data, db_home.__dict__)
