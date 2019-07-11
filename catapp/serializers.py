# from exceptions import AttributeError

from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer

from catapp.models import GENDER_CHOICES

from .models import Breed, Cat, Home, Human


class GenderChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]


class HomeListingField(serializers.RelatedField):
    def to_representation(self, value):
        human = Human.objects.get(id=value.owner_id)
        home = Home.objects.get(id=human.home_id)
        return "Cat: %s, Home: %s" % (value.name, home)


class HomeSerializer(HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Home
        fields = "__all__"


class HumanSerializer(HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    cats = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="cat-detail"
    )
    # cats_name = serializers.StringRelatedField(many=True, read_only=True, source='cats')
    gender = GenderChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Human
        fields = "__all__"


class BreedSerializer(HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    homes = HomeListingField(many=True, source="cats", read_only=True)

    class Meta:
        model = Breed
        fields = "__all__"


class CatSerializer(HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    # gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    gender = GenderChoiceField(choices=GENDER_CHOICES)
    home = serializers.SerializerMethodField("owner_home")

    def owner_home(self, cat):
        return cat.owner.home.name

    class Meta:
        model = Cat
        fields = (
            "url",
            "name",
            "gender",
            "date_of_birth",
            "description",
            "breed",
            "owner",
            "home",
        )
